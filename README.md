# The Cost of Stopping

Nuclear Discontinuity, Industrial Forgetting, and Europe's Energy Vulnerability, 1973–2022. The paper treats Europe's nuclear retreat as an industrial-capability event: the ability to build reactors economically is a stock that decays when idle and regenerates only through use, and once the retreat is read at that level its chronology, invisibility, price, and self-justification follow from one mechanism. Four claims, in descending order of evidential support: the retreat predates Chernobyl (Western construction starts collapsed by 1983; the accident supplied lock-in); stopping was five processes on five clocks, and the operating fleet concealed the dead order pipeline for two decades while EU output rose to its 2004 peak; the loss was hysteretic, so the 2005 restart arrived at roughly 4 times its estimates and the price was read as a property of the technology; and underneath sat a coordination failure, since the capability was continental while every build decision was national. A deterministic model calibrated to the fourteen-year construction-start hiatus, the fourfold restart premium, and the 15% series effect reproduces the record's shape: output holds its peak for 28 years after orders stop while capability falls to a third; a cost-reading chooser recovers from freezes up to 7 years and locks beyond 13 even tolerating triple cost, and the hiatus was 14; every probe launched inside the trap prices at 4 to 6 times series cost and confirms the stop that caused it; fourteen idle years take 22 building years to undo. A minimum-continuity counterfactual, keeping certified reactors plus a two-unit-a-year replacement sequence, saves 24% of total system cost against the observed path, halves the 2022 exposure, and keeps the option to build at 1.6 times series cost instead of 5.8; the advantage survives 21 of 24 regimes and fails only where fossil externalities are priced near zero and the crisis never comes.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Deterministic, no sampled randomness; a rerun reproduces every number bit for bit. Eighteen invariant checks fail the run loudly if broken, among them: the two calibration anchors round-trip (fourteen idle years price the next unit at 4.0; one completion at that level cuts the next unit by 15%); the ratchet exists and is monotone in freeze length; every probe launched inside the locked state exceeds the chooser's tolerance; the hysteresis asymmetry disappears when learning is moved from completion to order time, isolating the completion lag as the mechanism; continuity beats retention and the observed path at base prices while crash expansion's advantage is confined to high externality prices; and the thesis fails in the stated corner of the regime grid. Historical quantities quoted in prose are carried in `results.json` under `cited_record`, marked as quoted rather than computed, with provenance in `sources.md`.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build the-cost-of-stopping`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
