#!/usr/bin/env python3

import panflute as pf
import parse
import dateutil.parser

#import logging
#logging.basicConfig(level=logging.DEBUG)


# if we have an e that looks like e.g. \qty{1}{\joule} and we aren't
# going for latex output, then we need to convert it using pandoc.  
def latex_printdate(e,doc):
    if (type(e)==pf.RawInline) and (doc.format!="latex"): # or pdf? 
        if e.format == 'tex':
            md_str = e.text
            #logging.debug(md_str)
            if (rv := parse.parse("\\printdate{{{s}}}",md_str)):
                if 's' in rv:
                    o = dateutil.parser.parse(rv['s']).strftime("%B %-d, %Y")
                    return pf.Str(o)
        
if __name__ == "__main__":
    pf.run_filter(latex_printdate)

