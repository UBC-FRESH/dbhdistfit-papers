LATEXMK ?= latexmk
LATEX_FLAGS ?= -pdf -interaction=nonstopmode -file-line-error

.PHONY: all clean

all: main.pdf

main.pdf: main.tex
	$(LATEXMK) $(LATEX_FLAGS) main.tex

clean:
	$(LATEXMK) -C main.tex
