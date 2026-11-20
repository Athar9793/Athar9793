"""Generate services/, expertise/ and blog/ pages from index.html chrome + tools/content.py.
Run from the repo root:  python3 tools/build_pages.py"""
import re, json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import SERVICES, EXPERTISE, BLOG, UI
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
idx = open(R + 'index.html').read()
E = html.escape
HOME_A = json.loads(re.search(r'var A=(\{.*?\}),r=', idx).group(1))

def grab(a, b):
    i = idx.index(a); return idx[i:idx.index(b, i) + len(b)]
CSS = idx[idx.index('<style>') + 7: idx.index('</style>')].replace('url(images/', 'url(../images/')
NAV = grab('<nav id="hdr">', '</nav>')
FOOT = grab('<footer>', '</footer>')
WA = grab('<a id="wa"', '</a>')
SCRIPTS = re.findall(r'<script>\n?\(function\(\)\{var (?:b=document.getElementById\(\'top\'\)|r=document.documentElement,k=\'theme\'|n=document.getElementById\(\'hdr\'\)).*?</script>', idx, re.S)
TR = re.search(r'<script>\n?\(function\(\)\{var A=\{.*?</script>', idx, re.S).group(0)
assert len(SCRIPTS) == 3

def relink(h):
    h = re.sub(r'href="#([^"]*)"', lambda m: f'href="../index.html#{m.group(1)}"' if m.group(1) else 'href="../index.html"', h)
    h = re.sub(r'href="(services|expertise|blog)/', r'href="../\1/', h)
    return h.replace('src="branding/', 'src="../branding/')
NAV, FOOT = relink(NAV), relink(FOOT)
for s in SERVICES:  # footer service links -> service pages
    FOOT = FOOT.replace(f'<a href="../index.html#services">{E(s["title"][0])}</a>', f'<a href="../services/{s["slug"]}.html">{E(s["title"][0])}</a>')

def card_of(title):
    m = re.search(r'<div class="card[^"]*"[^>]*><div class="thumb"><img src="([^"?]*)[^"]*" alt="([^"]*)"[^>]*></div><span class="tag">([^<]*)</span><h3>' + re.escape(E(title)) + r'</h3><p>([^<]*)</p>', idx)
    return m.groups()
def blog_of(i):
    m = re.findall(r'<div class="card"><div class="thumb"><img src="([^"?]*)[^"]*" alt="([^"]*)"[^>]*></div><small class="date">([^<]*)</small><h3>([^<]*)</h3>', idx)
    return m[i]

EXTRA = '''
header.ph{padding:150px 0 72px!important;background:linear-gradient(100deg,rgba(16,36,58,.95) 35%,rgba(16,36,58,.55)),var(--img) center/cover,#10243A!important}
header.ph h1{font-size:clamp(30px,4.6vw,48px)}header.ph .tag{color:#7DD8E6;border-color:rgba(125,216,230,.5);margin-bottom:14px}
.crumbs{display:flex;gap:8px;flex-wrap:wrap;font-size:14px;color:#B8C4CE;margin:0 0 18px!important}.crumbs a{color:#D5DEE6}.crumbs a:hover{color:#7DD8E6}
.split{display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center}.split img{width:100%;height:auto;border-radius:14px;display:block;box-shadow:0 14px 32px rgba(16,36,58,.12)}
.lead2{font-size:18px;line-height:1.8;color:var(--ink)}
.checks{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;list-style:none;padding:0}
.checks li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px 16px 48px;position:relative}
.checks li::before{content:"\\2713";position:absolute;left:18px;top:15px;color:var(--teal);font-weight:700}
[dir=rtl] .checks li{padding:16px 48px 16px 18px}[dir=rtl] .checks li::before{left:auto;right:18px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;counter-reset:s}
.step{position:relative;padding-top:56px!important}.step .n{position:absolute;top:18px;left:22px;font-family:Manrope,Inter,sans-serif;font-weight:800;font-size:28px;color:var(--teal);opacity:.9}
[dir=rtl] .step .n{left:auto;right:22px}
.sys h3{margin-bottom:10px!important}.sys ul{padding-left:18px}[dir=rtl] .sys ul{padding-left:0;padding-right:18px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chip{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:8px 16px;font-size:14px;color:var(--ink)}.chip:hover{border-color:var(--teal);color:var(--teal)}
.ctaband{background:var(--deep)!important;color:#fff;text-align:center}.ctaband h2{color:#fff}.ctaband h2::before{margin:0 auto 14px}.ctaband p{color:#C9D4DE;margin-bottom:22px}
.ctaband .btn{margin:4px}.btnwa{background:#25d366!important;color:#fff!important}
.article{max-width:780px}.article h2{font-size:24px;margin:36px 0 14px}.article p{font-size:17px;line-height:1.85;margin-bottom:12px}
.article ul{padding-left:22px;display:grid;gap:8px;margin:6px 0 10px}[dir=rtl] .article ul{padding-left:0;padding-right:22px}.article li{font-size:17px}
.article .hero-img{width:100%;height:auto;border-radius:14px;display:block;margin-bottom:12px}
@media(max-width:820px){.split,.two{grid-template-columns:1fr}}
'''

