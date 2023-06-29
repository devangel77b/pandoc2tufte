#!/usr/bin/env python3
"""
newthought Pandoc filter implemented in panflute
Dennis Evangelista (2023)

Raw input markdown
<span class="newthought>Tufte books start with</span>
becomes
(Span Para([Str(Tufte) Space Str(books)...]); classes=['newthought'])
becomes
\newthought{Tufte books start with}

Example call (when called from command line):
  pandoc input.md --filter newthought.py --to=latex

Or in other filters you access the filter action directly:
  import newthought
  newthought.to_latex(e,doc)
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
    :return: If the element is not <span class="newthought">...</span>,
         returns None. Otherwise it returns a list containing
         panflute.RawInline of \newthought{...} for use in latex.
         If we're not looking for latex (doc.format is not latex)
         then it returns None. 
    :rtype: None or list of inline elements
    """
    if (doc.format == "latex"):
        if (isinstance(e,pf.Span)):
            if ('newthought' in e.classes):
                l = e.content
                l.insert(0,pf.RawInline("\\newthought{",format="latex"))
                l.append(pf.RawInline("}",format="latex"))
                logging.debug("{0} becomes {1}".format(e,l.list))
                return(l.list)

def main(doc=None):
    return(pf.run_filter(newthought2latex,doc))

if __name__ == "__main__":
    main()
