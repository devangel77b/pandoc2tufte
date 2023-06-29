#!/usr/bin/env python3
"""
sidenote, marginnote, footnot pandoc filter implemented in panflute
Dennis Evangelista (2023)

Raw input markdown
[^sn]: this is a sidenote
becomes
\sidenote{this is a sidenote}

Similarly:
[^mn]: {-} this is a marginnote
[^fn]: {.} this is a footnote

Example call (when called from command line):
  pandoc input.md --filter newthought.py --to=latex

Or in other filters you access the filter action directly:
  import newthought
  newthought.to_latex(e,doc)
"""

import panflute as pf
import logging
#logging.basicConfig(level=logging.DEBUG)


def to_latex(e, doc):
    """convert a Note to \sidenote{}, \marginnote, or \footnote
    as appropriate

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

    Since Note is an Inline, pandoc expects Inline return, which is odd
    because the stuff inside the note can be paragraphs. To accomplish
    this, we return a list with the content of the element (several paragraphs)
    connected by panflute.RawInline("\n\n"), so that the latex output is
    broken into paragraphs but it can still let pandoc fillin things it
    needs to like \textbf, \emph, math, href? and cite? . 
    """
    if (doc.format == "latex"):
        if (isinstance(e,pf.Note)):
            if len(e.content)==0:
                logging.debug("{0} becomes \sidenote{{}}".format(e))
                return(pf.RawInline("\\sidenote{}",format="latex"))
            else:
                l = []
                if (e.content[0].content[0]==pf.Str("{-}")):
                    l.append(pf.RawInline("\\marginnote{",format="latex"))
                    e.content[0].content.pop(0)
                elif (e.content[0].content[0]==pf.Str("{.}")):
                    l.append(pf.RawInline("\\footnote{",format="latex"))
                    e.content[0].content.pop(0)
                else:
                    if (len(e.content)>1):
                        l.append(pf.RawInline("\\sidnote{%\n",format="latex"))
                    else:
                        l.append(pf.RawInline("\\sidenote{",format="latex"))
                
                for p in e.content:
                    # remove leading spaces cuz theyre annoying
                    while (p.content[0]==pf.Space()):
                        p.content.pop(0)

                    l.extend(p.content.list)
                    if p.next:
                        l.append(pf.RawInline("\n\n",format="latex"))
                
                l.append(pf.RawInline("}",format="latex"))
                logging.debug("{0} becomes {1}".format(e,l))
                return(l)

def main(doc=None):
    return pf.run_filter(to_latex,doc)
            
if __name__ == "__main__":
    main()
    
