.PHONY: help $(REPRO_RULES)
.DEFAULT_GOAL := help

SUBPROJECTS := dbhdistfit-hps dbhdistfit-truncdata
REPRO_RULES := $(SUBPROJECTS:%=%-repro)

help:
	@echo "Available targets:"
	@echo "  make dbhdistfit-hps-repro        - run full reproducibility pipeline for dbhdistfit-hps"
	@echo "  make dbhdistfit-truncdata-repro  - run full reproducibility pipeline for dbhdistfit-truncdata"

$(REPRO_RULES):
	$(MAKE) -C $(patsubst %-repro,%,$@) repro
