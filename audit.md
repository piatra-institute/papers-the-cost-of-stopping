# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — prose revision

Prose revised against the house standards. Headings made descriptive (Introduction, Chronology of the retreat, Five processes of stopping, The 2005 restart, Closure order and the German phase-out, The 2022 crisis, A model of a building system, Forgetting, learning and the illusion window, Cost-reading decisions and lock-in, National decisions and continental capability, Four counterfactual order books, Sensitivity and limitations, Conclusion, Reproducibility).
Grid audit: freeze thresholds (7 and 13 years) are on an integer-year freeze grid, which matches the model's annual time step; the crash-expansion comparison over externality prices is now explicitly stated as a grid in quarter steps. No other grid-derived thresholds. results.json unchanged by the figure edits.

## 2026-08-06 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 24 entries verified against Crossref or the publisher's record before citation; JDJ 2022 read first-hand from the author manuscript (the seed's "330–800 deaths" replaced with the published table's 799.8; its NBER-era "1,100+" superseded). Cut from the seed: the unpublished Andersson–Finnegan estimates, an NEA savings triplet not present in the cited document, the unsourced "34% share in the 1990s", and the WNISR chronology (replaced with IAEA RDS-2, where Civaux-2 1991-4 and Olkiluoto-3 2005-8 anchor the fourteen-year hiatus first-hand).
  - Simulation: deterministic capability-stock model; two anchors calibrate the two rates (14 idle years -> 4.0x next-unit cost, per NAO 2026; one completion -> 15% pair effect, per NEA 7530). Design iterations logged: cost normalized to the mature programme; a cold 1955 start bunched the entire build history and was replaced with a documented warm start (k0 = 0.9, Calder Hall era); the ratchet chooser needed programme commitment (annual re-evaluation killed every restart inside its own completion lag) and a probe cooldown (first version probed every year); the regime grid folded the shock axis in after an all-holds grid hid the no-shock failure corner.
  - Honesty items surfaced by the model and kept: crash expansion is cheapest at base externality prices (margin fragile, gone below 0.75x; reported, with the invariant testing fragility rather than forcing a ranking); the model's emergent 2005 restart prices at 3.1 vs the record's 4.0 (design novelty unpriced; stated in the paper); renewables timing moves almost nothing (reported as a finding).
  - Voice: draft came in at 0 errors, 1 review-candidate (a negate-pivot), fixed; seven meta-commentary phrases removed in a dedicated pass ("at the centre of this paper", "worth stating in words", "itself a finding", "on the table", "honest complication", "exists to formalize", "organizes everything that follows"); institutional citations spelled out so the refs matcher reconciles them (the gate skips all-caps tokens in-text).

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 24 in-text keys, 24 bib entries, 0 missing, 0 unused
  - claims: 478 sim values, 23 decimal claims in prose, 0 without a match
  - build: 14 pages, no missing-character warnings
  - simulation: 18/18 invariants
  - check => PASS
