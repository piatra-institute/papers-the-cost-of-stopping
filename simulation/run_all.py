"""Orchestrator: reproduces every number and all five figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. The model is
deterministic; a rerun reproduces every number bit for bit. A failed
invariant or a failed figure fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run, simulate, SCENARIOS, YEARS

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    runs = {name: simulate(**kw) for name, kw in SCENARIOS.items()}
    from figures import (plot_stock_flow, plot_ratchet, plot_hysteresis,
                         plot_counterfactuals, plot_regimes)
    plot_stock_flow(results, runs, YEARS, str(OUT / "figures" / "stock_flow.png"))
    plot_ratchet(results, str(OUT / "figures" / "ratchet.png"))
    plot_hysteresis(results, str(OUT / "figures" / "hysteresis.png"))
    plot_counterfactuals(results, runs, YEARS, str(OUT / "figures" / "counterfactuals.png"))
    plot_regimes(results, str(OUT / "figures" / "regimes.png"))

    sf = results["stock_flow"]
    print(f"stock-flow: orders stop {sf['order_stop_year']}, output peaks "
          f"{sf['output_peak_year']} (lag {sf['stock_flow_lag_years']}), "
          f"plateau to {sf['plateau_end_year']} "
          f"(illusion window {sf['illusion_window_years']})")
    ra = results["ratchet"]
    print(f"ratchet: critical freeze {ra['critical_freeze_years']} years at "
          f"tolerance {ra['tolerance']}; by tolerance "
          f"{ra['critical_freeze_by_tolerance']}")
    hy = results["hysteresis"]
    print(f"hysteresis: 14 idle years take "
          f"{hy['freeze_14']['recovery_years']} building years to undo "
          f"({hy['mechanism_check']['learning_at_start']} if learning arrived "
          f"at order time)")
    cf = results["counterfactuals"]
    print("scenario totals:", {n: round(cf[n]["total"], 1) for n in SCENARIOS})
    rg = results["regimes"]
    print(f"regimes: continuity beats retention in {rg['holds_in']}/{rg['cells']}; "
          f"first failure {rg['first_failure'] and {k: rg['first_failure'][k] for k in ('shock', 'renewables', 'damage_mult')}}")
    print(f"expansion overtakes continuity from damage multiple "
          f"{rg['expansion_overtakes_at_damage_mult']}")
    co = results["coordination"]
    print(f"coordination: planner {co['planner_rate_at_base']} vs nash "
          f"{co['nash_rate_at_base']} per country at sigma {co['base_sigma']}")
    print("vintage:", results["vintage"])
    print("checks:", all(results["checks"].values()), "-",
          f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
