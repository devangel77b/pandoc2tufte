#!/usr/bin/env python3

import panflute as pf
import logging
#logging.basicConfig(level=logging.DEBUG)

class FigureProcessor():
    def __init__(self):
        self.active=False
        self.l=[]
        self.e=None
    def consume(self,e):
        if ((e==pf.RawBlock('<figure>',format='html')) or
            (e==pf.RawBlock('<figure class="figure">',format='html'))):
            self.l = [pf.RawBlock('\\begin{figure}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{figure}',format='latex')
            logging.debug(e)
            self.active=True
            return([])
        elif ((e==pf.RawBlock('<figure class="fullwidth">',format='html')) or
              (e==pf.RawBlock('<figure class="figure*">',format='html'))):
            self.l = [pf.RawBlock('\\begin{figure*}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{figure*}',format='latex')
            logging.debug(e)
            self.active=True
            return([])
        elif (e==pf.RawBlock('<figure class="marginfigure">',format='html')):
            self.l = [pf.RawBlock('\\begin{figure*}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{figure*}',format='latex')
            logging.debug(e)
            self.active=True
            return([])
        elif (self.active and isinstance(e,pf.Figure)):
            logging.debug(e)
            #if e.identifier:
            #    self.l.append(pf.RawBlock(
            #        '\033[A\\hypertarget{'+e.identifier+'}{%',
            #        format='latex'))
            e.caption.content[0].content.insert(0,
                                                pf.RawInline(
                                                    '\033[A\\caption{',
                                                    format='latex'))
            e.caption.content[-1].content.append(
                pf.RawInline('}',format='latex'))
            for p in e.caption.content:
                self.l.append(p)
            if e.identifier:
                self.l.append(pf.RawBlock(
                    '\033[A\\label{'+e.identifier+'}',format='latex'))
            #if e.identifier:
            #    self.l.append(pf.RawBlock('\033[A\\includegraphics{'+
            #                              e.content[0].content[0].url+
            #                              '}}',format='latex'))
            #else:
            self.l.append(pf.RawBlock('\033[A\\includegraphics{'+
                                      e.content[0].content[0].url+
                                      '}',format='latex'))
            return([])
        elif (self.active and (e==pf.RawBlock('</figure>',format='html'))):
            logging.debug(e)
            self.l.append(self.e)
            self.active=False
            return(self.l)
        else:
            pass
    def to_latex(self,e,doc):
        if (doc.format=='latex'):
            return(self.consume(e))
       
figure_processor = FigureProcessor()
to_latex = figure_processor.to_latex

def main(doc=None):
    return(pf.run_filter(to_latex,doc))

if __name__ == "__main__":
    main()
