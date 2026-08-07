# -*- coding: utf-8 -*-
import os, base64, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Q=chr(34); FF='LXGW WenKai, PingFang SC, sans-serif'
def embed(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
def tag(n,**kw): return '<'+n+' '+' '.join(k.replace('_','-')+'='+Q+str(v)+Q for k,v in kw.items())+'/>'
def txt(x,y,s,c,t,anchor=None):
    a=' text-anchor='+Q+anchor+Q if anchor else ''
    return '<text x='+Q+str(x)+Q+' y='+Q+str(y)+Q+' font-family='+Q+FF+Q+' font-size='+Q+str(s)+Q+' fill='+Q+c+Q+a+'>'+t+'</text>'

W=1500; H=980
p=['<svg xmlns='+Q+'http://www.w3.org/2000/svg'+Q+' width='+Q+str(W)+Q+' height='+Q+str(H)+Q+' viewBox='+Q+'0 0 '+str(W)+' '+str(H)+Q+'>',
   tag('rect',width=W,height=H,fill='#ffffff'),
   txt(50,56,34,'#2e405b','「周振坤印」· 已完成并接入站点'),
   txt(50,86,19,'#7c8794','霞鹜文楷字形 · 朱红 #9e3d33 · 全部为矢量图形')]

y0=118
# main seal
p.append(tag('rect',x=50,y=y0,width=330,height=330,rx=8,fill='#fbfaf7',stroke='#e6e2da',stroke_width=1.5))
p.append(tag('image',x=70,y=y0+20,width=290,height=290,href=embed('final/png/seal-zhouzhenkun@1024.png')))
p.append(txt(50,y0+368,24,'#1d2a3d','主印 · 四字方印'))
p.append(txt(50,y0+396,17,'#7c8794','页头 / 文章落款 / 名片'))

# single mark
p.append(tag('rect',x=420,y=y0,width=250,height=250,rx=8,fill='#fbfaf7',stroke='#e6e2da',stroke_width=1.5))
p.append(tag('image',x=440,y=y0+20,width=210,height=210,href=embed('final/favicon/mark-512.png')))
p.append(txt(420,y0+288,24,'#1d2a3d','小印 · 单字「周」'))
p.append(txt(420,y0+316,17,'#7c8794','favicon / 头像'))

# variants column
vx=710
p.append(txt(vx,y0+18,22,'#1d2a3d','其他版本'))
for i,(f,lab) in enumerate([('final/png/seal-zhouzhenkun-ink@1024.png','墨色单色版'),
                             ('final/png/seal-zhouzhenkun-transparent@1024.png','透明镂空版')]):
    bx=vx+i*195
    p.append(tag('rect',x=bx,y=y0+38,width=175,height=175,rx=6,fill='#fbfaf7',stroke='#e6e2da',stroke_width=1.5))
    p.append(tag('image',x=bx+15,y=y0+53,width=145,height=145,href=embed(f)))
    p.append(txt(bx,y0+238,17,'#7c8794',lab))

# favicon real sizes
fy=y0+290
p.append(txt(vx,fy,22,'#1d2a3d','浏览器标签实际大小'))
xx=vx
for s in [16,32,48,64]:
    p.append(tag('image',x=xx,y=fy+20,width=s,height=s,href=embed('final/favicon/mark-%d.png'%s)))
    p.append(txt(xx,fy+20+s+18,15,'#9aa4b0',str(s)+'px'))
    xx+=s+34

# lockup
ly=y0+430
p.append(txt(50,ly,24,'#1d2a3d','横版组合 · 印 + 姓名'))
p.append(tag('rect',x=50,y=ly+18,width=880,height=290,rx=8,fill='#fbfaf7',stroke='#e6e2da',stroke_width=1.5))
p.append(tag('image',x=90,y=ly+50,width=800,height=226,href=embed('final/png/lockup-horizontal@1024.png')))

p.append('</svg>')
open('_final.svg','w').write('\n'.join(p))
subprocess.run(['rsvg-convert','-w',str(W),'_final.svg','-o','final/png/showcase.png'],check=True)
print('ok')
