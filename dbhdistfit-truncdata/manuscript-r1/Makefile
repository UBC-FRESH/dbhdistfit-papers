LATEXMK ?= latexmk
LATEX_FLAGS ?= -pdf -interaction=nonstopmode -file-line-error

.PHONY: all clean title-page cover-letter preprint

all:
	$(LATEXMK) $(LATEX_FLAGS) main.tex

title-page:
	$(LATEXMK) $(LATEX_FLAGS) title-page.tex

cover-letter:
	$(LATEXMK) $(LATEX_FLAGS) cover-letter.tex

clean:
	$(LATEXMK) -C main.tex
	$(LATEXMK) -C title-page.tex
	$(LATEXMK) -C cover-letter.tex
