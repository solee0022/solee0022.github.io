"""Academic homepage renderer. Publication images are optional local asset paths."""
from html import escape as e

def render(d):
    d = {**d, **d.get('cv', {})}
    d['links'] = {k: v for k, v in d['links'].items() if k not in ('DBLP', 'ORCID')}
    d['links']['GitHub'] = 'https://github.com/solee0022'
    d['links']['LinkedIn'] = 'https://www.linkedin.com/in/solee-im-414614225/'
    def figure(p):
        if p.get('image'):
            license_link = f' · <a href="{e(p["image_license"])}">CC BY 4.0</a>' if p.get('image_license') else ''
            source = p.get('image_source') or p.get('url')
            source_link = f' <a href="{e(source)}">Original paper ↗</a>' if source else ''
            credit = f'<details class="figure-credit"><summary>Figure source</summary><p>{e(p.get("image_credit", ""))}{source_link}{license_link}</p></details>'
            return f'<figure class="paper-figure filled"><a class="figure-zoom" href="{e(p["image"])}" target="_blank" rel="noopener" aria-label="View full-size figure for {e(p["title"])}"><img src="{e(p["image"])}" alt="{e(p.get("image_alt") or p["title"])}" loading="lazy"><span class="zoom-hint" aria-hidden="true">↗</span></a><figcaption>{credit}</figcaption></figure>'
        return ''

    def paper(p):
        title=e(p['title']); authors=e(p['authors']).replace('Solee Im','<strong>Solee Im</strong>')
        title=f'<a href="{e(p["url"])}">{title}</a>' if p.get('url') else title
        status=p.get('year', p.get('status',''))
        if p.get('status') == 'Poster': status += ' · Poster'
        venue=e(p['venue'])
        action=f'<a class="paper-link" href="{e(p["url"])}">Paper <span aria-hidden="true">↗</span></a>' if p.get('url') else ''
        layout = '' if p.get('image') else ' style="grid-template-columns:1fr"'
        return f'<article class="paper-row"{layout}>{figure(p)}<div class="paper-content"><div class="paper-meta"><span class="badge">{e(status)}</span><span>{venue}</span></div><h4>{title}</h4><p class="authors">{authors}</p>{action}</div></article>'

    groups=''
    for key,title in [('under_review','Manuscripts Under Review'),('publications','Conference Publications')]:
        note='<p class="contribution">* Equal contribution (co-first authors).</p>' if any('*' in p['authors'] for p in d[key]) else ''
        groups+=f'<section class="paper-group" aria-labelledby="{key}-heading"><h3 id="{key}-heading">{title}</h3>'+''.join(paper(p) for p in d[key])+note+'</section>'
    details=''
    academic_bio = e(d.get('academic_bio', ''))
    academic_bio = academic_bio.replace('from POSTECH, advised by', 'from POSTECH, where I worked in the <a href="https://nlp.postech.ac.kr/">NLP Lab</a> under')
    for advisor in d.get('advisors', []):
        academic_bio = academic_bio.replace(e(advisor['name']), '<a href="'+e(advisor['url'])+'">'+e(advisor['name'])+'</a>')
    academic_html = '<p class="intro">'+academic_bio+'</p>' if academic_bio else ''
    about_html = ''.join('<p class="intro">'+('<strong>Research Focus:</strong> ' if i == 0 else '')+e(paragraph)+'</p>' for i, paragraph in enumerate(d['about'].split('\n\n')) if paragraph.strip())
    news_items = d.get('news', [
        {'date': 'Aug. 2025', 'text': 'I received my master’s degree in Artificial Intelligence from POSTECH.'},
        {'date': 'Jul. 2025', 'text': 'I joined the SoundAI Team at KT as an AI Researcher.'},
    ])
    news_rows = ''.join('<li style="display:flex;gap:1.25rem;align-items:baseline;margin-bottom:.75rem;flex-wrap:wrap"><span class="entry-date" style="min-width:6rem">'+e(item['date'])+'</span><span style="flex:1;min-width:14rem">'+e(item['text'])+'</span></li>' for item in news_items)
    news_html = '<section id="news" class="detail-section"><h2>News</h2><ul style="list-style:none;padding:0">'+news_rows+'</ul></section>' if news_rows else ''
    news_nav = '<a href="#news">News</a>' if news_rows else ''
    def contact_icon(kind):
        paths = {
            'location': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
            'email': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
            'Google Scholar': '<path d="m2 9 10-5 10 5-10 5-10-5Zm4 2v6c4 3 8 3 12 0v-6M22 9v8"/>',
            'GitHub': '<path d="M9 20c-5 1-5-3-7-3m14 5v-4c0-1-.3-2-1-2.5 4-.5 6-2 6-6a5 5 0 0 0-1.5-3.5c.2-1 .2-2.5-.5-3.5-2 0-3.5 1-4 1.5a14 14 0 0 0-6 0C8.5 3.5 7 2.5 5 2.5c-.7 1-.7 2.5-.5 3.5A5 5 0 0 0 3 9.5c0 4 2 5.5 6 6-.7.5-1 1.5-1 2.5v4"/>',
            'LinkedIn': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-7m0 3a3 3 0 0 1 6 0v4"/>',
        }
        return '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink:0">'+paths[kind]+'</svg>'
    d['email'] = 'imsol2277@gmail.com'
    d['location'] = 'Seoul, South Korea'
    row_style = 'display:flex;align-items:center;gap:10px'
    social = '<div style="'+row_style+';color:var(--muted)">'+contact_icon('location')+e(d.get('location', 'South Korea'))+'</div>'
    if d.get('email') and '[' not in d['email']:
        social += '<a style="'+row_style+'" href="mailto:'+e(d['email'])+'">'+contact_icon('email')+e(d['email'])+'</a>'
    for label, url in d['links'].items():
        social += '<a style="'+row_style+'" href="'+e(url)+'">'+contact_icon(label)+e('solee0022' if label == 'GitHub' else label)+'</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Solee Im — research, publications, and curriculum vitae."><title>Solee Im | Research</title><script src="theme.js"></script><link rel="stylesheet" href="home.css"></head><body id="top"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="#top">Solee Im<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="#about">About</a>{news_nav}<a href="#publications">Publications</a><a href="cv.html">CV <span aria-hidden="true">↗</span></a></nav><button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">Dark</span></button></div></header><div class="layout"><aside class="profile" aria-label="Researcher profile"><div class="portrait" style="height:auto;display:block;background:transparent;border:0"><img src="assets/solee-profile-v2.jpg" alt="Solee Im" style="display:block;width:100%;height:auto"></div><h1>{e(d['name'])}</h1><p class="role">{e(d['role'])}<br>{e(d['affiliation'])}</p><div class="social" style="flex-direction:column;align-items:flex-start;gap:8px">{social}</div></aside><main id="main"><section id="about" class="about-section"><p class="eyebrow">RESEARCH & PUBLICATIONS</p><h2>About me</h2><p class="intro">I am an AI Researcher in the SoundAI Team at KT.</p>{about_html}{academic_html}</section>{news_html}<section id="publications"><div class="section-heading"><h2>Publications</h2><a href="{e(d['links']['Google Scholar'])}">Google Scholar ↗</a></div>{groups}</section>{details}<footer><span>© 2026 Solee Im</span></footer></main></div></body></html>'''
