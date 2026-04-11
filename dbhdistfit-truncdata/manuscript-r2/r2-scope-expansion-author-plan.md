# R2 Scope Expansion Plan (Author-Facing, Detailed)

## 1) Purpose

This document records the full scope expansion implemented for the R2 revision of:

- Manuscript: `A Two-Stage Fitting Method for Truncated Stem Diameter Distributions`
- Manuscript ID: `FRSC-D-25-00220R1`

It is written for author use: to support final manuscript decisions, response-to-reviewers positioning, and submission QA.

---

## 2) Why Scope Was Expanded

The post-R1 decision letter explicitly signaled that:

1. Additional robustness evidence would strengthen the manuscript.
2. Word-count limits should not block improvements that materially improve quality.
3. Reviewer #2 concerns about shape diversity, generalization, and fairness needed explicit acknowledgement/rebuttal.

The R2 expansion was therefore designed to:

- preserve the original 1sc vs 1st vs 2sc comparison framework,
- add cross-shape stress tests (empirical + synthetic),
- quantify practical differences between 1st and 2sc,
- keep claims bounded and context-dependent rather than universal.

---

## 3) Expansion Summary (Delta vs Prior Compact Scope)

## A) New empirical robustness layer (shape-stratified, all 32 groups)

What was added:

- Fit all 32 species-group / cover-type combinations.
- Classify each empirical histogram into one of three shape classes:
  - `inverse-J-ish`
  - `unimodal-mid`
  - `right-peaked/flat`
- Summarize:
  - method win counts by shape class,
  - 1st-vs-2sc discrepancy metrics (RMSE, max abs),
  - fit-failure counts.

Where implemented:

- Config: `config/distribution_tiers.yml`
- Script: `scripts/run_distribution_sweep.py`
- Outputs:
  - `tables/shape_robustness_group_level.csv`
  - `tables/shape_robustness_summary.csv`
  - `tables/shape_robustness_metrics.csv`
  - `tables/distribution_sweep_core_detail.csv`
  - `figures/shape_robustness_wins.pdf`

Shape classification rule details:

- Light smoothing kernel: `[0.25, 0.5, 0.25]`.
- Peak location ratio:
  - `<= 0.2` -> `inverse-J-ish`
  - `<= 0.6` -> `unimodal-mid`
  - `> 0.6` -> `right-peaked/flat`

Current empirical outcome snapshot:

- Shape membership:
  - inverse-J-ish: 27 groups
  - unimodal-mid: 4 groups
  - right-peaked/flat: 1 group
- Winner counts:
  - inverse-J-ish: 2sc = 25, 1sc = 2
  - unimodal-mid: 1sc = 3, 2sc = 1
  - right-peaked/flat: 2sc = 1

Interpretation impact:

- This directly addresses the "inverse-J-only evidence" criticism.
- It also supports bounded claims: method preference is shape/context dependent.

## B) New synthetic robustness layer (canonical scenarios)

What was added:

- Canonical simulation suite with fixed seed (`20260402`), replicated design, and controlled sample sizes.
- Four scenario families:
  - `inverse_j`
  - `unimodal_mid`
  - `near_flat`
  - `right_shifted`
- Two sample sizes: `1500`, `4000`.
- Replicates: `40` per scenario-size setting.

Where implemented:

- Config: `config/simulations.yml`
- Script: `scripts/run_simulations.py`
- Outputs:
  - `tables/simulation_robustness.csv`
  - `tables/simulation_robustness_wins.csv`
  - `tables/simulation_robustness_metrics.csv`
  - `figures/simulation_robustness.pdf`

Current synthetic outcome snapshot:

- 2sc wins all replicates in:
  - inverse_j (1500, 4000)
  - near_flat (1500, 4000)
- 2sc mostly/all wins in:
  - unimodal_mid (1500: 33/40, 4000: 40/40)
- 1sc dominates in:
  - right_shifted (1500: 39/40, 4000: 40/40)

Interpretation impact:

- This directly addresses Reviewer #2 concerns on shape robustness and fairness.
- It makes explicit that 2sc is strong but not universally dominant under all low-information/right-shifted settings.

## C) Expanded distribution context (tiered registry checks)

What was added:

- Core fit families in expanded robustness workflows:
  - `weibull`, `gamma`, `lognormal`, `exponential`
- Supplemental registry diagnostics (availability/support snapshot):
  - `ga`, `w`, `exp`, `gg`, `birnbaum_saunders`, `johnsonsb`, `pareto`, `fisk`, `ll`

Where implemented:

- Config: `config/distribution_tiers.yml`
- Script: `scripts/run_distribution_sweep.py`
- Outputs:
  - `tables/distribution_sweep_supplemental_registry.csv`
  - `tables/distribution_sweep_supplemental_registry.tex`

Interpretation impact:

- Documents broader ecosystem context without overloading the core manuscript comparison.

## D) Optional `nemora` backend with local fallback

What was added:

- Adapter-based runtime that supports:
  - local-only execution (default fallback),
  - optional `nemora` integration when available.
