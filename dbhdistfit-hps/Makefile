SHELL := /bin/bash
PYTHON ?= python

.PHONY: help env figures tables manuscript notebook repro clean

help:
	@echo "Available targets:"
	@echo "  make env         - create/refresh the virtual environment (optional hook)"
	@echo "  make figures     - generate all manuscript figures into figures/"
	@echo "  make tables      - generate all manuscript tables into tables/"
	@echo "  make manuscript  - compile the LaTeX manuscript PDF"
	@echo "  make notebook    - execute the reproducible notebook"
	@echo "  make repro       - run end-to-end reproducibility pipeline"
	@echo "  make clean       - remove derived outputs"

env:
	@if [ ! -d .venv ]; then $(PYTHON) -m venv .venv; fi
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

figures:
	$(PYTHON) scripts/generate_figures.py --config config/figures.yml

tables:
	$(PYTHON) scripts/generate_tables.py --config config/tables.yml

manuscript:
	$(MAKE) -C manuscript all

notebook:
	$(PYTHON) -m jupyter nbconvert --to notebook --execute notebooks/hpsdistfit_repro.ipynb --output hpsdistfit_repro.executed.ipynb --output-dir notebooks

repro: figures tables notebook manuscript

clean:
	rm -rf figures/* tables/* manuscript/build notebooks/*.executed.ipynb
