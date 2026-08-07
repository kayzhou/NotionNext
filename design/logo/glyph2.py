# -*- coding: utf-8 -*-
"""Extract glyph outlines and fit them into a seal cell."""
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttCollection import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

FONTS = {
 'wenkai-m':  '/Users/Kay/Library/Fonts/LXGWWenKai-Medium.ttf',
 'wenkai-r':  '/Users/Kay/Library/Fonts/LXGWWenKai-Regular.ttf',
 'kaiti':     '/Users/Kay/Library/Fonts/DFKai SB.ttf',
 'fangsong':  '/Users/Kay/Library/Fonts/仿宋_GB2312.ttf',
 'simsun':    '/Users/Kay/Library/Fonts/SimSun.ttf',
}
_cache = {}

def _font(key):
    if key not in _cache:
        _cache[key] = TTFont(FONTS[key], fontNumber=0)
    return _cache[key]

def cell_path(char, font='wenkai-m', w=100.0, h=100.0, mode='fill', pad=0.0):
    """Fit `char` into a w x h cell. mode='fill' stretches (seal style),
    'fit' preserves aspect. Returns SVG path data, y-down coords."""
    f = _font(font)
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord(char)]
    g = gs[name]
    bp = BoundsPen(gs); g.draw(bp)
    x0, y0, x1, y1 = bp.bounds
    gw, gh = x1 - x0, y1 - y0
    tw, th = w - 2*pad, h - 2*pad
    if mode == 'fill':
        sx, sy = tw/gw, th/gh
    else:
        s = min(tw/gw, th/gh); sx = sy = s
    dx = pad + (tw - gw*sx)/2.0
    dy = pad + (th - gh*sy)/2.0
    # flip y (font y-up -> svg y-down)
    t = Transform(sx, 0, 0, -sy, -x0*sx + dx, y1*sy + dy)
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
    g.draw(TransformPen(pen, t))
    return pen.getCommands()

if __name__ == '__main__':
    for fk in FONTS:
        try:
            d = cell_path('印', fk)
            print(fk, 'OK', len(d))
        except Exception as e:
            print(fk, 'ERR', e)
