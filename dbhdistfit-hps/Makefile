SHELL := /bin/bash
PYTHON ?= python

.PHONY: help env data figures tables manuscript title-page cover-letter em-submission notebook repro clean

help:
	@echo "Available targets:"
	@echo "  make env         - create/refresh the virtual environment (optional hook)"
	@echo "  make figures     - generate all manuscript figures into figures/"
	@echo "  make tables      - generate all manuscript tables into tables/"
	@echo "  make manuscript  - compile the LaTeX manuscript PDF"
	@echo "  make title-page  - compile the Forest Science title page PDF"
	@echo "  make cover-letter - compile the submission cover letter PDF"
	@echo "  make em-submission- build flat Editorial Manager package (dir + zip)"
	@echo "  make notebook    - execute the reproducible notebook"
	@echo "  make repro       - run end-to-end reproducibility pipeline"
	@echo "  make clean       - remove derived outputs"

env:
	@if [ ! -d .venv ]; then $(PYTHON) -m venv .venv; fi
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

data:
	@if command -v datalad >/dev/null 2>&1; then \
		datalad get data/interim/tiges_final_full.p data/interim/essencegroupe1.csv data/interim/groupe1groupe2groupe3.csv >/dev/null 2>&1 || true; \
	fi
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
	$(MAKE) -C manuscript cover-letter

em-submission: figures tables manuscript title-page cover-letter
	$(PYTHON) scripts/prepare_em_submission.py

notebook: data
	$(PYTHON) -m jupyter nbconvert --to notebook --execute notebooks/hpsdistfit_repro.ipynb --output hpsdistfit_repro.executed.ipynb --output-dir notebooks

repro: figures tables notebook manuscript

clean:
	rm -rf figures/* tables/* manuscript/build notebooks/*.executed.ipynb
