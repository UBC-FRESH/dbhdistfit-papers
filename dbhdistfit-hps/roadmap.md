# HPS CJFR Submission Roadmap

- [x] Phase 0 — Scope and article type
  - [x] Task 0.1 — Confirm article type
    - [x] Subtask 0.1.1 — Choose Research Article vs Note based on word/reference limits
    - [x] Subtask 0.1.2 — Confirm abstract word count ≤ 200
  - [x] Task 0.2 — Baseline counts
    - [x] Subtask 0.2.1 — Compute word count (Introduction through Discussion)
    - [x] Subtask 0.2.2 — Count total references and compare to limits

- [x] Phase 1 — CJFR formatting conversion
  - [x] Task 1.1 — Create CJFR manuscript variant
    - [x] Subtask 1.1.1 — Add CJFR-specific manuscript directory or build target
    - [x] Subtask 1.1.2 — Preserve Discover Forests files unchanged
  - [x] Task 1.2 — Page layout and spacing
    - [x] Subtask 1.2.1 — Set 8.5x11 (or A4) single-column layout
    - [x] Subtask 1.2.2 — Enable double-spacing
    - [x] Subtask 1.2.3 — Enable continuous line numbers
    - [x] Subtask 1.2.4 — Ensure page numbering is visible
  - [x] Task 1.3 — Manuscript order
    - [x] Subtask 1.3.1 — Title page with authors and affiliations
    - [x] Subtask 1.3.2 — Abstract and keywords placement
    - [x] Subtask 1.3.3 — Body order: Introduction → Methods → Results → Discussion
    - [x] Subtask 1.3.4 — Add Acknowledgements before References

- [x] Phase 2 — References and citation style
  - [x] Task 2.1 — Switch to Harvard author-year citations
    - [x] Subtask 2.1.1 — Update LaTeX class and bibliography style
    - [x] Subtask 2.1.2 — Verify alphabetical ordering in references
    - [x] Subtask 2.1.3 — Ensure DOIs/hyperlinks are present where available
  - [x] Task 2.2 — Citation consistency QA
    - [x] Subtask 2.2.1 — Check all in-text citations use author-year format
    - [x] Subtask 2.2.2 — Remove numeric citation remnants

- [ ] Phase 3 — Content alignment with CJFR requirements
  - [ ] Task 3.1 — Abbreviations and terminology
    - [x] Subtask 3.1.1 — Define abbreviations at first use (Abstract + text + captions)
    - [ ] Subtask 3.1.2 — Verify consistent spelling (Oxford/Merriam-Webster)
  - [x] Task 3.2 — Statistical reporting
    - [x] Subtask 3.2.1 — Avoid * / ** significance without p-values
    - [x] Subtask 3.2.2 — State model assumptions clearly
  - [x] Task 3.3 — Statements and declarations
    - [x] Subtask 3.3.1 — Convert Statements/Declarations to CJFR Acknowledgements/Notes
    - [x] Subtask 3.3.2 — Ensure data availability statement remains

- [ ] Phase 4 — Appendices and supplementary material
  - [ ] Task 4.1 — Appendix handling
    - [ ] Subtask 4.1.1 — Decide appendix vs supplementary placement
    - [ ] Subtask 4.1.2 — If appendix, ensure A-numbering for figures/tables/equations
  - [ ] Task 4.2 — Supplementary files (if any)
    - [ ] Subtask 4.2.1 — Name files per CJFR convention (suppla/supplb)
    - [ ] Subtask 4.2.2 — Cite supplementary material via manuscript footnote

- [ ] Phase 5 — Figures, tables, and permissions
  - [ ] Task 5.1 — Figure/table compliance
    - [ ] Subtask 5.1.1 — Verify captions use required format and define symbols
    - [ ] Subtask 5.1.2 — Confirm figures/tables cited in order
  - [ ] Task 5.2 — Permissions
    - [ ] Subtask 5.2.1 — Confirm all figures/tables are original
    - [ ] Subtask 5.2.2 — Add permission statements if any adapted material exists

- [ ] Phase 6 — Build, packaging, and QA
  - [ ] Task 6.1 — CJFR build pass
    - [ ] Subtask 6.1.1 — Build CJFR manuscript PDF with line numbers
    - [ ] Subtask 6.1.2 — Verify spacing, pagination, and column layout
  - [ ] Task 6.2 — Limits and checklist verification
    - [ ] Subtask 6.2.1 — Verify word count within article-type limits
    - [ ] Subtask 6.2.2 — Verify reference count within limits
    - [ ] Subtask 6.2.3 — Final proofread for CJFR compliance

- [ ] Phase 7 — Submission and archiving
  - [ ] Task 7.1 — Submission assets
    - [ ] Subtask 7.1.1 — Draft CJFR cover letter
    - [ ] Subtask 7.1.2 — Prepare submission metadata (authors, ORCID, statements)
  - [ ] Task 7.2 — Submit
    - [ ] Subtask 7.2.1 — Upload manuscript, figures/tables, appendix/supplement
    - [ ] Subtask 7.2.2 — Enter portal metadata and declarations
    - [ ] Subtask 7.2.3 — Record submission ID and date
  - [ ] Task 7.3 — Archive
    - [ ] Subtask 7.3.1 — Tag CJFR submission branch
    - [ ] Subtask 7.3.2 — Save submission package snapshot

## Detailed Next Steps Notes

- Locked CJFR article type: Note (word count ~1008; abstract 132 words; references 5).
- CJFR manuscript variant created (`dbhdistfit-hps/manuscript-cjfr`) with line numbers and double spacing; build via `make manuscript-cjfr`.
- Harvard author–year references verified (alphabetical; DOIs/URLs present where available).
- Defined dataset abbreviations in text and captions (SPFL-S/Birch-M/Maple-H; sepm/bop/ers; r/m/f) and stated modeling assumptions.
- Remaining: spelling consistency check and appendix vs supplement decision.
