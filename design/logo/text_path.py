# -*- coding: utf-8 -*-
"""Convert a text run to SVG outlines so it renders without the font installed."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

def text_to_path(s, font_path, size, x=0.0, y=0.0, tracking=0.0):
    """Baseline-anchored at (x,y). Returns (path_d, advance_width)."""
    f = TTFont(font_path, fontNumber=0)
    upm = f['head'].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f['hmtx']
    scale = size/upm
    cur = x
    parts=[]
    for ch in s:
        if ord(ch) not in cmap:
            cur += size*0.5 + tracking
            continue
        name = cmap[ord(ch)]
        g = gs[name]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        t = Transform(scale, 0, 0, -scale, cur, y)
        g.draw(TransformPen(pen, t))
        cmds = pen.getCommands()
        if cmds:
            parts.append(cmds)
        adv = hmtx[name][0]*scale
        cur += adv + tracking
    return ' '.join(parts), cur - x
