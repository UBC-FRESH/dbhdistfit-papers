# R2 Submission Readiness Checklist (Final Pass)

Snapshot date: 2026-04-11 (UTC)

Legend:
- `[x]` done
- `[~]` partial / verify
- `[ ]` pending

## Editorial and administrative package
- [x] Point-by-point response markdown is current (`response-to-reviewers-r2.md`).
- [x] Portal-ready plain-text response prepared (`response-to-reviewers-r2-portal.txt`).
- [x] Highlighted-changes artifact regenerated (`latexdiff-em/main.pdf`).
- [x] Submission manifest updated for R2 (`submission-upload-manifest.md`).
- [x] Submission metadata updated for R2 (`submission-metadata.md`).
- [x] Cover letter refreshed with current date and R2 scope (`cover-letter.txt`).
- [x] Authorship unchanged (single author).
- [ ] Upload package in Editorial Manager (past due date; submit immediately).

## Scientific response completeness (post-R1 letter)
- [x] Explicit robustness expansion included in manuscript appendix (`sections/appendix-robustness.tex`).
- [x] Fairness concern (1sc vs 2sc) addressed with shape-diverse analysis framing in response text.
- [x] Practical significance metrics (RMSE/max-abs) reported in main results.
- [x] Limitation framing is explicit and bounded in Discussion.
- [x] Appendix table references are consistent (`B1--B3`) across manuscript and response documents.

## Packaging and build QA
- [x] `manuscript-r2/main.pdf` rebuilds successfully.
- [x] `em-submission-r2.zip` rebuilt successfully.
- [x] R2 package is truly minimal: compile-only manuscript source files in zip; title page and cover letter uploaded separately.
- [x] Blinded manuscript (`em-submission-r2/main.tex`) excludes author-identifying metadata.
- [~] LaTeX warnings remain non-fatal (expected overfull boxes; build completes).

## Immediate final action
- [ ] Submit in portal now using `submission-upload-manifest.md`.
