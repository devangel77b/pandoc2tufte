# `pandoc2tufte` filters in Python
### D Evangelista

This is for converting from Pandoc markdown to tufte-latex, in order to
support using Pandoc to write things with PDF output via tufte-latex as 
well as html and epub output via tufte.css. 

As example of use:

```bash
pandoc input.md --filter pandoc2tufte.py
```

## Conversions

1. newthought: `<span class="newthought"></span>` to `\newthought{}`
2. 
# pandoc2tufte
