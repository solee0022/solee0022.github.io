"""Academic homepage renderer. Publication images are optional local asset paths."""
from html import escape as e

def render(d):
    d = {**d, **d.get('cv', {})}
    d['links'] = {k: v for k, v in d['links'].items() if k not in ('DBLP', 'ORCID')}
    def figure(p):
        if p.get('image'):
            license_link = f' · <a href="{e(p["image_license"])}">CC BY 4.0</a>' if p.get('image_license') else ''
            credit = f'<details class="figure-credit"><summary>Figure source</summary><p>{e(p.get("image_credit", ""))} <a href="{e(p.get("image_source", p.get("url", "")))}">Original paper ↗</a>{license_link}</p></details>'
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
    for key,title in [('education','Education'),('experience','Experience'),('awards','Honors & Awards'),('service','Academic Service')]:
        items = [x for x in d[key] if x.get('title') and '[' not in x['title']]
        if not items:
            continue
        columns = {'education': ('Institution / Location', 'Degree / Program', 'Period'), 'experience': ('Position', 'Organization', 'Period'), 'awards': ('Award / Fellowship', 'Organization', 'Year'), 'service': ('Activity', 'Venue / Organization', 'Year')}[key]
        rows = ''
        for x in items:
            row_title, detail = x['title'], x['detail']
            if key == 'experience' and ' · ' in row_title:
                row_title, organization = row_title.split(' · ', 1)
                detail = organization + ' @ South Korea\n' + detail
            title_html = e(row_title).replace('cum laude', '<i>cum laude</i>')
            detail_html = e(detail).replace('\n', '<br>')
            rows += f'<tr><th scope="row">{title_html}</th><td>{detail_html}</td><td class="entry-date">{e(x["dates"])}</td></tr>'
        headers=''.join(f'<th scope="col">{e(label)}</th>' for label in columns)
        details+=f'<section id="{key}" class="detail-section"><h2 id="{key}-title">{title}</h2><div class="table-scroll" tabindex="0" role="region" aria-labelledby="{key}-title"><table class="background-table"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div></section>'
    social=''.join(f'<a href="{e(url)}">{e(label)} <span aria-hidden="true">↗</span></a>' for label,url in d['links'].items())
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Solee Im — research, publications, and curriculum vitae."><title>Solee Im | Research</title><script src="theme.js"></script><link rel="stylesheet" href="home.css"></head><body id="top"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="#top">Solee Im<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#publications">Publications</a><a href="#education">Background</a><a href="cv.html">CV <span aria-hidden="true">↗</span></a></nav><button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">Dark</span></button></div></header><div class="layout"><aside class="profile" aria-label="Researcher profile"><h1>{e(d['name'])}</h1><p class="role">{e(d['role'])}<br>{e(d['affiliation'])}</p>{('<p class="email">'+e(d['email'])+'</p>') if d.get('email') and '[' not in d['email'] else ''}<div class="social">{social}</div><a class="download" href="Solee_Im_CV.pdf" download>Download CV <span aria-hidden="true">↓</span></a></aside><main id="main"><section id="about" class="about-section"><p class="eyebrow">RESEARCH & PUBLICATIONS</p><h2>About me</h2><p class="intro">{e(d['about'])}</p><p>I am an AI Researcher in the SoundAI Team at KT.</p><div class="topics"><span class="topics-label">Topics in my publications</span><ul>{''.join('<li>'+e(x)+'</li>' for x in d['interests'])}</ul></div></section><section id="publications"><div class="section-heading"><h2>Publications</h2><a href="{e(d['links']['Google Scholar'])}">Google Scholar ↗</a></div>{groups}</section>{details}<section class="cv-section"><div><p class="eyebrow">CURRICULUM VITAE</p><h2>A closer look at my background.</h2><p>Education, research experience, and publications.</p></div><a href="cv.html">View CV ↗</a></section><footer><span>© 2026 Solee Im</span></footer></main></div></body></html>'''
