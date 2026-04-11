# R2 Resubmission Roadmap

- [x] Phase 1 — Baseline and reproducibility setup
  - [x] Task 1.1 — Freeze `manuscript-r1` and create `manuscript-r2`
  - [x] Task 1.2 — Add R2 Makefile targets and packaging hooks
  - [x] Task 1.3 — Pin optional `nemora` backend commit for reproducibility

- [x] Phase 2 — Analysis pipeline expansion
  - [x] Task 2.1 — Add optional `nemora` adapter with local fallback
  - [x] Task 2.2 — Add canonical simulation workflow and outputs
  - [x] Task 2.3 — Add empirical shape-stratified robustness workflow
  - [x] Task 2.4 — Add tiered distribution sweep registry reporting (core + supplemental)

- [x] Phase 3 — Manuscript content updates
  - [x] Task 3.1 — Methods: document optional backend + fallback behaviour
  - [x] Task 3.2 — Results: report empirical shape and simulation robustness summaries
  - [x] Task 3.3 — Discussion: bound claims and explicitly report mixed/failure scenarios

- [ ] Phase 4 — Response package and submission
  - [x] Task 4.1 — Draft R2 reviewer response matrix
  - [x] Task 4.2 — Draft R2 point-by-point response text
  - [ ] Task 4.3 — Final QA build and package upload to Editorial Manager

## R2 analysis artefacts

- Empirical shape robustness:
  - `tables/shape_robustness_summary.{csv,tex}`
  - `tables/shape_robustness_metrics.{csv,tex}`
  - `figures/shape_robustness_wins.pdf`
- Simulation robustness:
  - `tables/simulation_robustness.{csv,tex}`
  - `figures/simulation_robustness.pdf`
- Tiered distribution registry snapshot:
  - `tables/distribution_sweep_supplemental_registry.{csv,tex}`

## Backend provenance

All new R2 robustness outputs include backend provenance fields:
- `backend` (`local` or `nemora`)
- `nemora_version` (when available)
- `nemora_commit` (when available)
