#!/usr/bin/env python3

import panflute as pf
import parse
import logging
#logging.basicConfig(level=logging.DEBUG)

D={'AlignLeft':'l', 'AlignCenter':'c', 'AlignRight':'r','AlignDefault':'c'}

class TableProcessor():
    def __init__(self):
        self.active=False
        self.l=[]
        self.e=None
    def consume(self,e):
        if (e==pf.RawBlock('<figure class="table">',format='html')):
            self.l = [pf.RawBlock('\\begin{table}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{table}',format='latex')
            #logging.debug(e)
            self.active=True
            return([])
        elif ((e==pf.RawBlock(
                '<figure class="table-fullwidth">',format='html')) or
              (e==pf.RawBlock('<figure class="table*">',format='html'))):
            self.l = [pf.RawBlock('\\begin{table*}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{table*}',format='latex')
            #logging.debug(e)
            self.active=True
            return([])
        elif (e==pf.RawBlock('<figure class="margintable">',format='html')):
            self.l = [pf.RawBlock('\\begin{margintable}',format='latex')]
            self.e = pf.RawBlock('\033[A\\end{margintable}',format='latex')
            #logging.debug(e)
            self.active=True
            return([])
        elif (self.active and isinstance(e,pf.Figure)):
            #logging.debug(e)
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
        elif (self.active and isinstance(e,pf.Table)):
            #logging.debug(e)
            # check if last bit is the label
            rv = parse.parse("{{#{lab}}}",
                             pf.stringify(e.caption.content[-1].content[-1]))
            if rv:
                e.identifier=rv['lab']
                e.caption.content[-1].content.pop(-1)
            while e.caption.content[-1].content[-1]==pf.Space():
                e.caption.content[-1].content.pop(-1)
            #if e.identifier:
            #    self.l.append(pf.RawBlock(
            #        '\033[A\\hypertarget{'+e.identifier+'}{%',
            #        format='latex'))
            # handle caption
            e.caption.content[0].content.insert(0,
                                                pf.RawInline(
                                                    '\033[A\\caption{',
                                                    format='latex'))
            
            e.caption.content[-1].content.append(
                pf.RawInline('}',format='latex'))
            for p in e.caption.content:
                self.l.append(p)
            # handle label
            if e.identifier:
                self.l.append(pf.RawBlock(
                    '\033[A\\label{'+e.identifier+'}',format='latex'))
            # make the tabular
            colspec = ''.join([D[x[0]] for x in e.colspec])
            self.l.append(pf.RawBlock(
                '\033[A\\begin{tabular}{'+colspec+'}',
                format='latex'))
            self.l.append(pf.RawBlock('\033[A\\toprule',format='latex'))
            # process head here
            for row in e.head.content:
                rowl = [pf.RawInline('\033[A',format='latex')]
                for tabelem in row.content:
                    for plainelem in tabelem.content:
                        rowl.extend(plainelem.content)
                        if tabelem.next:
                            rowl.append(pf.RawInline(' & ',format='latex'))
                        else:
                            rowl.append(pf.RawInline(' \\\\',format='latex'))
                        #logging.debug(rowl)
                self.l.append(pf.Plain(*rowl))
                self.l.append(pf.RawBlock('\033[A\\midrule',format='latex'))
            # process body here
            #logging.debug(e.content[0].content)
            for row in e.content[0].content:
                rowl = [pf.RawInline('\033[A',format='latex')]
                for tabelem in row.content:
                    for plainelem in tabelem.content:
                        rowl.extend(plainelem.content)
                        if tabelem.next:
                            rowl.append(pf.RawInline(' & ',format='latex'))
                        else:
                            rowl.append(pf.RawInline(' \\\\',format='latex'))
                        #logging.debug(rowl)
                self.l.append(pf.Plain(*rowl))
            self.l.append(pf.RawBlock('\033[A\\bottomrule',format='latex'))
            #if e.identifier:
            #    self.l.append(pf.RawBlock(
            #    '\033[A\\end{tabular}}',format='latex'))
            #else:
            self.l.append(pf.RawBlock(
                '\033[A\\end{tabular}',format='latex'))
            return([])
        elif (self.active and (e==pf.RawBlock('</figure>',format='html'))):
            #logging.debug(e)
            self.l.append(self.e)
            self.active=False
            return(self.l)
        else:
            pass
    def to_latex(self,e,doc):
        if (doc.format=='latex'):
            return(self.consume(e))
       
table_processor = TableProcessor()
to_latex = table_processor.to_latex

def main(doc=None):
    return(pf.run_filter(to_latex,doc))

if __name__ == "__main__":
    main()
