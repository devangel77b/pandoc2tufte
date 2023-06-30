#!/usr/bin/env python3
"""
Pandoc to tufte-latex filters implemented in panflute
Dennis Evangelista (2023)

* newthought
* sidenote (plus marginnote and footnote)
* blockquote footer (new environment not in tufte-latex)
* epigraph (new environment not in tufte-latex)
* code escaping (requires minted package in latex)
* <figure> as floats (figures, tables) plus marginfigure and margintable

These should be run *after* running pandoc-crossref and --natbib?
Each filter can also be used on its own; running filter pandoc2tufte
runs them all in sequence. 

Already built-in to pandoc: 
* blockquote (becomes quote environment)
* href and url links
* cross references (use pandoc --filter pandoc-crossref)
* bibliography (use pandoc --natbib)
* images [!caption here]{image.png} as \includegraphics
* tables wtf simple works but maybe start doing standalone... 

Todo:
* run tabletest.md and check
* check image widths. what to do with this?
* might have to add case in figure.py for html/xml/epub output
"""

import panflute as pf
import newthought
import sidenote
import footer
import epigraph
import code
import figure
import logging
#logging.basicConfig(level=logging.DEBUG)

def main(doc=None):
    return pf.run_filters([newthought.to_latex,
                           sidenote.to_latex,
                           footer.to_latex,
                           epigraph.to_latex,
                           code.to_latex,
                           figure.to_latex,
                           ],doc)

if __name__ == "__main__":
    main()
    
