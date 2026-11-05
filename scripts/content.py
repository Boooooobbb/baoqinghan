"""Render curated collections and optional Markdown articles at build time."""
from html import escape
from datetime import date
import json,re
import markdown

def prepare_content(root,pages):
    bodies={}
    for key,items in json.loads((root/'src/collections.json').read_text()).items():
        label,english=('电影','CINEMA LIST.') if key=='movies' else ('游戏','PLAY LIST.')
        cards=''.join(f'<li class="cover-item"><figure><img src="{{{{root}}}}assets/covers/{slug}.jpg" alt="{escape(title)}的 AI 手绘封面" width="400" height="600" loading="lazy"><figcaption><span class="cover-number">{i:02d}</span><div class="cover-copy"><h2>{escape(title)}</h2><p class="cover-review">{escape(review)}</p></div></figcaption></figure></li>' for i,(slug,title,review) in enumerate(items,1))
        bodies[key+'/index.html']=f'<div class="shell"><header class="page-head"><p class="eyebrow">{label}清单 / {len(items):02d} PICKS</p><h1>{english}</h1><p class="intro">'+('把喜欢的故事，收进这一页。' if key=='movies' else '在另一个世界里，继续探索。')+f'</p></header><ol class="cover-list">{cards}</ol><p class="cover-credit">封面为 AI 手绘演绎，作品名称及相关形象归各自权利人所有。</p></div>'
    articles=[]
    for source in sorted((root/'content/articles').glob('*.md')):
        slug=source.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError(f'Invalid article slug: {slug}')
        text=source.read_text()
        # JSON metadata followed by a blank line and Markdown body.
        meta,end=json.JSONDecoder().raw_decode(text)
        for key in ('title','date','summary'):
            if not isinstance(meta.get(key),str) or not meta[key].strip():raise ValueError(f'{source}: missing {key}')
        date.fromisoformat(meta['date'])
        body=text[end:].strip()
        if not body:raise ValueError(f'{source}: empty article')
        path=f'notes/{slug}/index.html'
        if any(p['path']==path for p in pages):raise ValueError(f'Duplicate article path: {path}')
        rendered=markdown.markdown(body,extensions=['fenced_code','tables','sane_lists','toc'])
        if re.search(r'<h1\b',rendered):raise ValueError('Use headings starting at ##; the article title supplies h1')
        pages.append(dict(path=path,title=meta['title']+'｜包庆涵',description=meta['summary'],active='notes'))
        bodies[path]=f'<article class="shell"><header class="page-head article-head"><p class="eyebrow">文章 / <time datetime="{meta["date"]}">{meta["date"]}</time></p><h1>{escape(meta["title"])}</h1></header><div class="prose article-body">{rendered}<p class="article-end"><a href="{{{{root}}}}notes/">← 所有文章</a></p></div></article>'
        articles.append((meta,path))
    rows=''.join(f'<a class="note-row" href="{{{{root}}}}{path[:-10]}"><time>{meta["date"]}</time><h2>{escape(meta["title"])}</h2><p>{escape(meta["summary"])}</p></a>' for meta,path in sorted(articles,key=lambda a:(a[0]['date'],a[1]),reverse=True))
    bodies['notes/index.html']='<div class="shell"><header class="page-head"><p class="eyebrow">文章 / NOTES</p><h1>WORDS &amp; IDEAS.</h1><p class="intro">记录思考，也为新的想法留白。</p></header><div class="articles-list">'+(rows or '<div class="article-empty"><span aria-hidden="true">✳</span><h2>这一页，留给下一次思考。</h2><p>暂时还没有发布文章。</p></div>')+'</div></div>'
    return pages,bodies
