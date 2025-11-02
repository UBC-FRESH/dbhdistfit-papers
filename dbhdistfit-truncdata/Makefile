SHELL := /bin/bash
PYTHON ?= python

.PHONY: help env data figures tables manuscript title-page cover-letter preprint em-submission notebook repro clean

help:
	@echo "Targets:"
	@echo "  make env          - create/refresh virtual environment"
	@echo "  make data         - preprocess PSP tallies for truncated analysis"
	@echo "  make figures      - regenerate all figures"
	@echo "  make tables       - regenerate all tables"
	@echo "  make manuscript   - compile LaTeX manuscript"
	@echo "  make title-page   - compile journal title page"
	@echo "  make cover-letter - compile submission cover letter"
	@echo "  make preprint     - build EarthArXiv-ready PDF"
	@echo "  make em-submission- build Editorial Manager package"
	@echo "  make notebook     - execute reproducibility notebook(s)"
	@echo "  make repro        - run full reproducibility pipeline"
	@echo "  make clean        - remove generated artefacts"

env:
	@if [ ! -d .venv ]; then $(PYTHON) -m venv .venv; fi
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

data:
	$(PYTHON) scripts/preprocess_data.py

figures: data
	$(PYTHON) scripts/generate_figures.py --config config/figures.yml

tables: data
	$(PYTHON) scripts/generate_tables.py --config config/tables.yml

manuscript:
	$(MAKE) -C manuscript all

title-page:
	$(MAKE) -C manuscript title-page

cover-letter:
	@test -f manuscript/cover-letter.txt || (echo "cover-letter.txt missing" && exit 1)

preprint: figures tables manuscript
	$(PYTHON) scripts/build_preprint.py

em-submission: figures tables manuscript title-page cover-letter
	$(PYTHON) scripts/prepare_em_submission.py

notebook: data
	$(PYTHON) -m jupyter nbconvert --to notebook --execute notebooks/dbhdistfit_truncdata.ipynb --output dbhdistfit_truncdata.executed.ipynb --output-dir notebooks

repro: figures tables notebook manuscript

clean:
	rm -rf figures/* tables/* manuscript/build notebooks/*.executed.ipynb preprint/*.pdf em-submission/*.pdf em-submission/*.zip tmp/*
