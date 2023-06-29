#!/usr/bin/env python3
"""
footer Pandoc filter implemented in panflute
Dennis Evangelista (2023)

Raw input markdown
<div class="epigraph">
blah
</div>
becomes
Div(..., classes=['epigraph'])
becomes
\begin{epigraph}
...
\end{epigraph}

Example call (when called from command line):
  pandoc input.md --filter epigraph.py --to=latex

Or in other filters you access the filter action directly:
  import epigraph
  epigraph.to_latex(e,doc)
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
    :return: If the element is not <div class="epigraph">...</div>
    returns None. Otherwise it returns latex versions as needed, i.e.
    \begin{epigraph} or \end{epigraph}.
    If we're not looking for latex (doc.format is not latex)
    then it returns None. 
    :rtype: None or list of Block elements
    """
    if (doc.format == "latex"):
        if (isinstance(e,pf.Div)):
            if ("epigraph" in e.classes):
                e.content.insert(0,pf.RawBlock(
                    "\\begin{epigraph}\033[A",format="latex"))
                e.content.append(pf.RawBlock(
                    "\033[A\\end{epigraph}",format="latex"))
                logging.debug("epigraph becomes {0}".format(e))
                pass

def main(doc=None):
    return pf.run_filter(to_latex, doc)

if __name__ == "__main__":
    main()