def page(title, desc, path, img, body, strings):
    d = {k: HOME_A[k] for k in HOME_A}
    for en, ar in strings:
        d[html.unescape(en)] = ar
    tr = re.sub(r'var A=\{.*?\},r=', lambda m: 'var A=' + json.dumps(d, ensure_ascii=False) + ',r=', TR, count=1, flags=re.S)
    url = 'https://athar9793.github.io/Athar9793/' + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Azmi MEP Consultants</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)} | Azmi MEP Consultants"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://athar9793.github.io/Athar9793/{img}">
<link rel="icon" href="../branding/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA}</style>
</head>
<body>
{NAV}
{body}
{FOOT}
{WA}
<button id="top" type="button" aria-label="Back to top">↑</button>
{chr(10).join(SCRIPTS[:2])}
{tr}
{SCRIPTS[2]}
</body>
</html>
'''

def ul(items, cls='checks'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{E(en)}</li>' for en, _ in items) + '</ul>'
def hero(img, crumbs, tag, title, sub, cta=True):
    c = '<p class="crumbs"><a href="../index.html">Home</a><span>/</span>' + ''.join(f'<a href="{h}">{E(t)}</a><span>/</span>' for t, h in crumbs) + f'<span>{E(title)}</span></p>'
    b = '<a class="btn" href="../index.html#contact">Request a quote</a> <a class="btn btn2" href="https://wa.me/966508696504" target="_blank" rel="noopener">Chat on WhatsApp</a>' if cta else ''
    return f'<header class="ph" style="--img:url(\'../{img}\')"><div class="wrap">{c}<span class="tag">{E(tag)}</span><h1>{E(title)}</h1><p>{E(sub)}</p>{b}</div></header>'
CTA = '<section class="ctaband"><div class="wrap"><h2>Need this service for your project?</h2><p>Share your scope and we will send a tailored quotation.</p><a class="btn" href="../index.html#contact">Request a quote</a><a class="btn btnwa" href="https://wa.me/966508696504" target="_blank" rel="noopener">Chat on WhatsApp</a></div></section>'
BASE = [("Home", UI["Home"]), ("Services", HOME_A["Services"]), ("Expertise", HOME_A["Expertise"]), ("Blog", UI["Blog"]), ("Request a quote", HOME_A["Request a quote"])] + list(UI.items())
SV = {s['slug']: s for s in SERVICES}; EX = {x['slug']: x for x in EXPERTISE}
out = []

for s in SERVICES:
    t_en, t_ar = s['title']; img, alt, tag, desc = card_of(t_en); tag = html.unescape(tag); desc = html.unescape(desc)
    st = BASE + [s['title'], (tag, HOME_A.get(tag, tag)), (desc, HOME_A.get(desc, desc)), s['overview']] + s['deliver'] + s['ideal']
    steps = ''.join(f'<div class="card step"><span class="n">0{i+1}</span><h3>{E(a)}</h3><p>{E(c)}</p></div>' for i, (a, b, c, d) in enumerate(s['approach']))
    st += [(a, b) for a, b, c, d in s['approach']] + [(c, d) for a, b, c, d in s['approach']]
    faqs = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, qa, a, aa in s['faqs'])
    st += [(q, qa) for q, qa, a, aa in s['faqs']] + [(a, aa) for q, qa, a, aa in s['faqs']]
    rel = ''.join(f'<a class="chip" href="../expertise/{x}.html">{E(EX[x]["title"][0])}</a>' for x in s['expertise'])
    oth = ''.join(f'<a class="chip" href="{o["slug"]}.html">{E(o["title"][0])}</a>' for o in SERVICES if o is not s)
    st += [EX[x]['title'] for x in s['expertise']] + [o['title'] for o in SERVICES]
    body = (hero(img, [("Services", "../index.html#services")], tag, t_en, desc) +
      f'<section><div class="wrap split"><div><h2>{E(t_en)}</h2><p class="lead2">{E(s["overview"][0])}</p></div><img src="../{img}" alt="{alt}" width="640" height="360" loading="lazy"></div></section>'
      f'<section><div class="wrap"><h2>What we deliver</h2>{ul(s["deliver"])}</div></section>'
      f'<section><div class="wrap"><h2>Our approach</h2><div class="steps">{steps}</div></div></section>'
      f'<section><div class="wrap two"><div><h2>Who it\'s for</h2>{ul(s["ideal"])}</div><div><h2>Frequently asked questions</h2>{faqs}</div></div></section>'
      + CTA +
      f'<section><div class="wrap two"><div><h2>Related expertise</h2><div class="chips">{rel}</div></div><div><h2>Other services</h2><div class="chips">{oth}</div></div></div></section>')
    path = f'services/{s["slug"]}.html'; open(R + path, 'w').write(page(t_en, s['overview'][0], path, img, body, st)); out.append(path)

for x in EXPERTISE:
    t_en, t_ar = x['title']; tag = x['tag']
    st = BASE + [x['title'], tag, x['intro']] + x['standards'] + x['calcs'] + x['outputs']
    sysc = ''
    for (n_en, n_ar), items in x['systems']:
        sysc += f'<div class="card sys"><h3>{E(n_en)}</h3><ul>' + ''.join(f'<li>{E(a)}</li>' for a, b in items) + '</ul></div>'
        st += [(n_en, n_ar)] + items
    mid = ''
    if x['standards']:
        mid = f'<section><div class="wrap two"><div><h2>Codes and standards</h2>{ul(x["standards"])}</div><div><h2>Key calculations we check</h2>{ul(x["calcs"])}</div></div></section>'
    rel = ''.join(f'<a class="chip" href="../services/{v}.html">{E(SV[v]["title"][0])}</a>' for v in x['services'])
    oth = ''.join(f'<a class="chip" href="{o["slug"]}.html">{E(o["title"][0])}</a>' for o in EXPERTISE if o is not x)
    st += [SV[v]['title'] for v in x['services']] + [o['title'] for o in EXPERTISE]
    body = (hero(x['img'], [("Expertise", "../index.html#expertise")], tag[0], t_en, x['intro'][0]) +
      f'<section><div class="wrap"><h2>Systems we cover</h2><div class="grid">{sysc}</div></div></section>' + mid +
      f'<section><div class="wrap"><h2>Typical outputs</h2>{ul(x["outputs"])}</div></section>' + CTA +
      f'<section><div class="wrap two"><div><h2>Related services</h2><div class="chips">{rel}</div></div><div><h2>Other expertise</h2><div class="chips">{oth}</div></div></div></section>')
    os.makedirs(R + 'expertise', exist_ok=True)
    path = f'expertise/{x["slug"]}.html'; open(R + path, 'w').write(page(t_en, x['intro'][0], path, x['img'], body, st)); out.append(path)

for i, b in enumerate(BLOG):
    img, alt, date, title = blog_of(i); title_u = html.unescape(title)
    st = BASE + [(date, HOME_A.get(date, date)), (title_u, HOME_A.get(title_u, title_u))]
    art = f'<img class="hero-img" src="../{img}" alt="{alt}" width="1280" height="720">'
    for h_en, h_ar, p, items in b['sections']:
        if h_en: art += f'<h2>{E(h_en)}</h2>'; st.append((h_en, h_ar))
        if p: art += f'<p>{E(p[0])}</p>'; st.append(p)
        if items: art += '<ul>' + ''.join(f'<li>{E(a)}</li>' for a, _ in items) + '</ul>'; st += items
    more = ''.join(f'<a class="chip" href="{BLOG[j]["slug"]}.html">{blog_of(j)[3]}</a>' for j in range(len(BLOG)) if j != i)
    st += [(html.unescape(blog_of(j)[3]), HOME_A.get(html.unescape(blog_of(j)[3]), '')) for j in range(len(BLOG))]
    intro = b['sections'][0][2][0]
    body = (hero(img, [("Blog", "../index.html#blog")], html.unescape(date), title_u, intro, cta=False) +
      f'<section><div class="wrap article">{art}</div></section>' + CTA +
      f'<section><div class="wrap"><h2>More articles</h2><div class="chips">{more}</div></div></section>')
    path = f'blog/{b["slug"]}.html'; open(R + path, 'w').write(page(title_u, intro, path, img, body, st)); out.append(path)

U = 'https://athar9793.github.io/Athar9793/'
open(R + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{U}{p}</loc></url>\n' for p in [''] + out) + '</urlset>\n')
print('\n'.join(out))
