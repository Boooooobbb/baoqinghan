#!/usr/bin/env python3
"""Build static pages for GitHub Pages and mirror deployable files into dist/."""
from pathlib import Path
from html import escape
import json, shutil
ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://boooooobbb.github.io/baoqinghan/'
pages=json.loads((ROOT/'src/pages.json').read_text())
nav_items=[('home','','首页'),('about','about/','关于'),('projects','projects/','作品'),('notes','notes/','记录')]
for page in pages:
    path=page['path']; depth=len(Path(path).parts)-1
    base='../'*depth if depth else './'
    if path=='404.html': base='/baoqinghan/'
    nav=''.join(f'<a href="{base}{url}"'+(' aria-current="page"' if key==page['active'] else '')+f'>{label}</a>' for key,url,label in nav_items)
    canonical=ORIGIN+(path[:-10] if path.endswith('index.html') else path)
    body=(ROOT/'src/pages'/page['source']).read_text().replace('{{root}}',base)
    title=escape(page['title']); desc=escape(page['description'],quote=True)
    html=f'''<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#fbfbf8">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="{'article' if page['active']=='notes' and depth==2 else 'website'}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{ORIGIN}assets/bao-marker-portrait-v2.png"><meta property="og:locale" content="zh_CN">
<link rel="icon" type="image/svg+xml" sizes="any" href="{base}assets/backpack-icon-v2.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&amp;family=Patrick+Hand&amp;family=ZCOOL+KuaiLe&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css">
<link rel="stylesheet" href="{base}assets/site.css"><script src="{base}assets/site.js" defer></script>
</head><body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header class="site-header"><div class="shell nav"><a class="logo" href="{base}" aria-label="奇思妙想包 · 首页"><img class="brand-logo" src="{base}assets/qisimiaoxiangbao-logo.png" alt="奇思妙想包" width="1942" height="809" fetchpriority="high"></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="打开导航"><span></span><span></span><span></span></button><nav class="nav-links" id="site-nav" aria-label="主要导航">{nav}<a href="{base}#contact">联系我 ↗</a></nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="shell footer-inner"><span>© <span id="year">2026</span> Bao Qinghan</span><div class="footer-links"><a href="mailto:rynejason1@gmail.com">邮件 ↗</a><a href="https://github.com/Boooooobbb" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="{base}about/">关于我</a></div><span class="footer-hand">made with a wobbly line</span></div></footer>
<noscript><style>.menu-button{{display:none}}@media(max-width:760px){{.nav{{flex-wrap:wrap;padding-block:14px}}.nav-links{{position:static;display:flex;flex-wrap:wrap;opacity:1;transform:none;pointer-events:auto;box-shadow:none;border:0;padding:0;gap:12px}}}}</style></noscript>
</body></html>'''
    dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('\n'.join(line.rstrip() for line in html.splitlines())+'\n')
urls=[ORIGIN+(p['path'][:-10] if p['path'].endswith('index.html') else p['path']) for p in pages if p['path']!='404.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>\n')
# Keep the existing hosting configuration usable alongside GitHub Pages.
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
for p in pages:
    target=dist/p['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p['path'],target)
for name in ['bao-marker-portrait-v2.png','contact-icons-LICENSE.txt','site.css','site.js','favicon.svg','backpack-icon-v2.svg','qisimiaoxiangbao-logo.png']:
    (dist/'assets').mkdir(exist_ok=True);shutil.copy2(ROOT/'assets'/name,dist/'assets'/name)
shutil.copy2(ROOT/'sitemap.xml',dist/'sitemap.xml')
print(f'Built {len(pages)} pages; root and dist synchronized.')
