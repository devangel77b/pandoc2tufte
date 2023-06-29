#!/usr/bin/env python3
"""
footer Pandoc filter implemented in panflute
Dennis Evangelista (2023)

Raw input markdown
<footer>
blah
</footer>
becomes
RawBlock(<footer>") Para([Str(blah)]) RawBlock(</footer>
becomes
\begin{blockquotefooter}
Blah
\end{blockquotefooter}

Example call (when called from command line):
  pandoc input.md --filter footer.py --to=latex

Or in other filters you access the filter action directly:
  import footer
  footer.to_latex(e,doc)
"""

import panflute as pf
import logging
#logging.basicConfig(level=logging.DEBUG)

def to_latex(e,doc):
    """panflute filter action for converting markdown newthought to latex

    Positional arguments:
    :param e: the element being processed, e.g. by panflute walk
    :type e: panflute.Element
    :param doc: the document being processed (handled by panflute)
    :type doc: panflute.Doc
    :return: If the element is not <footer>...</footer>
    returns None. Otherwise it returns latex versions as needed, i.e.
    \begin{blockquotefooter} or \end{blockquotefooter}.
    If we're not looking for latex (doc.format is not latex)
    then it returns None. 
    :rtype: None or list of Block elements
    """
    if (doc.format=="latex"):
        if (e == pf.RawBlock("<footer>",format="html")):
            return pf.RawBlock(
                "\\begin{blockquotefooter}\033[A",format="latex")
        elif (e==pf.RawBlock("</footer>",format="html")):
            if (e.prev == pf.RawBlock("<footer>",format="html")):
                return pf.RawBlock("\\end{blockquotefooter}",format="latex")
            else:
                return pf.RawBlock(
                    "\033[A\\end{blockquotefooter}",format="latex")

def main(doc=None):
    return(pf.run_filter(to_latex,doc))

if __name__ == "__main__":
    main()
