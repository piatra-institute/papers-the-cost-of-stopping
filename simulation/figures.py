"""Figures for *The Cost of Stopping*. Each reads the results dict and writes one PNG.

Scenario palette (stack order, CVD-checked): expansion amber, continuity green,
retention blue, observed warm gray; line styles differ so identity never rides
on hue alone. Diverging map for the regime grid runs red to green through a
neutral midpoint.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

INK = "#1a1a1a"
GRID = "#d9d9d9"
COL = {"observed": "#57534e", "retention": "#2563eb",
       "continuity": "#15803d", "expansion": "#b45309"}
STYLE = {"observed": "-", "retention": "--", "continuity": "-", "expansion": ":"}
LABEL = {"observed": "observed", "retention": "retention only",
         "continuity": "minimum continuity", "expansion": "crash expansion"}
ORDER = ["observed", "retention", "continuity", "expansion"]
DIVERGE = LinearSegmentedColormap.from_list(
    "adv", ["#b3202c", "#f0efed", "#15803d"])


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_stock_flow(res: dict, runs: dict, years, path: str) -> None:
    """Three clocks that do not agree: orders, output, capability."""
    sf = res["stock_flow"]
    r = runs["observed"]
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(8.6, 6.4), sharex=True)

    a1.bar(years, r["starts"], color="#57534e", width=0.85)
    a1.set_ylabel("starts / year", fontsize=8.5)
    a1.axvline(sf["order_stop_year"], color=INK, lw=0.9, ls="--")
    a1.text(sf["order_stop_year"] + 0.8, 4.6, f"orders stop {sf['order_stop_year']}",
            fontsize=8, color=INK)
    a1.set_title("construction starts", fontsize=10, color=INK, loc="left")

    a2.plot(years, r["output"], color="#2563eb", lw=1.8)
    a2.axvspan(sf["order_stop_year"], sf["plateau_end_year"],
               color="#2563eb", alpha=0.08)
    a2.set_ylabel("output (TWh)", fontsize=8.5)
    a2.axvline(sf["output_peak_year"], color=INK, lw=0.9, ls="--")
    a2.text(sf["output_peak_year"] + 0.8, 200,
            f"peak {sf['output_peak_year']}, plateau to {sf['plateau_end_year']}",
            fontsize=8, color=INK)
    a2.set_title(f"nuclear generation ({sf['illusion_window_years']}-year plateau "
                 "after orders stop)", fontsize=10, color=INK, loc="left")

    a3.plot(years, r["K"], color="#b3202c", lw=1.8)
    a3.set_ylabel("capability K", fontsize=8.5)
    a3.set_ylim(0, 1.0)
    a3.axhline(0.5 * sf["k_mature"], color=INK, lw=0.9, ls="--")
    a3.text(2024, 0.5 * sf["k_mature"] + 0.04, "half the mobilization level",
            fontsize=8, color=INK)
    a3.set_title("capability stock",
                 fontsize=10, color=INK, loc="left")
    a3.set_xlabel("year", fontsize=9)
    for ax in (a1, a2, a3):
        _style(ax)
    a1.grid(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_ratchet(res: dict, path: str) -> None:
    ra = res["ratchet"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.8))

    t = np.arange(len(ra["trajectories"]["short"]["cost"]))
    a1.plot(t, ra["trajectories"]["short"]["cost"], color="#15803d", lw=1.8,
            label=f"{ra['short_freeze_example']['freeze']}-year freeze: recovers")
    a1.plot(t, ra["trajectories"]["long"]["cost"], color="#b3202c", lw=1.8,
            label=f"{ra['long_freeze_example']['freeze']}-year freeze: locks")
    a1.axhline(ra["tolerance"], color=INK, lw=0.9, ls="--")
    a1.text(1, ra["tolerance"] + 0.12, "tolerance", fontsize=8, color=INK)
    a1.set_xlabel("years", fontsize=9)
    a1.set_ylabel("cost of the next unit (mature = 1)", fontsize=9)
    a1.set_title("next-unit cost after 3- and 14-year freezes", fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="center right")

    tols = [float(x) for x in ra["critical_freeze_by_tolerance"].keys()]
    gs = [g if g is not None else 21 for g in ra["critical_freeze_by_tolerance"].values()]
    a2.step(tols, gs, where="mid", color="#2563eb", lw=1.8)
    a2.plot(tols, gs, "o", color="#2563eb", ms=5)
    a2.axhline(14, color="#b3202c", lw=1.2, ls="--")
    a2.text(1.22, 14.4, "the documented hiatus: fourteen years",
            fontsize=8.5, color="#b3202c")
    a2.set_xlabel("cost tolerance of the chooser", fontsize=9)
    a2.set_ylabel("critical freeze duration (years)", fontsize=9)
    a2.set_ylim(0, 21)
    a2.set_title("critical freeze length against cost tolerance", fontsize=10, color=INK)
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_hysteresis(res: dict, path: str) -> None:
    hy = res["hysteresis"]
    rows = hy["rows"]
    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    x = np.arange(len(rows))
    w = 0.27
    ax.bar(x - w, [r["freeze_years"] for r in rows], w, color="#57534e",
           label="idle years (the loss)")
    ax.bar(x, [r["recovery_years"] for r in rows], w, color="#b3202c",
           label="rebuild years, learning at completion")
    ax.bar(x + w, [r["recovery_years_if_learning_at_start"] for r in rows], w,
           color="#15803d", label="rebuild years, if learning arrived at order")
    for i, r in enumerate(rows):
        ax.text(i, r["recovery_years"] + 0.5, str(r["recovery_years"]),
                ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r['freeze_years']}-year freeze" for r in rows], fontsize=9)
    ax.set_ylabel("years", fontsize=9)
    ax.set_ylim(0, 31)
    ax.set_title("building years needed against idle years",
                 fontsize=10, color=INK)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_counterfactuals(res: dict, runs: dict, years, path: str) -> None:
    cf = res["counterfactuals"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 3.9),
                                 gridspec_kw={"width_ratios": [1.25, 1]})

    for name in ORDER:
        a1.plot(years, runs[name]["output"], STYLE[name], color=COL[name],
                lw=1.7, label=LABEL[name])
    a1.set_xlabel("year", fontsize=9)
    a1.set_ylabel("nuclear output (TWh)", fontsize=9)
    a1.set_title("nuclear output by scenario", fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8, loc="upper left")

    comps = [("build", "#2563eb", "building"),
             ("nuclear_opex", "#9db8e8", "operating"),
             ("fossil", "#b3202c", "fossil burned"),
             ("shock", "#7f1d1d", "2022 shock")]
    x = np.arange(len(ORDER))
    bottom = np.zeros(len(ORDER))
    for key, col, lab in comps:
        vals = np.array([cf[n][key] for n in ORDER])
        a2.bar(x, vals, 0.6, bottom=bottom, color=col, label=lab,
               edgecolor="white", linewidth=1.2)
        bottom += vals
    for i, n in enumerate(ORDER):
        a2.text(i, bottom[i] + 25, f"{cf[n]['total']:.0f}", ha="center",
                fontsize=8.5, color=INK)
    a2.set_xticks(x)
    a2.set_xticklabels([LABEL[n].replace(" ", "\n") for n in ORDER], fontsize=8)
    a2.set_ylabel("total cost 1973–2040 (mature units)", fontsize=9)
    a2.set_title("total cost by scenario, 1973-2040", fontsize=10, color=INK)
    a2.legend(frameon=False, fontsize=8, loc="upper right")
    for ax in (a1, a2):
        _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_regimes(res: dict, path: str) -> None:
    co = res["coordination"]
    rg = res["regimes"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 3.9),
                                 gridspec_kw={"width_ratios": [1, 1.2]})

    sig = [c["sigma"] for c in co["curve"]]
    a1.plot(sig, [c["planner_rate"] for c in co["curve"]], "o-",
            color="#15803d", lw=1.8, ms=5, label="continental planner")
    a1.plot(sig, [c["nash_rate"] for c in co["curve"]], "s--",
            color="#b3202c", lw=1.8, ms=5, label="national choosers (Nash)")
    a1.set_xlabel("continental share of capability", fontsize=9)
    a1.set_ylabel("per-country order rate (units / year)", fontsize=9)
    a1.set_title("order rates by planner against spillover share",
                 fontsize=10, color=INK)
    a1.legend(frameon=False, fontsize=8.5, loc="upper left")

    rows = [(s, r) for s in (0.0, 1.0) for r in ("fast", "observed", "slow")]
    cols = sorted({g["damage_mult"] for g in rg["grid"]})
    M = np.zeros((len(rows), len(cols)))
    H = np.zeros_like(M, dtype=bool)
    for g in rg["grid"]:
        i = rows.index((g["shock"], g["renewables"]))
        j = cols.index(g["damage_mult"])
        M[i, j] = g["continuity_advantage"]
        H[i, j] = g["holds"]
    lim = float(np.abs(M).max())
    a2.imshow(M, cmap=DIVERGE, vmin=-lim, vmax=lim, aspect="auto")
    for i in range(len(rows)):
        for j in range(len(cols)):
            a2.text(j, i, f"{M[i, j]:+.0f}", ha="center", va="center",
                    fontsize=8, color=INK,
                    fontweight="bold" if not H[i, j] else "normal")
            if not H[i, j]:
                a2.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96,
                                           fill=False, edgecolor="#b3202c",
                                           linewidth=1.6))
    a2.set_xticks(range(len(cols)))
    a2.set_xticklabels([f"{c:g}x" for c in cols], fontsize=8.5)
    a2.set_yticks(range(len(rows)))
    a2.set_yticklabels([f"{'no shock' if s == 0 else 'shock'}, {r} renewables"
                        for s, r in rows], fontsize=8)
    a2.set_xlabel("fossil externality price (multiple of base)", fontsize=9)
    a2.set_title("continuity advantage across regimes",
                 fontsize=10, color=INK)
    a2.grid(False)
    _style(a1)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
