#!/usr/bin/env python3
"""Check actual generated links, fragments, metadata and deployment parity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.refs=[];self.titles=0;self.h1=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   assert a['id'] not in self.ids, 'Duplicate id: '+a['id']
   self.ids.add(a['id'])
  if tag=='title':self.titles+=1
  if tag=='h1':self.h1+=1
  for k in ('href','src'):
   if k in a:self.refs.append(a[k])
paths=[ROOT/p['path'] for p in json.loads((ROOT/'src/pages.json').read_text())]
parsed={p:Page(p.read_text()) for p in paths}
for p,page in parsed.items():
 assert page.titles==1 and page.h1==1, str(p)
 assert '{{root}}' not in p.read_text()
 assert p.read_bytes()==(ROOT/'dist'/p.relative_to(ROOT)).read_bytes(), 'dist differs'
 for ref in page.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  name=unquote(u.path)
  if name.startswith('/baoqinghan/'): target=ROOT/name[len('/baoqinghan/'):]
  else:target=(p.parent/name).resolve() if name else p
  if target.is_dir():target=target/'index.html'
  assert target.exists(),f'{p.relative_to(ROOT)}: missing {ref}'
  if u.fragment and target.suffix=='.html':
   q=parsed.get(target) or Page(target.read_text())
   assert unquote(u.fragment) in q.ids,f'{p}: missing anchor {ref}'
for name in ['site.css','site.js','favicon.svg','backpack-icon-v2.svg','bao-marker-portrait-v2.png','qisimiaoxiangbao-logo.png']:
 assert (ROOT/'assets'/name).read_bytes()==(ROOT/'dist/assets'/name).read_bytes()
print(f'PASS: {len(paths)} pages, local links/anchors, unique IDs, titles, headings, and dist parity.')
