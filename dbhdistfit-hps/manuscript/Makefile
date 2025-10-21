LATEXMK ?= latexmk

.PHONY: all clean

all:
	$(LATEXMK) -pdf -interaction=nonstopmode -file-line-error main.tex

clean:
	$(LATEXMK) -C
