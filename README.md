# The Cost of Stopping

Nuclear Discontinuity, Industrial Forgetting, and Europe's Energy Vulnerability, 1973–2022.

Between the oil shock of 1973 and the gas shock of 2022, Western Europe built the world's largest fleet of low-carbon power plants, stopped building it, lost the ability to build economically, and then attributed the price of that loss to the technology. We treat the retreat as an industrial-capability event and make four claims in descending order of evidential support. Construction starts collapsed between 1979 and 1983, before Chernobyl, which converted an investment slowdown into political lock-in. Stopping comprised five processes on different timescales, and the operating fleet concealed the end of new orders for two decades: EU nuclear output peaked at 928 TWh in 2004. The capability loss was hysteretic: the first projects of the 2005 restart cost roughly 4 times their original estimates, took over seventeen years to build, and were read as evidence that reactors cannot be built economically. And construction anywhere in Europe maintained suppliers, skills and regulatory competence everywhere, while decisions to order or cancel were national. A deterministic model calibrated to the fourteen-year construction hiatus, the fourfold restart premium and a 15% series effect reproduces the record's shape. Output holds near its peak for 28 years after orders stop while capability falls to a third of its mobilization level; a cost-reading decision-maker recovers from an order freeze shorter than 7 years and remains locked from 7 years on; and fourteen idle years take 22 building years to undo. Against the observed path, retaining the closed reactors saves 8% of total system cost, and adding a replacement sequence of two units a year saves 24%, an advantage that holds in 21 of 24 regimes.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build the-cost-of-stopping`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
