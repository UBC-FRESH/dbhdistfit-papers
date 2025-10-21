(TeX-add-style-hook
 "hpsdistfit_article"
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
    "hyperref")
   (LaTeX-add-labels
    "sec:introduction"
    "sec:methods"
    "sec:results"
    "fig:results"
    "tab:rss"
    "sec:discussion"
    "sec:conclusion")
   (LaTeX-add-bibliographies
    "../pdf.bib")))

