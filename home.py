"""Academic homepage renderer. Publication images are optional local asset paths."""
from html import escape as e

def render(d):
    def figure(p):
        if p.get('image'):
            license_link = f' · <a href="{e(p["image_license"])}">CC BY 4.0</a>' if p.get('image_license') else ''
            credit = f'<details class="figure-credit"><summary>Figure source</summary><p>{e(p.get("image_credit", ""))} <a href="{e(p.get("image_source", p.get("url", "")))}">Original paper ↗</a>{license_link}</p></details>'
            return f'<figure class="paper-figure filled"><a class="figure-zoom" href="{e(p["image"])}" target="_blank" rel="noopener" aria-label="View full-size figure for {e(p["title"])}"><img src="{e(p["image"])}" alt="{e(p.get("image_alt") or p["title"])}" loading="lazy"><span class="zoom-hint" aria-hidden="true">↗</span></a><figcaption>{credit}</figcaption></figure>'
        return '<figure class="paper-figure empty"><span class="figure-icon" aria-hidden="true">▧</span><span>Research preview</span><small>Figure to be added</small></figure>'

    def paper(p):
        title=e(p['title']); authors=e(p['authors']).replace('Solee Im','<strong>Solee Im</strong>')
        title=f'<a href="{e(p["url"])}">{title}</a>' if p.get('url') else title
        status=p.get('year', p.get('status',''))
        if p.get('status') == 'Poster': status += ' · Poster'
        venue=e(p['venue'])
        action=f'<a class="paper-link" href="{e(p["url"])}">Paper <span aria-hidden="true">↗</span></a>' if p.get('url') else ''
        return f'<article class="paper-row">{figure(p)}<div class="paper-content"><div class="paper-meta"><span class="badge">{e(status)}</span><span>{venue}</span></div><h4>{title}</h4><p class="authors">{authors}</p>{action}</div></article>'

    groups=''
    for key,title in [('under_review','Manuscripts Under Review'),('publications','Conference Publications')]:
        note='<p class="contribution">* Equal contribution (co-first authors).</p>' if any('*' in p['authors'] for p in d[key]) else ''
        groups+=f'<section class="paper-group" aria-labelledby="{key}-heading"><h3 id="{key}-heading">{title}</h3>'+''.join(paper(p) for p in d[key])+note+'</section>'
    details=''
    for key,title in [('education','Education'),('experience','Experience'),('awards','Honors & Awards'),('service','Academic Service')]:
        entries=''.join(f'<div class="entry"><div><h3>{e(x["title"])}</h3><p>{e(x["detail"])}</p></div><span>{e(x["dates"])}</span></div>' for x in d[key])
        details+=f'<section id="{key}" class="detail-section"><h2>{title}</h2>{entries}</section>'
    social=''.join(f'<a href="{e(url)}">{e(label)} <span aria-hidden="true">↗</span></a>' for label,url in d['links'].items())
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Solee Im — research, publications, and curriculum vitae."><title>Solee Im | Research</title><script src="theme.js"></script><link rel="stylesheet" href="home.css"></head><body id="top"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="#top">Solee Im<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#publications">Publications</a><a href="#education">Background</a><a href="cv.html">CV <span aria-hidden="true">↗</span></a></nav><button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">Dark</span></button></div></header><div class="layout"><aside class="profile" aria-label="Researcher profile"><div class="portrait"><span class="initials">SI</span><span class="portrait-label">Portrait to be added</span></div><h1>{e(d['name'])}</h1><p class="role">{e(d['role'])}<br>{e(d['affiliation'])}</p><p class="email">{e(d['email'])}</p><div class="social">{social}</div><a class="download" href="Solee_Im_CV.pdf" download>Download CV <span aria-hidden="true">↓</span></a><p class="profile-note">Academic homepage<br><span>Template edition · 2026</span></p></aside><main id="main"><section id="about" class="about-section"><div class="draft"><span></span>Profile draft · Personal details to be completed</div><p class="eyebrow">RESEARCH & PUBLICATIONS</p><h2>About me</h2><p class="intro">{e(d['about'])}</p><p class="placeholder">[Add your current position, affiliation, and a short research biography.]</p><div class="topics"><span class="topics-label">Topics in my publications</span><ul>{''.join('<li>'+e(x)+'</li>' for x in d['interests'])}</ul></div></section><section id="publications"><div class="section-heading"><h2>Publications</h2><a href="{e(d['links']['Google Scholar'])}">Google Scholar ↗</a></div>{groups}</section>{details}<section class="cv-section"><div><p class="eyebrow">CURRICULUM VITAE</p><h2>A closer look at my background.</h2><p>Education, research experience, and publications.</p></div><a href="cv.html">View CV ↗</a></section><footer><span>© 2026 Solee Im</span><span>Publication records: <a href="{e(d['links']['DBLP'])}">DBLP</a> · <a href="https://aclanthology.org/2025.findings-acl.786/">ACL Anthology</a></span></footer></main></div></body></html>'''