- Provenance metadata attached to robustness outputs:
  - `backend`
  - `nemora_version`
  - `nemora_commit`

Where implemented:

- Adapter: `scripts/nemora_adapter.py`
- Pin guidance: `requirements.txt` (commented optional pin)
  - `nemora @ git+https://github.com/UBC-FRESH/nemora.git@cbba47789d7b680dc30a0e04100e26bfa46b6f81`

Important nuance:

- Provenance fields currently appear in detailed robustness outputs (for example `shape_robustness_group_level.csv`, `simulation_robustness.csv`), but not all aggregate summary tables.
- If needed for strict consistency claims, either:
  - add provenance fields to every aggregate table, or
  - narrow wording to "detailed robustness outputs include provenance."

---

## 4) Pipeline and Packaging Expansion

## New/updated automation targets

Makefile now supports R2 analysis and packaging flow:

- `make simulations`
- `make distribution-sweep`
- `make supplement-build`
- `make manuscript-r2`
- `make title-page-r2`
- `make cover-letter-r2`
- `make preprint-r2`
- `make em-submission-r2`
- `make reference-validate-r2`
- `make reference-validate-suggest-r2`

Packaging behavior expansion:

- `scripts/prepare_em_submission.py` now:
  - derives submission label from manuscript dir (`manuscript-r2` -> `em-submission-r2`),
  - includes robustness supplement assets in flat archive when present.

Current package:

- `em-submission-r2.zip` generated successfully.

---

## 5) Manuscript-Level Scope Expansion (What was written into paper text)

## Methods expansion

New subsection in Methods:

- `Robustness assessment workflow`
  - empirical shape-stratified analysis across all 32 combinations,
  - canonical synthetic benchmark across four scenario families,
  - optional backend adapter and provenance recording.

File:

- `manuscript-r2/sections/methods.tex`

## Results expansion

Results now explicitly report:

- shape-stratified empirical robustness summaries,
- simulation robustness behavior across scenarios/sample sizes,
- bounded interpretation where rankings are not uniform.

File:

- `manuscript-r2/sections/results.tex`

## Discussion expansion

Discussion now:

- keeps non-universal claim posture,
- recognizes context dependence (especially lower-information cases),
- positions 2sc as strong under tested conditions, not a universal replacement.

File:

- `manuscript-r2/sections/discussion.tex`

---

## 6) Quantitative Headline Deltas You Can Reuse in Author Narratives

Empirical (32 combinations):

- 2sc stage-2 AICc lowest in `25/32`.
- Remaining `7/32` favor 1sc.
- 1st best in `0/32`.
- 1st failures observed in 2 combinations in the main comparison table.

Shape-stratified empirical:

- inverse-J-ish class dominates sample (27/32 groups), but non-inverse-J classes are present and informative.
- right-peaked/flat class shows larger discrepancy magnitude than inverse-J/unimodal classes.

Synthetic:

- 2sc dominates inverse_j and near_flat scenarios at both sample sizes.
- 2sc also dominates unimodal_mid except some 1500-sample replicates.
- right_shifted strongly favors 1sc, which provides explicit evidence for context dependence.

---

## 7) How This Expansion Answers the Decision-Letter Issues

Directly addressed:

1. Need for broader robustness evidence beyond inverse-J.
2. Need for explicit practical comparison metrics (1st vs 2sc).
3. Need to confront fairness concern around 1sc comparisons under shape bias.
4. Need for stronger, non-universal claim framing.
5. Need to prioritize manuscript strength over strict brevity.

---

## 8) Known Remaining Items (Submission-Adjacent, Not Scope Gaps)

These are packaging/response hygiene items rather than missing technical scope:

1. Regenerate highlighted-changes (`latexdiff`) artifact from final R1 baseline to final R2 sources.
2. Ensure submission metadata/upload manifest files are fully R2-current.
3. Finalize portal-ready plain-text response formatting for Editorial Manager box.
4. Optionally standardize provenance columns across all robustness summary tables if strict universal wording is retained.

---

## 9) Reproducible Execution Recipe (Author Quick Use)

From `dbhdistfit-truncdata/`:

```bash
make simulations
make distribution-sweep
make manuscript-r2
make em-submission-r2
```

Expected high-level products:

- Manuscript PDF: `manuscript-r2/main.pdf`
- Robustness figures: `figures/shape_robustness_wins.pdf`, `figures/simulation_robustness.pdf`
- Robustness tables: `tables/shape_robustness_*.csv`, `tables/simulation_robustness*.csv`
- Submission archive: `em-submission-r2.zip`

---

## 10) Author Positioning Guidance (Internal)

When summarizing R2 scope to editor/AE/reviewer:

1. Lead with the fact that robustness was expanded in two independent layers:
   - empirical cross-shape evidence across all 32 combinations,
   - canonical synthetic scenarios with controlled replication.
2. Emphasize that fairness concerns were handled by full-shape benchmarking, not a single-panel visual swap.
3. Keep final claims bounded:
   - "strong under tested conditions"
   - "context-dependent in low-information settings"
   - avoid universal replacement language.

