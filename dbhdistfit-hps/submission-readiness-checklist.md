## Forest Science Submission Readiness Checklist (Brief Communication)

| **Category**                           | **Status**   | **Details & Notes**                                                                                                     |
|---------------------------------------|--------------|-------------------------------------------------------------------------------------------------------------------------|
| Article type & scope                  | ✅ Ready     | Brief Communication (≤2,000 words, ≤2 figures/tables); current draft ≈1,950 words with 1 figure + 1 table.             |
| Word-limit statement                  | ⚠️ To Do     | Forest Science requires explicit word-count declarations at the end of the manuscript (total incl./excl. references, abstract length, SI words). |
| Figures & tables                      | ✅ Ready     | Figure 1 (comparison plots) and Table 1 (RSS + relative L₂ stats) comply with ≤2 requirement; graphics at ≥300 dpi PNG—export final TIFF prior to submission. |
| Manuscript formatting                 | ✅ Ready     | LaTeX build passes; no line numbering; sections limited to three heading levels; keywords needed in final cover page.   |
| References & self-citation            | ✅ Ready     | Bibliography trimmed to external sources; `references.bib` refreshed after removing Paradis (2019).                      |
| Statements & Declarations section     | ⚠️ To Do     | Add combined “Statements and Declarations” block (Funding, Competing Interests, Data Availability, Author Contributions, Ethics/Consent as applicable). |
| Data & reproducibility artefacts      | ✅ Ready     | DataLad subdataset (`data/`) with GitHub + S3 remotes; preprocessing script (`scripts/preprocess_data.py`) regenerates processed data; `make repro` rebuilds figures/tables/LaTeX. |
| Supplementary information             | ⚠️ Decide    | Determine whether to include reproduction bundle (Makefile + DataLad instructions) as SI or cite repository only.       |
| Title page metadata                   | ⚠️ To Do     | Prepare journal-specific title page (authors, affiliations, corresponding author email, ORCID IDs).                     |
| Abstract & keywords                   | ⚠️ Review    | Confirm abstract length ≤250 words and add 4–6 keywords (non-redundant with title).                                     |
| Cover letter                          | ⚠️ Draft     | Compose cover letter summarising contribution, data availability, and reviewer suggestions.                             |
| ORCID + submission portal data        | ⚠️ Prepare   | Gather ORCID for corresponding author; ensure Competing Interest statement aligns with portal requirements.             |
| Checklist alignment in manuscript     | ✅ Ready     | Results & Discussion explicitly quantify control vs. test agreement (<2.4 % stand table; <8.5 % HPS).                   |
| Repository readiness                  | ✅ Ready     | `make repro` clean; README documents DataLad usage; figures/tables regenerating from workflow.                           |
| Final proofing                        | ⚠️ To Do     | Run grammar/style pass, confirm forest-science terminology, and ensure figure/table captions are stand-alone.           |

### Immediate Action Items
1. Insert the Forest Science word-count block at the end of the manuscript.
2. Add “Statements and Declarations” section covering funding, competing interests, author contributions, and data availability (link to DataLad repo/S3 remote).
3. Prepare journal-specific title page and confirm abstract + keywords meet guidelines.
4. Export final figure in TIFF format at ≥300 dpi (submit both TIFF and embedded PDF version if required).
5. Draft cover letter highlighting brief communication scope, quantitative agreement (near-perfect fit), and reproducible pipeline.
6. Decide whether to package reproduction scripts/notebook as Supplementary Information; label files accordingly if included.
7. Proofread for journal style, double-check references, and ensure README/manuscript cross-reference data/Zenodo (if DOI minted).

### Data & Reproducibility Snapshot
- **Data access**: `git submodule update --init --recursive` + `datalad get data/processed/binned_meta_plots.parquet`; raw PSP pickle stored in annex.
- **Pipeline**: `make repro` → runs preprocessing, regenerates figures/tables, executes notebook, compiles LaTeX.
- **Outputs**: `figures/sepm_r_comparison.png`, `tables/method_comparison.{csv,tex}`, notebook artefacts, manuscript PDF.
- **Environment**: Python 3.11+, SciPy stack, DataLad (optional but recommended for auto-fetching annexed data).

### Submission Package Checklist
- [ ] Manuscript (LaTeX → PDF + source `.tex`/`.bib`)
- [ ] Title page (Word/LaTeX as requested)
- [ ] Figure 1 TIFF (≥300 dpi) + original PNG
- [ ] Table 1 (inline; submit CSV if portal requests source)
- [ ] Cover letter (PDF or plain text)
- [ ] Supplementary material (if decided) with README
- [ ] ORCID + author metadata ready for submission portal
