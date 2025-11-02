(TeX-add-style-hook
 "pspdistfit_article"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("siunitx" "binary-units") ("lineno" "running")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "inputenc"
    "graphicx"
    "booktabs"
    "siunitx"
    "lineno"
    "setspace"
    "authblk"
    "natbib"
    "amsmath"
    "amssymb"
    "bm"
    "hyperref"
    "subcaption"
    "mathtools")
   (LaTeX-add-labels
    "sec:introduction"
    "sec:methods"
    "eq:z"
    "sec:results"
    "fig:results1"
    "fig:results2"
    "tab:results"
    "sec:discussion"
    "sec:conclusion"
    "tab:a_speciesgroups")
   (LaTeX-add-bibliographies
    "../pdf.bib")))

