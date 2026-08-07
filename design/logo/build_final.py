# -*- coding: utf-8 -*-
"""Final S1 seal asset set: 周振坤印"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glyph2 import cell_path

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, 'final')
os.makedirs(OUT, exist_ok=True)

CINNABAR = '#9e3d33'
PAPER    = '#f7f5f0'
WHITE    = '#ffffff'
INK      = '#1d2a3d'

CHARS = ['周', '振', '坤', '印']
ORDER = [(0,0), (0,1), (1,0), (1,1)]   # (col_from_right, row)

def grid(margin=30, gap=5.0, fill=PAPER, pad=3.0, font='wenkai-m', VB=256):
    inner = VB - 2*margin
    cell  = (inner - gap) / 2.0
    out=[]
    for ch,(colr,row) in zip(CHARS, ORDER):
        cx = margin + (1-colr)*(cell+gap)
        cy = margin + row*(cell+gap)
        d = cell_path(ch, font=font, w=cell, h=cell, mode='fill', pad=pad)
        out.append(f'  <g transform="translate({cx:.2f} {cy:.2f})"><path d="{d}" fill="{fill}"/></g>')
    return '\n'.join(out)

def svg256(body, label='周振坤印'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" '
            f'width="256" height="256" role="img" aria-label="{label}">\n{body}\n</svg>\n')

def wr(name, s):
    open(os.path.join(OUT,name),'w').write(s)

# 1. MASTER — 朱文方印, 红底白字
wr('seal-zhouzhenkun.svg', svg256(
  f'  <rect x="6" y="6" width="244" height="244" rx="22" fill="{CINNABAR}"/>\n'
  + grid()))

# 2. 单字小印「周」 — for favicon / small sizes
d = cell_path('周', font='wenkai-m', w=150, h=150, mode='fill', pad=0)
wr('seal-zhou-mark.svg', svg256(
  f'  <rect x="6" y="6" width="244" height="244" rx="22" fill="{CINNABAR}"/>\n'
  f'  <g transform="translate(53 53)"><path d="{d}" fill="{PAPER}"/></g>', '周'))

# 3. 单色墨版（深色/单色印刷用）
wr('seal-zhouzhenkun-ink.svg', svg256(
  f'  <rect x="6" y="6" width="244" height="244" rx="22" fill="{INK}"/>\n'
  + grid(fill=WHITE)))

# 4. 透明底 · 镂空字（可叠在任意背景，红章）
#    用 mask 让字真正透出背景
inner_grid = grid(fill='#000000')
wr('seal-zhouzhenkun-transparent.svg',
   '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-label="周振坤印">\n'
   '  <defs>\n    <mask id="cut">\n'
   '      <rect x="6" y="6" width="244" height="244" rx="22" fill="#fff"/>\n'
   + inner_grid + '\n    </mask>\n  </defs>\n'
   f'  <rect x="6" y="6" width="244" height="244" rx="22" fill="{CINNABAR}" mask="url(#cut)"/>\n'
   '</svg>\n')

# 5. 横版组合：印 + 站点名（页头/落款用）
#    文字全部转为轮廓，避免依赖本机字体
from text_path import text_to_path
WK_M = '/Users/Kay/Library/Fonts/LXGWWenKai-Medium.ttf'
WK_R = '/Users/Kay/Library/Fonts/LXGWWenKai-Regular.ttf'
GREY = '#7c8794'

SEAL = 150.0
sc   = SEAL / 256.0
PAD  = 28.0
seal_x = seal_y = PAD
tx = seal_x + SEAL + 34
cn_d, cn_w = text_to_path('周振坤', WK_M, 54, tx, seal_y + 72)
en_d, en_w = text_to_path('ZHENKUN ZHOU', WK_R, 24, tx, seal_y + 120, tracking=2.6)
LW = int(max(tx + cn_w, tx + en_w) + PAD)
LH = int(SEAL + PAD * 2)

wr('lockup-horizontal.svg',
   f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LW} {LH}" '
   f'width="{LW}" height="{LH}" role="img" aria-label="周振坤 · 周振坤印">\n'
   f'  <g transform="translate({seal_x} {seal_y}) scale({sc:.5f})">\n'
   f'    <rect x="6" y="6" width="244" height="244" rx="22" fill="{CINNABAR}"/>\n'
   + grid() + '\n  </g>\n'
   f'  <path d="{cn_d}" fill="{INK}"/>\n'
   f'  <path d="{en_d}" fill="{GREY}"/>\n'
   '</svg>\n')

print('built', sorted(os.listdir(OUT)))
