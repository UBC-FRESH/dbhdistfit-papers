## Discover Forests Submission Readiness Checklist (Brief Report)

| **Category**                           | **Status**   | **Details & Notes**                                                                                                     |
|---------------------------------------|--------------|-------------------------------------------------------------------------------------------------------------------------|
| Article type & scope                  | ✅ Ready     | Brief Report (abstract <250 words); current draft ≈1,900 words with 1 figure + 1 table. |
| Word-limit statement                  | ✅ Ready     | Word-count block appended to manuscript main text (`Word Count Summary` section). |
| Figures & tables                      | ✅ Ready     | Figure 1 (comparison plots) and Table 1 (RSS + relative L₂ stats) comply with ≤2 requirement; `make figures` now emits PNG/PDF/EPS/TIFF (`Fig1.*`) with embedded fonts (Type 42). |
| Manuscript formatting                 | ✅ Ready     | LaTeX build passes; no line numbering; sections limited to three heading levels; keywords listed after title.          |
| References & self-citation            | ✅ Ready     | Bibliography trimmed to external sources; `references.bib` refreshed after removing Paradis (2019).                      |
| Statements & Declarations section     | ✅ Ready     | Section added with funding, competing interests, author contributions, data availability, and ethics statements. |
| Data & reproducibility artefacts      | ✅ Ready     | DataLad subdataset (`data/`) with GitHub + S3 remotes; preprocessing script (`scripts/preprocess_data.py`) regenerates processed data; `make repro` rebuilds figures/tables/LaTeX. |
| Supplementary information             | ✅ Ready     | No separate SI submission; manuscript and cover letter reference GitHub workflow for full reproducibility.              |
| Title page metadata                   | ✅ Ready     | `manuscript/title-page.tex` prepared with author, affiliation, ORCID, keywords, and word counts.                         |
| Peer review model                     | ✅ Ready     | Single-anonymous (Discover Forests); manuscript includes author names/affiliations.                                      |
| Abstract & keywords                   | ✅ Ready     | Abstract is 134 words; five keywords listed post-title per journal guidance.                                            |
| Cover letter                          | ✅ Ready     | Drafted in `manuscript/cover-letter.tex`, emphasising Brief Report scope and transfer context.                          |
| ORCID + submission portal data        | ✅ Ready     | ORCID (0000-0001-9618-8797) and disclosure statements present in manuscript/title page.                                |
| Checklist alignment in manuscript     | ✅ Ready     | Results & Discussion explicitly quantify control vs. test agreement (<2.4 % stand table; <8.5 % HPS).                   |
| Repository readiness                  | ✅ Ready     | `make repro` clean; README documents DataLad usage; figures/tables regenerating from workflow.                           |
| Final proofing                        | ✅ Ready     | Proofreading pass completed; captions/paragraph spacing adjusted, Data Availability wording tightened.                  |

### Immediate Action Items
1. Run `make manuscript` and `make cover-letter` immediately before upload to refresh PDFs/Bib.
2. Upload the manuscript PDF/LaTeX source, title page, and cover letter via Snapp; include the data availability statement in the manuscript.

### Data & Reproducibility Snapshot
- **Data access**: `git submodule update --init --recursive` + `datalad get data/processed/binned_meta_plots.parquet`; raw PSP pickle stored in annex.
- **Pipeline**: `make repro` → runs preprocessing, regenerates figures/tables, executes notebook, compiles LaTeX.
- **Outputs**: `figures/sepm_r_comparison.png`, `tables/method_comparison.{csv,tex}`, notebook artefacts, manuscript PDF.
- **Environment**: Python 3.11+, SciPy stack, DataLad (optional but recommended for auto-fetching annexed data).

### Submission Package Checklist
- [x] Manuscript (LaTeX → PDF + source `.tex`/`.bib`)
- [x] Title page (LaTeX as requested)
- [x] Figure 1 source (PDF/PNG; upload additional formats if requested)
- [x] Table 1 (inline; submit CSV if portal requests source)
- [x] Cover letter (PDF or plain text)
- [x] Supplementary material note (reference GitHub repository; no separate upload)
- [x] ORCID + author metadata ready for submission portal
