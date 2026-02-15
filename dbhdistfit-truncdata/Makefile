SHELL := /bin/bash
PYTHON ?= python
MANUSCRIPT_R0_DIR ?= manuscript-r0
MANUSCRIPT_R1_DIR ?= manuscript-r1
MANUSCRIPT_DIR ?= $(MANUSCRIPT_R0_DIR)
TRUNCDATA_PICKLE ?= $(CURDIR)/data/interim/tiges_final_full.p

.PHONY: help env data figures tables manuscript manuscript-r0 manuscript-r1 \
	title-page title-page-r0 title-page-r1 cover-letter cover-letter-r0 cover-letter-r1 \
	preprint preprint-r0 preprint-r1 em-submission em-submission-r0 em-submission-r1 \
	reference-validate reference-validate-r0 reference-validate-r1 \
	reference-validate-suggest reference-validate-suggest-r0 reference-validate-suggest-r1 \
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
	@echo "  make title-page   - compile journal title page (defaults to r0)"
	@echo "  make title-page-r0 - compile journal title page r0"
	@echo "  make title-page-r1 - compile journal title page r1"
	@echo "  make cover-letter - verify cover letter text (defaults to r0)"
	@echo "  make cover-letter-r0 - verify cover letter text r0"
	@echo "  make cover-letter-r1 - verify cover letter text r1"
	@echo "  make preprint     - build EarthArXiv-ready PDF (defaults to r0)"
	@echo "  make preprint-r0  - build EarthArXiv-ready PDF from r0"
	@echo "  make preprint-r1  - build EarthArXiv-ready PDF from r1"
	@echo "  make em-submission- build Editorial Manager package (defaults to r0)"
	@echo "  make em-submission-r0 - build Editorial Manager package from r0"
	@echo "  make em-submission-r1 - build Editorial Manager package from r1"
	@echo "  make reference-validate - validate BibTeX entries (defaults to r0)"
	@echo "  make reference-validate-r0 - validate BibTeX entries for r0"
	@echo "  make reference-validate-r1 - validate BibTeX entries for r1"
	@echo "  make reference-validate-suggest - validate + suggest DOIs (defaults to r0)"
	@echo "  make reference-validate-suggest-r0 - validate + suggest DOIs for r0"
	@echo "  make reference-validate-suggest-r1 - validate + suggest DOIs for r1"
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

title-page:
	$(MAKE) -C $(MANUSCRIPT_DIR) title-page

title-page-r0:
	$(MAKE) -C $(MANUSCRIPT_R0_DIR) title-page

title-page-r1:
	$(MAKE) -C $(MANUSCRIPT_R1_DIR) title-page

cover-letter:
	@test -f $(MANUSCRIPT_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

cover-letter-r0:
	@test -f $(MANUSCRIPT_R0_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

cover-letter-r1:
	@test -f $(MANUSCRIPT_R1_DIR)/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

preprint: figures tables manuscript
	MANUSCRIPT_DIR=$(MANUSCRIPT_DIR) $(PYTHON) scripts/build_preprint.py

preprint-r0: figures tables manuscript-r0
	MANUSCRIPT_DIR=$(MANUSCRIPT_R0_DIR) $(PYTHON) scripts/build_preprint.py

preprint-r1: figures tables manuscript-r1
	MANUSCRIPT_DIR=$(MANUSCRIPT_R1_DIR) $(PYTHON) scripts/build_preprint.py

em-submission: figures tables manuscript title-page cover-letter
	MANUSCRIPT_DIR=$(MANUSCRIPT_DIR) $(PYTHON) scripts/prepare_em_submission.py

em-submission-r0: figures tables manuscript-r0 title-page-r0 cover-letter-r0
	MANUSCRIPT_DIR=$(MANUSCRIPT_R0_DIR) $(PYTHON) scripts/prepare_em_submission.py

em-submission-r1: figures tables manuscript-r1 title-page-r1 cover-letter-r1
	MANUSCRIPT_DIR=$(MANUSCRIPT_R1_DIR) $(PYTHON) scripts/prepare_em_submission.py

reference-validate:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_DIR)/references.bib --output $(MANUSCRIPT_DIR)/reference-validation-report.txt

reference-validate-r0:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_R0_DIR)/references.bib --output $(MANUSCRIPT_R0_DIR)/reference-validation-report.txt

reference-validate-r1:
	$(PYTHON) scripts/validate_references.py --bib $(MANUSCRIPT_R1_DIR)/references.bib --output $(MANUSCRIPT_R1_DIR)/reference-validation-report.txt

reference-validate-suggest:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_DIR)/references.bib --output $(MANUSCRIPT_DIR)/reference-validation-report.txt

reference-validate-suggest-r0:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_R0_DIR)/references.bib --output $(MANUSCRIPT_R0_DIR)/reference-validation-report.txt

reference-validate-suggest-r1:
	$(PYTHON) scripts/validate_references.py --suggest-doi --bib $(MANUSCRIPT_R1_DIR)/references.bib --output $(MANUSCRIPT_R1_DIR)/reference-validation-report.txt

notebook: data
	$(PYTHON) -m jupyter nbconvert --to notebook --execute notebooks/dbhdistfit_truncdata.ipynb --output dbhdistfit_truncdata.executed.ipynb --output-dir notebooks

repro: figures tables notebook manuscript

clean:
	rm -rf figures/* tables/* $(MANUSCRIPT_R0_DIR)/build $(MANUSCRIPT_R1_DIR)/build notebooks/*.executed.ipynb preprint/*.pdf em-submission/*.pdf em-submission/*.zip tmp/*
