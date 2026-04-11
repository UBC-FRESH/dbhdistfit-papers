SHELL := /bin/bash
PYTHON ?= python
MANUSCRIPT_R0_DIR ?= manuscript-r0
MANUSCRIPT_R1_DIR ?= manuscript-r1
MANUSCRIPT_R2_DIR ?= manuscript-r2
MANUSCRIPT_DIR ?= $(MANUSCRIPT_R0_DIR)
TRUNCDATA_PICKLE ?= $(CURDIR)/data/interim/tiges_final_full.p
R2_EM_ZIP ?= em-submission-r2.zip
R2_REQUIRED_BUNDLE ?= em-resubmission-r2-required-tex-title.zip
R2_DIFF_PDF ?= manuscript-r2/latexdiff-em/main.pdf

.PHONY: help env data figures tables manuscript manuscript-r0 manuscript-r1 \
	manuscript-r2 simulations distribution-sweep supplement-build \
	title-page title-page-r0 title-page-r1 cover-letter cover-letter-r0 cover-letter-r1 \
	title-page-r2 cover-letter-r2 \
	preprint preprint-r0 preprint-r1 em-submission em-submission-r0 em-submission-r1 \
	preprint-r2 em-submission-r2 bundle-r2-required verify-r2-package \
	reference-validate reference-validate-r0 reference-validate-r1 \
	reference-validate-r2 \
	reference-validate-suggest reference-validate-suggest-r0 reference-validate-suggest-r1 \
	reference-validate-suggest-r2 \
	notebook repro clean

help:
	@echo "Targets:"
	@echo "  make env          - create/refresh virtual environment"
	@echo "  make data         - preprocess PSP tallies for truncated analysis"
	@echo "  make figures      - regenerate all figures"
	@echo "  make tables       - regenerate all tables"
	@echo "  make manuscript   - compile LaTeX manuscript (defaults to r0)"
	@echo "  make manuscript-r0 - compile LaTeX manuscript r0"
	@echo "  make manuscript-r1 - compile LaTeX manuscript r1"
	@echo "  make manuscript-r2 - compile LaTeX manuscript r2"
	@echo "  make title-page   - compile journal title page (defaults to r0)"
	@echo "  make title-page-r0 - compile journal title page r0"
	@echo "  make title-page-r1 - compile journal title page r1"
	@echo "  make title-page-r2 - compile journal title page r2"
	@echo "  make cover-letter - verify cover letter text (defaults to r0)"
	@echo "  make cover-letter-r0 - verify cover letter text r0"
	@echo "  make cover-letter-r1 - verify cover letter text r1"
	@echo "  make cover-letter-r2 - verify cover letter text r2"
	@echo "  make preprint     - build EarthArXiv-ready PDF (defaults to r0)"
	@echo "  make preprint-r0  - build EarthArXiv-ready PDF from r0"
	@echo "  make preprint-r1  - build EarthArXiv-ready PDF from r1"
	@echo "  make preprint-r2  - build EarthArXiv-ready PDF from r2"
	@echo "  make em-submission- build Editorial Manager package (defaults to r0)"
	@echo "  make em-submission-r0 - build Editorial Manager package from r0"
	@echo "  make em-submission-r1 - build Editorial Manager package from r1"
	@echo "  make em-submission-r2 - build Editorial Manager package from r2"
	@echo "  make bundle-r2-required - build required R2 3-file upload bundle"
	@echo "  make verify-r2-package - enforce exact file-list contracts for R2 zips"
	@echo "  make simulations  - run canonical synthetic robustness experiments"
	@echo "  make distribution-sweep - run empirical shape + tiered distribution sweep"
	@echo "  make supplement-build - regenerate all R2 supplement artefacts"
	@echo "  make reference-validate - validate BibTeX entries (defaults to r0)"
	@echo "  make reference-validate-r0 - validate BibTeX entries for r0"
	@echo "  make reference-validate-r1 - validate BibTeX entries for r1"
	@echo "  make reference-validate-r2 - validate BibTeX entries for r2"
	@echo "  make reference-validate-suggest - validate + suggest DOIs (defaults to r0)"
	@echo "  make reference-validate-suggest-r0 - validate + suggest DOIs for r0"
	@echo "  make reference-validate-suggest-r1 - validate + suggest DOIs for r1"
	@echo "  make reference-validate-suggest-r2 - validate + suggest DOIs for r2"
	@echo "  make notebook     - execute reproducibility notebook(s)"
	@echo "  make repro        - run full reproducibility pipeline"
	@echo "  make clean        - remove generated artefacts"

