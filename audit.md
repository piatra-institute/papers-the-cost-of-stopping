# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 24 CSL entries. 13 matched in Crossref (title and year) with DOIs; 11 institutional documents entered by hand (nao2017, nao2026, stuk2019, iaea2023, iea2022, eurostat2025, ipcc2022, nea2020 re-fetched or DOI-resolved; cour2025, rte2023, euratom2023 entered from the legacy entries because the documents could not be re-fetched). Organisation ids shortened (iaea2023, iea2022, ipcc2022, nao2017, nao2026, nea2020, stuk2019, rte2023). In-text citations converted to Pandoc [@id]; legacy list replaced by the citeproc list.
- Bibliographic corrections: NAO Hinkley Point C session "2017–2019" -> "2017–18" (report cover); STUK-B 237 title -> "Finnish Report on Nuclear Safety: Finnish 8th National Report as Referred to in Article 5 of the Convention on Nuclear Safety"; Arrow 1962 pages 155 -> 155–173; Escobar Rangel and Lévêque journal name and co-author diacritics restored.
- Numerical correction: "had fallen 29% by 2024" -> "30%": Eurostat's 29% is the 2006–2024 decline; 928 438 -> 649 524 GWh from the 2004 peak is a 30.0% fall.
- Correction: the ratchet threshold. results.json /ratchet/critical_freeze_years = 7 is the shortest freeze that locks (freezes of 1–6 years recover; 7 does not). The prose said the programme recovers from a freeze "of up to 7 years"; abstract, body, metadata and README now say "shorter than 7 years" / "7 years or more ... locks".
- analyses.py: added derived fields computed from existing totals (counterfactuals/savings_vs_observed, counterfactuals/fault_output_loss_2022, coordination/planner_rate_continental_at_half, nash_rate_continental_at_half) so the prose's 176, 8%, 24%, 39% and 2.8 bind to pointers; every pre-existing value is unchanged and the rerun is deterministic.
- claims.yaml: 74 claims (46 computation, 13 source, 5 assumption, 7 interpretation, 2 definition, 1 normative). Source claims checked against re-fetched documents (IEA page, IAEA RDS-2 tables, Eurostat page, NAO HC 40 and HC 33 PDFs, STUK-B 237, IPCC SPM B.4.1) or Crossref/OpenAlex abstracts (Jarvis et al., Benkard, Lovering et al., Escobar Rangel and Lévêque, Davis).
- Unverified, not bound: Jarvis et al. replacement mix (57.6/16.7/7.6/4.9/10.6/16.5 TWh), 26.2 Mt CO2 and ~800 deaths (abstract gives only the €3–8bn cost and the mortality share; the NBER working-paper version reports different figures); Cour des comptes €23.7bn Flamanville cost (site unreachable); RTE 2022 availability and output figures; Euratom Supply Agency VVER fuel statement; NEA 7530 pair effect (site blocked); Müller and Thurner referendum chronology.
- Execution receipt: run id model (verification/model.json), `uv run python run_all.py`, 18/18 invariants, results.json reproduced.
- metadata claims_target: claim-ledger.

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
