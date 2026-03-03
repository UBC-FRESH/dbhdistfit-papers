LATEXMK ?= latexmk
LATEX_FLAGS ?= -pdf -interaction=nonstopmode -file-line-error

.PHONY: all appendix clean

all: main.pdf

main.pdf: main.tex
	$(LATEXMK) $(LATEX_FLAGS) main.tex

appendix: appendix.pdf

appendix.pdf: appendix.tex
	$(LATEXMK) $(LATEX_FLAGS) appendix.tex

clean:
	$(LATEXMK) -C main.tex
	$(LATEXMK) -C appendix.tex