env:
	@if [ ! -d .venv ]; then $(PYTHON) -m venv .venv; fi
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

data:
	DBHDISTFIT_TRUNCDATA_PICKLE=$(TRUNCDATA_PICKLE) $(PYTHON) scripts/preprocess_data.py

figures: data
	$(PYTHON) scripts/generate_figures.py --config config/figures.yml

tables: data
	$(PYTHON) scripts/generate_tables.py --config config/tables.yml

manuscript:
	$(MAKE) -C $(MANUSCRIPT_DIR) all

manuscript-r0:
	$(MAKE) -C $(MANUSCRIPT_R0_DIR) all

manuscript-r1:
	$(MAKE) -C $(MANUSCRIPT_R1_DIR) all

manuscript-r2:
	$(MAKE) -C $(MANUSCRIPT_R2_DIR) all

title-page:
	$(MAKE) -C $(MANUSCRIPT_DIR) title-page

title-page-r0:
	$(MAKE) -C $(MANUSCRIPT_R0_DIR) title-page

title-page-r1:
	$(MAKE) -C $(MANUSCRIPT_R1_DIR) title-page

title-page-r2:
	$(MAKE) -C $(MANUSCRIPT_R2_DIR) title-page

cover-letter:
	@test -f $(MANUSCRIPT_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

cover-letter-r0:
	@test -f $(MANUSCRIPT_R0_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

cover-letter-r1:
	@test -f $(MANUSCRIPT_R1_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

cover-letter-r2:
	@test -f $(MANUSCRIPT_R2_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

preprint: figures tables manuscript
	MANUSCRIPT_DIR=$(MANUSCRIPT_DIR) $(PYTHON) scripts/build_preprint.py

preprint-r0: figures tables manuscript-r0
	MANUSCRIPT_DIR=$(MANUSCRIPT_R0_DIR) $(PYTHON) scripts/build_preprint.py

preprint-r1: figures tables manuscript-r1
	MANUSCRIPT_DIR=$(MANUSCRIPT_R1_DIR) $(PYTHON) scripts/build_preprint.py

preprint-r2: figures tables manuscript-r2
	MANUSCRIPT_DIR=$(MANUSCRIPT_R2_DIR) $(PYTHON) scripts/build_preprint.py

em-submission: figures tables manuscript title-page cover-letter
	MANUSCRIPT_DIR=$(MANUSCRIPT_DIR) $(PYTHON) scripts/prepare_em_submission.py

em-submission-r0: figures tables manuscript-r0 title-page-r0 cover-letter-r0
	MANUSCRIPT_DIR=$(MANUSCRIPT_R0_DIR) $(PYTHON) scripts/prepare_em_submission.py

em-submission-r1: figures tables manuscript-r1 title-page-r1 cover-letter-r1
	MANUSCRIPT_DIR=$(MANUSCRIPT_R1_DIR) $(PYTHON) scripts/prepare_em_submission.py

em-submission-r2: figures tables manuscript-r2 title-page-r2 cover-letter-r2
	MANUSCRIPT_DIR=$(MANUSCRIPT_R2_DIR) $(PYTHON) scripts/prepare_em_submission.py

bundle-r2-required: em-submission-r2
	@test -f $(MANUSCRIPT_R2_DIR)/title-page.tex || (echo "title-page.tex missing" && exit 1)
	@test -f $(R2_DIFF_PDF) || (echo "r1-r2-diff source missing: $(R2_DIFF_PDF)" && exit 1)
	@cp $(R2_DIFF_PDF) r1-r2-diff.pdf
	@rm -f $(R2_REQUIRED_BUNDLE)
	@zip -j -q $(R2_REQUIRED_BUNDLE) $(R2_EM_ZIP) $(MANUSCRIPT_R2_DIR)/title-page.tex r1-r2-diff.pdf
	@echo "[bundle-r2-required] wrote $(R2_REQUIRED_BUNDLE)"

verify-r2-package: bundle-r2-required
	@set -euo pipefail; \
	em_expected="diameter_comparison.pdf main.tex method_comparison.tex"; \
	em_actual="$$(unzip -Z1 "$(R2_EM_ZIP)" | sed '/\/$$/d' | xargs -n1 basename | sort | tr '\n' ' ' | sed 's/ $$//')"; \
	if [ "$$em_actual" != "$$em_expected" ]; then \
		echo "[verify-r2-package] FAIL: $(R2_EM_ZIP)"; \
		echo "  expected: $$em_expected"; \
		echo "  actual:   $$em_actual"; \
		exit 1; \
	fi; \
	echo "[verify-r2-package] OK: $(R2_EM_ZIP) -> $$em_actual"; \
	req_expected="em-submission-r2.zip r1-r2-diff.pdf title-page.tex"; \
	req_actual="$$(unzip -Z1 "$(R2_REQUIRED_BUNDLE)" | sed '/\/$$/d' | xargs -n1 basename | sort | tr '\n' ' ' | sed 's/ $$//')"; \
	if [ "$$req_actual" != "$$req_expected" ]; then \
		echo "[verify-r2-package] FAIL: $(R2_REQUIRED_BUNDLE)"; \
		echo "  expected: $$req_expected"; \
		echo "  actual:   $$req_actual"; \
		exit 1; \
	fi; \
	echo "[verify-r2-package] OK: $(R2_REQUIRED_BUNDLE) -> $$req_actual"

simulations: data
	$(PYTHON) scripts/run_simulations.py --config config/simulations.yml

distribution-sweep: data
	$(PYTHON) scripts/run_distribution_sweep.py --tiers config/distribution_tiers.yml

supplement-build: simulations distribution-sweep
	@echo "[supplement] rebuilt simulation + empirical robustness artefacts"

reference-validate:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_DIR)/references.bib --output $(MANUSCRIPT_DIR)/reference-validation-report.txt

reference-validate-r0:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_R0_DIR)/references.bib --output $(MANUSCRIPT_R0_DIR)/reference-validation-report.txt

reference-validate-r1:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_R1_DIR)/references.bib --output $(MANUSCRIPT_R1_DIR)/reference-validation-report.txt

reference-validate-r2:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_R2_DIR)/references.bib --output $(MANUSCRIPT_R2_DIR)/reference-validation-report.txt

reference-validate-suggest:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_DIR)/references.bib --output $(MANUSCRIPT_DIR)/reference-validation-report.txt

reference-validate-suggest-r0:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_R0_DIR)/references.bib --output $(MANUSCRIPT_R0_DIR)/reference-validation-report.txt

reference-validate-suggest-r1:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_R1_DIR)/references.bib --output $(MANUSCRIPT_R1_DIR)/reference-validation-report.txt

reference-validate-suggest-r2:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_R2_DIR)/references.bib --output $(MANUSCRIPT_R2_DIR)/reference-validation-report.txt

notebook: data
	$(PYTHON) -m jupyter nbconvert --to notebook --execute notebooks/dbhdistfit_truncdata.ipynb --output dbhdistfit_truncdata.executed.ipynb --output-dir notebooks

repro: figures tables notebook manuscript simulations distribution-sweep

clean:
	rm -rf figures/* tables/* $(MANUSCRIPT_R0_DIR)/build $(MANUSCRIPT_R1_DIR)/build $(MANUSCRIPT_R2_DIR)/build notebooks/*.executed.ipynb preprint/*.pdf em-submission*.zip em-submission-r*/ tmp/*
