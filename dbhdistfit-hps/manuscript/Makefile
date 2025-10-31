LATEXMK ?= latexmk
LATEX_FLAGS ?= -pdf -interaction=nonstopmode -file-line-error

.PHONY: all clean title-page cover-letter em-submission em-submission-zip

all: main.pdf

main.pdf: main.tex
	$(LATEXMK) $(LATEX_FLAGS) main.tex

title-page: title-page.pdf

title-page.pdf: title-page.tex
	$(LATEXMK) $(LATEX_FLAGS) title-page.tex

cover-letter: cover-letter.pdf

cover-letter.pdf: cover-letter.tex
	$(LATEXMK) $(LATEX_FLAGS) cover-letter.tex

em-submission: ../em-submission.zip

em-submission-zip: ../em-submission.zip

../em-submission.zip:
	$(MAKE) -C .. em-submission

clean:
	$(LATEXMK) -C main.tex
	$(LATEXMK) -C title-page.tex
	$(LATEXMK) -C cover-letter.tex
