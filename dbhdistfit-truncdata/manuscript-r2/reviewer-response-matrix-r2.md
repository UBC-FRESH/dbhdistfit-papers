# Post-R1 Decision-Letter Issue Matrix (FRSC-D-25-00220R1)

Snapshot date: 2026-04-11 (UTC)

Status legend:
- `[x]` resolved
- `[~]` partially resolved / verify before submission
- `[ ]` open

This matrix tracks only the issues listed in the Editor decision letter for manuscript `FRSC-D-25-00220R1`.

| ID | Source | Issue from decision letter | Current response/action | Evidence in repo | Status | Remaining action before submit |
| --- | --- | --- | --- | --- | --- | --- |
| ED-REQ-1 | Editor instructions | Provide point-by-point response in the Editorial Manager "Response to Reviewers" box | Point-by-point response prepared in markdown and portal-ready plain-text formats | `response-to-reviewers-r2.md`, `response-to-reviewers-r2-portal.txt` | `[x]` | Paste `response-to-reviewers-r2-portal.txt` into the portal response box |
| ED-REQ-2 | Editor instructions | Highlight all manuscript changes (colored/underlined/highlighted) | Latexdiff artifact regenerated from final R1 baseline to current R2 sources | `latexdiff-em/main.pdf` | `[x]` | None |
| ED-REQ-3 | Editor instructions | Describe additional experiments and detailed rebuttals where disagreement exists | Added empirical shape-stratified and simulation analyses plus explicit fairness/limitations text | `sections/methods.tex`, `sections/results.tex`, `sections/discussion.tex`, `tables/shape_robustness_*.csv`, `tables/simulation_robustness*.csv` | `[x]` | None |
| ED-REQ-4 | Editor instructions | Ensure revised manuscript conforms to journal style | Manuscript compiles and uses existing journal-oriented structure | `manuscript-r2/main.tex`, successful `make manuscript-r2` build | `[~]` | Final manual style/compliance pass at upload stage |
| ED-REQ-5 | Editor instructions | Upload editable source files only (Word/TeX) | Editable TeX-based package regenerated | `em-submission-r2.zip`, `em-submission-r2/main.tex` | `[x]` | None |
| ED-REQ-6 | Editor instructions | Due date for revised manuscript: 02 Apr 2026 | Package is prepared; submission is now past the stated due date | current build timestamps | `[~]` | Submit in Editorial Manager immediately |
| ED-REQ-7 | Editor instructions | Authorship/order must remain correct unless formal change request is approved | No authorship changes detected | `manuscript-r2/main.tex` declarations; single-author metadata | `[x]` | None |
| EIC-1 | Editor-in-Chief | Prioritize manuscript strength over strict brief-communication word limit | Added robustness evidence and tempered claims rather than minimizing scope | `sections/methods.tex` robustness subsection; `sections/results.tex`; `sections/discussion.tex` | `[x]` | None |
| AE-1 | Associate Editor | Robustness expansion is optional but would strengthen manuscript (e.g., supplement) | Added empirical shape and simulation robustness analyses; summaries included directly in appendix tables B1--B3 | `sections/appendix-robustness.tex`, `tables/shape_robustness_*.csv`, `tables/simulation_robustness*.csv`, `figures/shape_robustness_wins.pdf`, `figures/simulation_robustness.pdf` | `[x]` | None |
| AE-2 | Associate Editor | Be explicit about limitations and the consequence of excluding extensions to other distributions/shapes | Discussion explicitly bounds claims and states context dependence | `sections/discussion.tex` | `[x]` | None |
| AE-3 | Associate Editor | Address/rebut concern that method robustness was not yet proven | Added direct robustness evidence across 32 empirical combinations and four synthetic families | `tables/shape_robustness_group_level.csv`, `tables/simulation_robustness.csv`, `sections/results.tex` | `[x]` | None |
| AE-4 | Associate Editor (re: Reviewer #2 comment 4) | Carefully acknowledge or rebut "unfair 1sc comparison" concern | Added shape-diverse robustness benchmarking and explicit low-information caveats; retained main figure as representative and made analysis-level fairness rebuttal explicit in response text | `sections/results.tex`, `sections/discussion.tex`, `response-to-reviewers-r2.md`, `response-to-reviewers-r2-portal.txt` | `[x]` | None |
| R1-ACK-1 | Reviewer #1 | "The authors have successfully addressed our concerns." | No additional technical request from Reviewer #1 | Decision letter text | `[x]` | None |
| R2-1 | Reviewer #2 | Generalization concern: right truncation may be impractical; risk of bias beyond upper bound | Clarified operational interpretation of upper bound and alternatives (left-truncation-only / location parameter) | `sections/introduction.tex`, `sections/methods.tex` | `[x]` | None |
| R2-2 | Reviewer #2 | Need shape-diverse evidence; inverse-J-only evidence is insufficient | Added empirical shape classes and canonical synthetic scenarios | `tables/shape_robustness_*.csv`, `tables/simulation_robustness*.csv`, `sections/results.tex` | `[x]` | None |
| R2-3 | Reviewer #2 | Practical meaning of 1st vs 2sc differences not justified | Added RMSE and max-absolute difference metrics and summarized ranges | `tables/method_comparison.csv`, `sections/results.tex` | `[x]` | None |
| R2-4 | Reviewer #2 | "Unfair" comparison to 1sc for inverse-J data; requested replacing Fig. 1(a,c,e) with different shapes | Addressed fairness concern via full shape-diverse benchmarking reported in appendix tables B1--B3; main figure retained as representative visual panel; response text now states this explicitly | `sections/results.tex`, `sections/appendix-robustness.tex`, `response-to-reviewers-r2.md`, `response-to-reviewers-r2-portal.txt` | `[x]` | None |
