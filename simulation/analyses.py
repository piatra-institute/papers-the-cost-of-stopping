"""A capability-hysteresis model of a reactor-building system, for *The Cost of Stopping*.

A continent builds reactors. Its ability to build them economically is a stock,
K in [0, 1]: design teams, qualified suppliers, nuclear-grade certification,
regulators who remember how to license new construction, owners who know how to
run a megaproject. The stock obeys two clocks that do not match:

    forgetting runs on the calendar   K decays every idle year
    learning arrives at completion    K rises only when a unit is finished

The cost of a unit rises as capability falls, C(K) = exp(lam * (K_mature - K)),
normalized so a mature programme builds at 1.0, and the time to build a unit
rises the same way. The feedback that would repair a decayed stock therefore
arrives with a delay the decay itself created. That asymmetry is the model's
engine, and everything the paper reports comes out of it: the stock-flow
illusion (output holds its peak for decades after orders stop, because the
fleet is a stock and the orders were the flow), the ratchet (a short order
freeze self-repairs, a long one locks), the self-validating trap (a chooser
who prices the next unit off current capability finds every restart probe
confirming that stopping was correct), the hysteresis asymmetry (capability
lost in G idle years takes longer than G building years to buy back), and the
coordination wedge (when capability spills across borders, national choosers
under-build relative to a continental planner).

Calibration is anchoring, and the two anchors are documented magnitudes: a
fourteen-year construction-start hiatus (Civaux-2 1991 to Olkiluoto-3 2005,
IAEA RDS-2) after which the first projects arrived at roughly four times their
original estimates (NAO 2026), and a series effect of about 15% on the second
unit of a pair (NEA 7530). The fourteen years are counted as idle; in the
record a construction trickle persisted into the 1990s, so the documented
fourfold outcome puts a floor under the pure-idleness decay rate. Everything
downstream is a fact about the model's geometry, disciplined by those anchors.
Nothing here is an econometric estimate, and the paper says so where it
reports the numbers.

The model is deterministic. There is no sampled randomness anywhere; a rerun
reproduces every number bit for bit.

Scale. One unit is 1.4 GW at capacity factor 0.80, about 9.8 TWh a year. Money
is measured in mature-programme unit costs (1.0 buys one reactor at full
capability). Demand, hydro and renewables are stylized logistic paths at
continental Western European scale. The model's TWh are not Europe's TWh and
are never quoted as if they were.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# constants and calibration
# ---------------------------------------------------------------------------

Y0, Y1 = 1955, 2040
YEARS = np.arange(Y0, Y1 + 1)
N_YEARS = len(YEARS)

UNIT_GW = 1.4
CAP_FACTOR = 0.80
TWH_PER_UNIT = UNIT_GW * 8760 * CAP_FACTOR / 1000.0   # 9.8112 TWh per unit-year

LAM = 2.5            # cost exponent
K_MATURE = 0.9       # capability reference: the mobilization-era programme
HIATUS = 14          # years, Civaux-2 (1991-4) to Olkiluoto-3 (2005-8), RDS-2
RESTART_RATIO = 4.0  # first post-hiatus projects: ~4x original estimates (NAO 2026)
PAIR_EFFECT = 0.15   # second unit of a pair ~15% cheaper (NEA 7530)

T0 = 6.0             # build years at the mature reference
MU = 3.0             # duration elongation with lost capability

LIFE = 45            # unit life in years from completion
LIFE_EXT = 55        # with lifetime extension (retention, continuity, expansion)

ESTIMATE_BIAS = 0.75   # engineering estimates see this fraction of true cost;
                       # documented optimism, milder than Olkiluoto-3's
CONGESTION = 0.15      # crash-pace premium per unit ordered above 3 a year;
                       # supply chains congest when a continent orders in bursts

# money: 1.0 = one mature-programme unit. Operating costs per TWh.
NUCLEAR_OPEX = 0.004     # ~ EUR 12/MWh against a EUR 3bn unit
FOSSIL_COST = 0.020      # fuel plus carbon plus health, ~ EUR 60/MWh all-in
SHOCK_PREMIUM = 0.060    # extra fossil cost per TWh in a shock year, per severity
SHOCK_YEARS = (2022, 2023)
COHORT_WINDOW = 10       # a vintage cohort: completions within a ten-year window
COMMON_MODE = 0.5        # a common-mode fault takes half the largest cohort
                         # offline for the first shock year

HYDRO_TWH = 350.0


def calibrate():
    """Solve the forgetting and learning rates from the two documented anchors.

    Anchor 1: starting at K_MATURE, fourteen idle years leave capability K_h
    with C(K_h) = 4, so K_h = K_MATURE - ln(4)/LAM and the annual decay rate
    follows from (1 - delta)^14 = K_h / K_MATURE.

    Anchor 2: at K_h, completing one unit teaches eta * (1 - K_h), and the
    next unit is 15% cheaper: exp(-LAM * eta * (1 - K_h)) = 0.85.
    """
    k_h = K_MATURE - np.log(RESTART_RATIO) / LAM
    delta = 1.0 - (k_h / K_MATURE) ** (1.0 / HIATUS)
    eta = np.log(1.0 / (1.0 - PAIR_EFFECT)) / (LAM * (1.0 - k_h))
    return float(delta), float(eta), float(k_h)


DELTA, ETA, K_HIATUS = calibrate()


def unit_cost(k: float) -> float:
    return float(np.exp(LAM * (K_MATURE - min(k, 1.0))))


def build_years(k: float) -> float:
    return T0 * (1.0 + MU * max(0.0, K_MATURE - min(k, 1.0)) / K_MATURE)


def spend_rate(s: float, k: float) -> float:
    congest = 1.0 + CONGESTION * max(0.0, s - 3.0)
    return s * unit_cost(k) * congest


def demand(year: np.ndarray) -> np.ndarray:
    return 1000.0 + 1800.0 / (1.0 + np.exp(-(year - 1990) / 9.0))


def renewables(year: np.ndarray, t_mid: float = 2018.0) -> np.ndarray:
    return 900.0 / (1.0 + np.exp(-(year - t_mid) / 5.0))


def largest_cohort_share(fleet) -> float:
    total = sum(a for _, a in fleet)
    if total <= 1e-9:
        return 0.0
    best = 0.0
    for w0 in range(Y0, Y1):
        share = sum(a for y, a in fleet if w0 <= y < w0 + COHORT_WINDOW) / total
        best = max(best, share)
    return best


# ---------------------------------------------------------------------------
# the simulator
# ---------------------------------------------------------------------------

def simulate(order_rate, *, life: int = LIFE, k0: float = 0.9,
             early_closure: tuple | None = None,
             t_mid: float = 2018.0, shock_severity: float = 1.0,
             fossil_cost: float = FOSSIL_COST):
    """Run the fluid model over 1955-2040.

    The model opens in 1955 with k0 = 0.9: the capability the national
    laboratories, military programmes and demonstration plants of the late
    1940s and 1950s had already assembled (Calder Hall connected in 1956).
    Opening cold instead would push the first completions two decades late
    and bunch the whole build history.

    order_rate: callable year -> units started that year (fractional allowed).
    early_closure: (year, fraction of fleet closed permanently) or None.
    In the first shock year a common-mode fault takes COMMON_MODE of the
    largest vintage cohort offline; the lost output lands on fossil at the
    shocked price. Returns yearly arrays plus totals over 1973-2040.
    """
    k = k0
    fleet = []            # [completion_year, amount]
    pipeline = []         # [completion_year, amount]

    K = np.zeros(N_YEARS)
    starts = np.zeros(N_YEARS)
    completions = np.zeros(N_YEARS)
    output = np.zeros(N_YEARS)
    fossil = np.zeros(N_YEARS)
    surplus = np.zeros(N_YEARS)
    build_spend = np.zeros(N_YEARS)
    cost_ratio = np.zeros(N_YEARS)     # cost of a unit started this year

    dem = demand(YEARS)
    ren = renewables(YEARS, t_mid)
    snapshot_2022 = []
    avail_2022 = 1.0

    for i, year in enumerate(YEARS):
        done = [p for p in pipeline if p[0] <= year]
        pipeline = [p for p in pipeline if p[0] > year]
        for cy, amt in done:
            completions[i] += amt
            fleet.append([year, amt])
            k = k + ETA * amt * (1.0 - k)
        k = k * (1.0 - DELTA)
        k = min(max(k, 0.02), 1.0)
        K[i] = k

        s = float(order_rate(year))
        starts[i] = s
        cost_ratio[i] = unit_cost(k)
        if s > 0:
            pipeline.append([year + build_years(k), s])
            build_spend[i] = spend_rate(s, k)

        fleet = [f for f in fleet if year - f[0] < life]
        if early_closure is not None and year == early_closure[0]:
            frac = early_closure[1]
            for f in fleet:
                f[1] *= (1.0 - frac)

        n_units = sum(f[1] for f in fleet)
        avail = 1.0
        if year == SHOCK_YEARS[0]:
            snapshot_2022 = [(int(f[0]), float(f[1])) for f in fleet]
            share = largest_cohort_share(fleet)
            avail = 1.0 - COMMON_MODE * share * min(shock_severity, 1.0)
            avail_2022 = avail
        output[i] = n_units * TWH_PER_UNIT * avail
        residual = dem[i] - HYDRO_TWH - ren[i] - output[i]
        fossil[i] = max(0.0, residual)
        surplus[i] = max(0.0, -residual)

    w = YEARS >= 1973
    shock_extra = 0.0
    for sy in SHOCK_YEARS:
        j = sy - Y0
        shock_extra += fossil[j] * SHOCK_PREMIUM * shock_severity
    totals = {
        "build": float(build_spend[w].sum()),
        "nuclear_opex": float((output[w] * NUCLEAR_OPEX).sum()),
        "fossil": float((fossil[w] * fossil_cost).sum()),
        "shock": float(shock_extra),
        "cumulative_fossil_twh": float(fossil[w].sum()),
        "curtailed_twh": float(surplus[w].sum()),
    }
    totals["total"] = (totals["build"] + totals["nuclear_opex"]
                       + totals["fossil"] + totals["shock"])
    return {"K": K, "starts": starts, "completions": completions,
            "output": output, "fossil": fossil, "cost_ratio": cost_ratio,
            "build_spend": build_spend, "fleet_2022": snapshot_2022,
            "availability_2022": avail_2022, "totals": totals}


# ---------------------------------------------------------------------------
# order schedules: the observed shape and its counterfactuals
# ---------------------------------------------------------------------------

def orders_observed(year: float) -> float:
    """Early programmes, oil-shock mobilization, the pre-Chernobyl collapse to
    a trickle, the hiatus, two restart probes, and a late revival attempt."""
    if 1955 <= year <= 1972:
        return 1.5
    if 1973 <= year <= 1981:
        return 6.0
    if 1982 <= year <= 1990:
        return 0.75
    if year in (2005, 2007):
        return 1.0
    if year >= 2028:
        return 1.0
    return 0.0


def make_orders_continuity(floor: float = 2.0):
    def orders(year: float) -> float:
        base = orders_observed(year)
        if year >= 1982:
            return max(base, floor)
        return base
    return orders


def orders_expansion(year: float) -> float:
    if 1955 <= year <= 1972:
        return 1.5
    if 1973 <= year <= 2000:
        return 6.0
    if year > 2000:
        return 3.0
    return 0.0


SCENARIOS = {
    "observed":  dict(order_rate=orders_observed, life=LIFE,
                      early_closure=(2011, 0.2)),
    "retention": dict(order_rate=orders_observed, life=LIFE_EXT,
                      early_closure=None),
    "continuity": dict(order_rate=make_orders_continuity(), life=LIFE_EXT,
                       early_closure=None),
    "expansion": dict(order_rate=orders_expansion, life=LIFE_EXT,
                      early_closure=None),
}


# ---------------------------------------------------------------------------
# analyses
# ---------------------------------------------------------------------------

def analysis_stock_flow(runs):
    """The illusion: output holds near its peak for decades after orders stop,
    while capability decays underneath it. All from the observed run."""
    r = runs["observed"]
    starts, output, K, comp = r["starts"], r["output"], r["K"], r["completions"]
    mob_peak = starts.max()
    below = np.where((YEARS >= 1975) & (starts < 0.25 * mob_peak))[0]
    order_stop = int(YEARS[below[0]])
    peak_i = int(np.argmax(output))
    peak_year = int(YEARS[peak_i])
    peak = float(output[peak_i])
    plateau = np.where(output >= 0.95 * peak)[0]
    plateau_end_i = int(plateau[-1])
    plateau_end = int(YEARS[plateau_end_i])
    k_mature = float(K.max())
    k_at_peak = float(K[peak_i])
    k_at_plateau_end = float(K[plateau_end_i])
    pre_probe = np.where((YEARS <= 2004) & (comp > 0.01))[0]
    construction_stop = int(YEARS[pre_probe[-1]])
    peak_k_i = int(np.argmax(K))
    after = np.where((np.arange(N_YEARS) > peak_k_i) & (K < 0.5 * k_mature))[0]
    cap_stop = int(YEARS[after[0]])
    j05 = 2005 - Y0
    j90 = 1990 - Y0
    return {
        "order_stop_year": order_stop,
        "output_peak_year": peak_year,
        "output_peak_twh": round(peak, 6),
        "stock_flow_lag_years": peak_year - order_stop,
        "plateau_end_year": plateau_end,
        "illusion_window_years": plateau_end - order_stop,
        "k_mature": round(k_mature, 6),
        "k_at_output_peak": round(k_at_peak, 6),
        "k_at_peak_over_k_mature": round(k_at_peak / k_mature, 6),
        "k_at_plateau_end": round(k_at_plateau_end, 6),
        "k_at_plateau_end_over_k_mature": round(k_at_plateau_end / k_mature, 6),
        "last_trickle_unit_cost_1990": round(float(r["cost_ratio"][j90]), 6),
        "emergent_restart_cost_2005": round(float(r["cost_ratio"][j05]), 6),
        "five_stops": {
            "order_stop": order_stop,
            "construction_stop_last_completion": construction_stop,
            "capability_stop_half_mature": cap_stop,
            "asset_stop_early_closure": 2011,
            "output_decline_after": plateau_end,
        },
    }


def _run_freeze(freeze_years: float, tolerance: float, probe_interval: int = 8,
                horizon: int = 90, build_rate: float = 2.0):
    """The ratchet experiment. A mature programme goes idle for freeze_years
    (orders and completions both; the freeze is measured from the last
    completion, matching how the decay rate was calibrated). Afterward a
    cost-reading chooser orders at the replacement rate whenever the
    engineering estimate for a new unit, ESTIMATE_BIAS times the true current
    cost, is within tolerance. When ordering is blocked it launches one
    exploratory unit every probe_interval years; the probe realizes the full
    current cost when it completes. A decision to build is a decision to run a
    programme: once ordering starts it is committed for ten years before the
    estimate is consulted again, which is how real programmes survive the
    completion lag their own restart creates. Locked versus recovered is read
    off terminal capability."""
    k = K_MATURE
    pipeline = []   # [completion_time, amount, cost_at_start]
    kk, cc, oo = [], [], []
    probes = []
    last_probe = -10**6
    programme_until = -10**6
    for t in range(horizon):
        done = [p for p in pipeline if p[0] <= t]
        pipeline = [p for p in pipeline if p[0] > t]
        for _, amt, c_start in done:
            k = k + ETA * amt * (1.0 - k)
        k *= (1.0 - DELTA)
        k = min(max(k, 0.02), 1.0)
        s = 0.0
        if t >= freeze_years:
            estimate = ESTIMATE_BIAS * unit_cost(k)
            if t < programme_until:
                s = build_rate
            elif estimate <= tolerance:
                s = build_rate
                programme_until = t + 10
            elif t - last_probe >= probe_interval:
                s = 1.0
                last_probe = t
                probes.append((t, unit_cost(k)))
            if s > 0:
                pipeline.append([t + build_years(k), s, unit_cost(k)])
        kk.append(k); cc.append(unit_cost(k)); oo.append(s)
    recovered = bool(kk[-1] > 0.5)
    return {"recovered": recovered, "k_end": kk[-1], "K": kk, "cost": cc,
            "orders": oo, "probes": probes}


def analysis_ratchet():
    """The critical freeze duration, and the trap that keeps confirming itself."""
    tolerance = 1.8
    outcomes = {}
    g_star = None
    for g in range(1, 25):
        r = _run_freeze(g, tolerance)
        outcomes[g] = r["recovered"]
        if g_star is None and not r["recovered"]:
            g_star = g
    tol_grid = [1.2, 1.5, 1.8, 2.2, 2.6, 3.0]
    g_grid = list(range(1, 21))
    regime = []
    for tol in tol_grid:
        regime.append([bool(_run_freeze(g, tol)["recovered"]) for g in g_grid])
    g_star_by_tol = {}
    for tol, row in zip(tol_grid, regime):
        gs = next((g for g, rec in zip(g_grid, row) if not rec), None)
        g_star_by_tol[str(tol)] = gs
    short = _run_freeze(3, tolerance)
    long_ = _run_freeze(HIATUS, tolerance)
    probe_costs = [round(c, 6) for _, c in long_["probes"]]
    return {
        "tolerance": tolerance,
        "critical_freeze_years": g_star,
        "recovered_by_freeze": {str(g): v for g, v in outcomes.items()},
        "regime_tolerances": tol_grid,
        "regime_freezes": g_grid,
        "regime_recovered": regime,
        "critical_freeze_by_tolerance": g_star_by_tol,
        "short_freeze_example": {"freeze": 3, "recovered": short["recovered"],
                                 "k_end": round(short["k_end"], 6)},
        "long_freeze_example": {"freeze": HIATUS, "recovered": long_["recovered"],
                                "k_end": round(long_["k_end"], 6),
                                "probe_costs": probe_costs,
                                "n_probes": len(probe_costs)},
        "trajectories": {
            "short": {"K": [round(x, 6) for x in short["K"]],
                      "cost": [round(x, 6) for x in short["cost"]]},
            "long": {"K": [round(x, 6) for x in long_["K"]],
                     "cost": [round(x, 6) for x in long_["cost"]]},
        },
    }


def _recovery_years(freeze: int, *, learn_at_start: bool = False,
                    horizon: int = 150) -> int | None:
    """Force ordering at the mobilization rate after the freeze (the political
    constraint is assumed away; someone pays whatever units cost) and count
    the years from restart until a newly started unit prices within 10% of
    the mature cost. With learn_at_start, learning arrives when a unit is
    ordered rather than when it completes; the comparison isolates the
    completion lag as the source of the asymmetry."""
    k = K_MATURE
    target = 1.10
    pipeline = []
    rate = 6.0
    for t in range(horizon):
        done = [p for p in pipeline if p[0] <= t]
        pipeline = [p for p in pipeline if p[0] > t]
        if not learn_at_start:
            for _, amt in done:
                k = k + ETA * amt * (1.0 - k)
        k *= (1.0 - DELTA)
        k = min(max(k, 0.02), 1.0)
        if t >= freeze:
            if unit_cost(k) <= target:
                return t - freeze
            if learn_at_start:
                k = k + ETA * rate * (1.0 - k)
            pipeline.append([t + build_years(k), rate])
    return None


def analysis_hysteresis():
    """Losing is instantaneous, buying back is lagged: the loop is asymmetric
    because forgetting starts the day orders stop, while the learning that
    would repair it arrives only when the first slow, expensive unit is done."""
    rows = []
    for g in [7, 10, 14, 18]:
        rec = _recovery_years(g)
        rec_ls = _recovery_years(g, learn_at_start=True)
        rows.append({"freeze_years": g, "recovery_years": rec,
                     "recovery_years_if_learning_at_start": rec_ls,
                     "asymmetry": round(rec / g, 6) if rec else None})
    base = next(r for r in rows if r["freeze_years"] == HIATUS)
    return {
        "rows": rows,
        "freeze_14": base,
        "asymmetry_at_14": base["asymmetry"],
        "mechanism_check": {
            "learning_at_completion": base["recovery_years"],
            "learning_at_start": base["recovery_years_if_learning_at_start"],
        },
    }


def analysis_counterfactuals(runs):
    out = {}
    for name, r in runs.items():
        t = dict(r["totals"])
        j22 = 2022 - Y0
        j23 = 2023 - Y0
        t["fossil_twh_2022"] = round(float(r["fossil"][j22]), 6)
        t["nuclear_twh_2022"] = round(float(r["output"][j22]), 6)
        t["k_2022"] = round(float(r["K"][j22]), 6)
        t["next_unit_cost_2023"] = round(float(r["cost_ratio"][j23]), 6)
        t["availability_2022"] = round(float(r["availability_2022"]), 6)
        for key in ("build", "nuclear_opex", "fossil", "shock", "total",
                    "cumulative_fossil_twh", "curtailed_twh"):
            t[key] = round(t[key], 6)
        out[name] = t
    out["ordering"] = {
        "cumulative_fossil": sorted(SCENARIOS, key=lambda s: out[s]["cumulative_fossil_twh"]),
        "total_cost": sorted(SCENARIOS, key=lambda s: out[s]["total"]),
    }
    out["continuity_vs_retention"] = {
        "extra_build": round(out["continuity"]["build"] - out["retention"]["build"], 6),
        "fossil_saved_twh": round(out["retention"]["cumulative_fossil_twh"]
                                  - out["continuity"]["cumulative_fossil_twh"], 6),
        "total_advantage": round(out["retention"]["total"] - out["continuity"]["total"], 6),
        "restart_cost_2023_retention": out["retention"]["next_unit_cost_2023"],
        "restart_cost_2023_continuity": out["continuity"]["next_unit_cost_2023"],
    }
    # derived quantities quoted in prose (computed from the totals above)
    obs = out["observed"]["total"]
    out["savings_vs_observed"] = {
        "retention": round(obs - out["retention"]["total"], 6),
        "retention_fraction": round((obs - out["retention"]["total"]) / obs, 6),
        "continuity": round(obs - out["continuity"]["total"], 6),
        "continuity_fraction": round((obs - out["continuity"]["total"]) / obs, 6),
    }
    out["fault_output_loss_2022"] = {
        name: round(1.0 - out[name]["availability_2022"], 6) for name in SCENARIOS}
    return out


def analysis_regimes():
    """Where the thesis fails. Sweep the renewables arrival, the price the
    world puts on fossil externalities, and whether the 2022-style shock
    happens at all; ask whether the replacement sequence (continuity) beats
    retention alone on total cost. A separate scan asks from which externality
    price upward crash expansion overtakes continuity."""
    speeds = {"fast": 2012.0, "observed": 2018.0, "slow": 2024.0}
    damage_mults = [0.25, 0.5, 1.0, 1.5]
    severities = [0.0, 1.0]
    grid = []
    holds = 0
    for sev in severities:
        for sname, tmid in speeds.items():
            for dm in damage_mults:
                fc = FOSSIL_COST * dm
                rr = simulate(**SCENARIOS["retention"], t_mid=tmid,
                              fossil_cost=fc, shock_severity=sev)
                cc = simulate(**SCENARIOS["continuity"], t_mid=tmid,
                              fossil_cost=fc, shock_severity=sev)
                adv = rr["totals"]["total"] - cc["totals"]["total"]
                grid.append({"shock": sev, "renewables": sname,
                             "damage_mult": dm,
                             "continuity_advantage": round(adv, 6),
                             "holds": bool(adv > 0)})
                holds += adv > 0
    expansion_scan = []
    expansion_cross = None
    for dm in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
        fc = FOSSIL_COST * dm
        ee = simulate(**SCENARIOS["expansion"], fossil_cost=fc)
        cc = simulate(**SCENARIOS["continuity"], fossil_cost=fc)
        margin = cc["totals"]["total"] - ee["totals"]["total"]
        expansion_scan.append({"damage_mult": dm,
                               "expansion_margin": round(margin, 6),
                               "expansion_wins": bool(margin > 0)})
        if expansion_cross is None and margin > 0:
            expansion_cross = dm
    first_failure = next((g for g in grid if not g["holds"]), None)
    return {"grid": grid, "cells": len(grid), "holds_in": int(holds),
            "first_failure": first_failure,
            "expansion_scan": expansion_scan,
            "expansion_overtakes_at_damage_mult": expansion_cross}


def _country_welfare(s_own: float, s_others: float, sigma: float,
                     n_countries: int = 8) -> float:
    """Reduced-form national welfare over 1982-2040 when this country orders
    s_own units a year and every other country orders s_others. Capability has
    a continental component (driven by everyone's building) and a national one
    (driven by one's own); sigma is the continental share. Returns minus cost."""
    total_rate = s_own + (n_countries - 1) * s_others

    def orders_total(year):
        return orders_observed(year) if year < 1982 else total_rate

    def orders_own(year):
        return orders_observed(year) / n_countries if year < 1982 else s_own

    r_eu = simulate(orders_total, life=LIFE_EXT)

    k = 0.9
    pipeline = []
    k_nat = np.zeros(N_YEARS)
    for i, year in enumerate(YEARS):
        done = [p for p in pipeline if p[0] <= year]
        pipeline = [p for p in pipeline if p[0] > year]
        for _, amt in done:
            k = k + ETA * amt * (1.0 - k)
        k *= (1.0 - DELTA)
        k = min(max(k, 0.02), 1.0)
        s = orders_own(year)
        if s > 0:
            pipeline.append([year + build_years(k), s])
        k_nat[i] = k

    k_eff = sigma * r_eu["K"] + (1.0 - sigma) * k_nat
    dem = demand(YEARS) / n_countries
    ren = renewables(YEARS) / n_countries
    hydro = HYDRO_TWH / n_countries

    fleet = []
    pipeline = []
    cost = 0.0
    for i, year in enumerate(YEARS):
        done = [p for p in pipeline if p[0] <= year]
        pipeline = [p for p in pipeline if p[0] > year]
        for _, amt in done:
            fleet.append([year, amt])
        s = orders_own(year)
        if s > 0:
            pipeline.append([year + build_years(k_eff[i]), s])
            if year >= 1973:
                cost += s * unit_cost(k_eff[i])
        fleet = [f for f in fleet if year - f[0] < LIFE_EXT]
        n_units = sum(f[1] for f in fleet)
        out = n_units * TWH_PER_UNIT
        fossil = max(0.0, dem[i] - hydro - ren[i] - out)
        if year >= 1973:
            cost += out * NUCLEAR_OPEX + fossil * FOSSIL_COST
            if year in SHOCK_YEARS:
                cost += fossil * SHOCK_PREMIUM
    return -cost


def analysis_coordination():
    """The Euratom paradox as a number: with a continental capability share,
    the symmetric Nash order rate sits below the planner's."""
    s_grid = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.35, 0.5]
    sigmas = [0.0, 0.25, 0.5, 0.75, 1.0]
    curve = []
    for sigma in sigmas:
        planner_s, planner_w = None, -np.inf
        for s in s_grid:
            w = _country_welfare(s, s, sigma)
            if w > planner_w:
                planner_w, planner_s = w, s
        nash_s = None
        for s_bar in s_grid:
            br, brw = None, -np.inf
            for s in s_grid:
                w = _country_welfare(s, s_bar, sigma)
                if w > brw:
                    brw, br = w, s
            if br == s_bar:
                nash_s = s_bar
                break
        curve.append({"sigma": sigma, "planner_rate": planner_s,
                      "nash_rate": nash_s,
                      "wedge": None if nash_s is None
                      else round((planner_s or 0) - nash_s, 6)})
    base = next(c for c in curve if c["sigma"] == 0.75)
    return {"curve": curve, "per_country_grid": s_grid,
            "n_countries": 8, "base_sigma": 0.75,
            "planner_rate_at_base": base["planner_rate"],
            "nash_rate_at_base": base["nash_rate"],
            "planner_rate_continental_at_base": round(base["planner_rate"] * 8, 6),
            "nash_rate_continental_at_base": round(base["nash_rate"] * 8, 6),
            "wedge_at_base": base["wedge"],
            "planner_rate_continental_at_half": round(
                next(c for c in curve if c["sigma"] == 0.5)["planner_rate"] * 8, 6),
            "nash_rate_continental_at_half": round(
                (next(c for c in curve if c["sigma"] == 0.5)["nash_rate"] or 0) * 8, 6)}


def analysis_vintage(runs):
    """The caveat as a number: a fleet built in a burst concentrates its
    vintages, so one common-mode fault reaches most of it at once."""
    out = {}
    for name in ("observed", "continuity"):
        share = largest_cohort_share(runs[name]["fleet_2022"])
        out[name] = {"largest_cohort_share": round(share, 6),
                     "availability_2022": round(runs[name]["availability_2022"], 6)}
    out["concentration_ratio"] = round(
        out["observed"]["largest_cohort_share"]
        / out["continuity"]["largest_cohort_share"], 6)
    return out


# ---------------------------------------------------------------------------
# invariants
# ---------------------------------------------------------------------------

def run_checks(res) -> dict:
    checks = {}
    cal = res["calibration"]
    checks["calibration_hiatus_hits_anchor"] = abs(cal["cost_ratio_after_hiatus"] - RESTART_RATIO) < 0.01
    checks["calibration_pair_hits_anchor"] = abs(cal["pair_effect_check"] - PAIR_EFFECT) < 0.01
    sf = res["stock_flow"]
    checks["stock_flow_lag_over_decade"] = sf["stock_flow_lag_years"] >= 12
    checks["capability_gone_before_output_declines"] = (
        sf["k_at_plateau_end_over_k_mature"] < 0.55
        and sf["k_at_peak_over_k_mature"] < 0.85)
    ra = res["ratchet"]
    checks["ratchet_exists"] = ra["critical_freeze_years"] is not None and \
        ra["short_freeze_example"]["recovered"] and not ra["long_freeze_example"]["recovered"]
    rec = [ra["recovered_by_freeze"][str(g)] for g in range(1, 25)]
    checks["ratchet_monotone"] = all(not a or b for a, b in zip(rec[1:], rec[:-1]))
    checks["trap_self_validates"] = all(c > ra["tolerance"]
                                        for c in ra["long_freeze_example"]["probe_costs"]) and \
        ra["long_freeze_example"]["n_probes"] >= 2
    hy = res["hysteresis"]
    checks["hysteresis_asymmetric"] = hy["asymmetry_at_14"] is not None and hy["asymmetry_at_14"] > 1.2
    checks["completion_lag_is_the_mechanism"] = (
        hy["mechanism_check"]["learning_at_start"] is not None
        and hy["mechanism_check"]["learning_at_start"] < hy["mechanism_check"]["learning_at_completion"])
    cf = res["counterfactuals"]
    checks["fossil_ordering"] = (cf["expansion"]["cumulative_fossil_twh"]
                                 <= cf["continuity"]["cumulative_fossil_twh"]
                                 <= cf["retention"]["cumulative_fossil_twh"]
                                 <= cf["observed"]["cumulative_fossil_twh"])
    checks["continuity_beats_retention_and_observed"] = (
        cf["continuity"]["total"] < cf["retention"]["total"] < cf["observed"]["total"])
    checks["continuity_preserves_option"] = (cf["continuity"]["next_unit_cost_2023"]
                                             < cf["retention"]["next_unit_cost_2023"] - 0.5)
    rg = res["regimes"]
    checks["thesis_fails_somewhere"] = rg["holds_in"] < rg["cells"]
    checks["thesis_holds_mostly"] = rg["holds_in"] >= rg["cells"] * 0.6
    checks["expansion_margin_fragile"] = (
        rg["expansion_overtakes_at_damage_mult"] is not None
        and rg["expansion_overtakes_at_damage_mult"] >= 0.75
        and not rg["expansion_scan"][0]["expansion_wins"])
    co = res["coordination"]
    checks["no_wedge_without_spillover"] = co["curve"][0]["wedge"] == 0.0
    checks["wedge_at_base_positive"] = co["wedge_at_base"] is not None and co["wedge_at_base"] > 0
    vi = res["vintage"]
    checks["burst_concentrates_vintage"] = vi["concentration_ratio"] > 1.5
    return checks


# ---------------------------------------------------------------------------
# entry
# ---------------------------------------------------------------------------

def run() -> dict:
    k = K_MATURE
    for _ in range(HIATUS):
        k *= (1.0 - DELTA)
    pair_next = 1.0 - np.exp(-LAM * ETA * (1.0 - K_HIATUS))
    calibration = {
        "lam": LAM, "k_mature": K_MATURE, "delta": round(DELTA, 6),
        "eta": round(ETA, 6), "k_after_hiatus": round(k, 6),
        "cost_ratio_after_hiatus": round(unit_cost(k), 6),
        "pair_effect_check": round(float(pair_next), 6),
        "estimate_bias": ESTIMATE_BIAS, "congestion": CONGESTION,
        "build_years_at_mature": round(build_years(K_MATURE), 6),
        "build_years_after_hiatus": round(build_years(K_HIATUS), 6),
        "anchors": {
            "hiatus_years": HIATUS, "restart_cost_ratio": RESTART_RATIO,
            "pair_effect": PAIR_EFFECT,
            "provenance": "IAEA RDS-2 (Civaux-2 1991-4, Olkiluoto-3 2005-8); "
                          "NAO 2026 HC 33 (four times original estimates); "
                          "NEA 7530 (second unit of a pair ~15% cheaper)",
        },
    }
    runs = {name: simulate(**kw) for name, kw in SCENARIOS.items()}
    res = {
        "calibration": calibration,
        "stock_flow": analysis_stock_flow(runs),
        "ratchet": analysis_ratchet(),
        "hysteresis": analysis_hysteresis(),
        "counterfactuals": analysis_counterfactuals(runs),
        "regimes": analysis_regimes(),
        "coordination": analysis_coordination(),
        "vintage": analysis_vintage(runs),
        "cited_record": {
            "note": "values quoted in prose from verified external sources "
                    "(see sources.md); listed here so the claims gate can "
                    "reconcile them; none is a model output",
            "jarvis_deschenes_jha_2022": {
                "nuclear_twh_lost_per_year": 57.6, "hard_coal_twh": 16.7,
                "lignite_twh": 7.6, "gas_twh": 4.9, "oil_twh": 1.2,
                "net_imports_twh": 10.6, "wind_solar_twh": 16.5,
                "co2_mt_per_year": 26.2, "excess_deaths_per_year": 799.8,
                "social_cost_bn_eur_low": 3, "social_cost_bn_eur_high": 8},
            "flamanville_cost_bn_eur_2023": 23.7,
            "ol3_planned_cost_bn_eur": 3.2, "ol3_over_budget_bn_eur_2017": 5.3,
            "eurostat": {"peak_twh_2004": 928.438, "twh_2024": 649.524,
                         "share_2024_pct": 23.3, "decline_2006_2024_pct": 29},
            "rte_2022": {"availability_pct": 54, "availability_2015_2019_pct": 73,
                         "output_twh": 279, "drop_twh": 81.7,
                         "net_imports_twh": 16.5},
            "iea_2021_russian_gas": {"bcm": 155, "share_of_imports_pct": 45,
                                     "share_of_consumption_pct": 40},
            "ipcc_ar6_cost_declines_pct": {"solar": 85, "wind": 55,
                                           "batteries": 85},
        },
    }
    res["checks"] = run_checks(res)
    failed = [k for k, v in res["checks"].items() if not v]
    if failed:
        import json as _json
        print(_json.dumps({k: v for k, v in res["checks"].items()}, indent=2))
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run()["checks"], indent=2))
