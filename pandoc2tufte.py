#!/usr/bin/env python3
"""
Pandoc to tufte-latex filters implemented in panflute
Dennis Evangelista (2023)

* newthought
* sidenote (plus marginnote and footnote)
* blockquote footer (new environment not in tufte-latex)
* epigraph (new environment not in tufte-latex)
* code escaping (requires minted package in latex)

These should be run *after* running pandoc-crossref and --natbib?
Each filter can also be used on its own. 

Already built-in to pandoc: 
* blockquote (becomes quote environment)
* href and url links
* cross references (use pandoc --filter pandoc-crossref)
* bibliography (use pandoc --natbib)

Todo:
* <figure> as floats (figures, tables) plus marginfigure and margintable
* images [!caption here]{image.png} as \includegraphics
* tables wtf simple works but maybe start doing standalone... 
"""

import panflute as pf
import newthought
import sidenote
import footer
import epigraph
import code
import logging
#logging.basicConfig(level=logging.DEBUG)

def dummy_action(e,doc):
    pass

def main(doc=None):
    return pf.run_filters([newthought.to_latex,
                           sidenote.to_latex,
                           footer.to_latex,
                           epigraph.to_latex,
                           code.to_latex,
                           ],doc)

if __name__ == "__main__":
    main()
    
