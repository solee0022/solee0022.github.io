import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / 'profile.json').read_text())
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
e = html.escape
links = ' '.join(f'<a href="{e(url)}">{e(label)}</a>' for label, url in D['links'].items())

def papers():
    result = []
    for p in D['publications']:
        authors = e(p['authors']).replace('Solee Im', '<strong>Solee Im</strong>')
        result.append(f'''<article class="paper"><div class="paper-meta"><b>{e(p['year'])}</b><span>{e(p['tag'])}</span></div><h3><a href="{e(p['url'])}">{e(p['title'])}</a></h3><p class="authors">{authors}</p><p class="venue">{e(p['venue'])}, {e(p['year'])}</p><a class="paper-link" href="{e(p['url'])}">Paper & publication details ↗</a></article>''')
    return '\n'.join(result)

def entries(key):
    return ''.join(f'<div class="entry"><div><strong>{e(x["title"])}</strong><p>{e(x["detail"])}</p></div><time>{e(x["dates"])}</time></div>' for x in D[key])

def additional_section(key, title):
    items = []
    for p in D.get(key, []):
        authors = e(p['authors']).replace('Solee Im', '<strong>Solee Im</strong>')
        link = f'<a class="paper-link" href="{e(p["url"])}">Publication details ↗</a>' if p.get('url') else ''
        items.append(f'<article class="paper"><div class="paper-meta"><b>{e(p["status"])}</b><span>{e(p["venue"])}</span></div><h3>{e(p["title"])}</h3><p class="authors">{authors}</p>{link}</article>')
    return '<section><div class="section-head"><h2>'+title+'</h2></div>'+''.join(items)+'</section>'

review_html = additional_section('under_review', 'Manuscripts Under Review').replace('</section>', '<p class="note">* Equal contribution (co-first authors).</p></section>')
poster_html = ''

sections = ''.join(f'<section id="{key}"><div class="section-head"><h2>{label}</h2><span>To be completed</span></div>{entries(key)}</section>' for key, label in [('education','Education'),('experience','Experience'),('awards','Honors & Awards'),('service','Academic Service')])
head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Solee Im — academic homepage, publications, and curriculum vitae."><link rel="stylesheet" href="style.css">'
homepage = f'''{head}<title>Solee Im | Research</title></head><body><div class="layout"><aside class="profile"><div class="portrait" aria-label="Portrait placeholder"><strong>SI</strong><span>PORTRAIT TO ADD</span></div><h1>{e(D['name'])}</h1><p class="role">{e(D['role'])}<br>{e(D['affiliation'])}</p><p class="note">{e(D['email'])}</p><div class="social">{links}</div><a class="cv-link" href="Solee_Im_CV.pdf" download>Download CV ↓</a><nav class="nav" aria-label="Main navigation"><a href="#about">About</a><a href="#publications">Publications</a><a href="#education">Education</a><a href="#experience">Experience</a><a href="cv.html">Curriculum Vitae ↗</a></nav></aside><main><div class="draft">Working draft · Profile details to be completed</div><section id="about"><p class="eyebrow">SPEECH & LANGUAGE RESEARCH</p><h2>About</h2><p class="about">{e(D['about'])}</p><p class="placeholder">[Add your current position, affiliation, and a short research biography.]</p><p class="note">Research topics reflected in my publications</p><ul class="interests">{''.join('<li>'+e(x)+'</li>' for x in D['interests'])}</ul></section>{review_html}<section id="publications"><div class="section-head"><h2>Publications</h2><span>Selected conference publications</span></div>{papers()}<p class="note">See <a href="{D['links']['Google Scholar']}">Google Scholar</a> and <a href="{D['links']['DBLP']}">DBLP</a> for additional records.</p></section>{poster_html}{sections}<section id="cv"><h2>Curriculum Vitae</h2><p>An overview of my education, research, and publications.</p><a href="Solee_Im_CV.pdf">Download PDF ↓</a> <span class="note">&nbsp; / &nbsp;</span> <a href="cv.html">View CV online ↗</a><p class="note">Template edition · November 2026</p></section><footer><span>© 2026 Solee Im</span><span>Publication metadata: <a href="https://dblp.org/pid/387/3897">DBLP</a> & <a href="https://aclanthology.org/2025.findings-acl.786/">ACL Anthology</a></span></footer></main></div></body></html>'''
from home import render
(OUT / 'index.html').write_text(render(D))
cv = f'''{head}<title>Solee Im | Curriculum Vitae</title></head><body><main class="cv-page"><div class="toolbar"><a href="index.html">← Homepage</a><a href="Solee_Im_CV.pdf" download>Download PDF ↓</a><button onclick="window.print()">Print CV</button></div><h1>{e(D['name'])}</h1><p>Curriculum Vitae</p><p class="note">{e(D['role'])} · {e(D['affiliation'])}<br>{e(D['email'])}</p><div class="social">{links}</div><div class="draft">Template edition · November 2026 · Bracketed fields to be completed</div><section><h2>Research Interests</h2><p>{e('; '.join(D['interests']))}.</p><p class="note">Draft topics based on the publications below.</p></section>{sections.split('<section id="awards">')[0]}{review_html}<section><h2>Conference Publications</h2>{papers()}<p class="note">* Equal contribution (co-first authors).</p></section>{poster_html}<section><h2>Honors & Awards</h2>{entries('awards')}</section><section><h2>Academic Service</h2>{entries('service')}</section><footer><span>Publication metadata verified against DBLP and ACL Anthology.</span></footer></main></body></html>'''
# Share homepage typography, colors, and theme preference with the online CV.
cv_styles = '''
.cv-page{max-width:1040px;margin:0 auto;padding:0 42px 40px}.cv-page .toolbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;flex-wrap:wrap;gap:12px 22px;min-height:76px;margin-bottom:42px;padding:12px 0;background:var(--header);border-bottom:1px solid var(--line);font-size:16px}.toolbar>a:first-child{margin-right:auto}.toolbar button{font:inherit;cursor:pointer}.toolbar .print-button{border:1px solid var(--border);border-radius:4px;background:transparent;color:var(--ink);padding:7px 12px;min-height:44px}.cv-page h1{font-size:38px;margin-bottom:8px}.cv-page>p{margin-bottom:12px}.cv-page .social{flex-direction:row;flex-wrap:wrap;gap:12px 22px;margin:18px 0}.cv-page .note{font-size:16px;line-height:1.7;color:var(--muted)}.cv-page .draft{margin:18px 0 32px}.cv-page section{margin:32px 0}.cv-page h2{font-size:28px;margin:0 0 18px;padding-top:28px;border-top:1px solid var(--line)}.cv-page .section-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-top:1px solid var(--line);padding-top:28px}.cv-page .section-head h2{padding:0;border:0}.cv-page .section-head>span{font-size:14px;color:var(--muted)}.cv-page .paper{padding:20px 0;border-bottom:1px solid var(--line)}.cv-page .paper:last-of-type{border-bottom:0}.cv-page .paper h3{font-size:19px;font-weight:600;line-height:1.5;margin:0 0 9px}.cv-page .paper-meta{font-size:14px;letter-spacing:0;gap:12px}.cv-page .paper-meta b{color:var(--accent);font-weight:600}.cv-page .authors{font-size:16px;margin-bottom:8px}.cv-page .venue{font-size:16px;color:var(--muted);margin-bottom:12px}.cv-page .entry{padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline}.cv-page .entry:last-child{border-bottom:0}.cv-page .entry strong{font-size:17px;font-weight:500}.cv-page .entry p,.cv-page .entry time{font-size:16px;color:var(--muted);margin:4px 0 0}.cv-page .entry time{white-space:nowrap;font-variant-numeric:tabular-nums}.cv-page footer{margin-top:36px}
@media(max-width:760px){.cv-page{padding:0 22px 28px}.cv-page .toolbar{gap:8px 14px;margin-bottom:30px;font-size:14px}.cv-page .toolbar>a:first-child{flex-basis:100%}.cv-page .toolbar .theme-toggle{margin-left:auto}.cv-page h1{font-size:32px}.cv-page h2{font-size:26px}.cv-page .section-head{flex-wrap:wrap;gap:0 12px}.cv-page .entry{align-items:flex-start}.cv-page .entry time{white-space:normal}.cv-page .paper-meta{flex-wrap:wrap}}
@media print{html{color-scheme:light!important}.cv-page{padding:0;margin:0;max-width:none;color:#222;font-size:10pt}.cv-page .toolbar,.cv-page .draft{display:none!important}.cv-page h1{font-size:26pt}.cv-page h2{font-size:16pt;break-after:avoid}.cv-page .paper h3{font-size:11pt}.cv-page .note,.cv-page .authors,.cv-page .venue,.cv-page .entry strong,.cv-page .entry p,.cv-page .entry time{font-size:10pt;color:#444}.cv-page .paper,.cv-page .entry{break-inside:avoid}.cv-page a{color:#222}.cv-page .paper-link{border:0;padding:0}.cv-page section{margin:18px 0}@page{size:A4;margin:18mm}}
'''
cv = cv.replace('<link rel="stylesheet" href="style.css">', '<script src="theme.js"></script><link rel="stylesheet" href="home.css"><style>'+cv_styles+'</style>')
cv = cv.replace('<button onclick="window.print()">Print CV</button>', '<button class="print-button" onclick="window.print()">Print CV</button><button class="theme-toggle" type="button" aria-label="Switch to dark mode" aria-pressed="false"><span class="theme-icon" aria-hidden="true">☾</span><span class="theme-label">Dark</span></button>')
(OUT / 'cv.html').write_text(cv)

import sys
if '--web-only' in sys.argv:
    print('Built website; existing PDF preserved.')
    sys.exit(0)

# A compact, editable-source PDF CV. Bracketed fields deliberately remain visible.
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CVName',fontName='Times-Roman',fontSize=29,leading=33,textColor=colors.HexColor('#27333a'),spaceAfter=5))
styles.add(ParagraphStyle(name='CVBody',fontName='Helvetica',fontSize=9,leading=13,textColor=colors.HexColor('#27333a'),spaceAfter=5))
styles.add(ParagraphStyle(name='CVSmall',parent=styles['CVBody'],fontSize=8,leading=11,textColor=colors.HexColor('#69767c')))
styles.add(ParagraphStyle(name='CVSection',fontName='Times-Roman',fontSize=15,leading=19,spaceBefore=13,spaceAfter=7,textColor=colors.HexColor('#176e72')))
story=[]
def para(text,sty='CVBody'):
    return Paragraph(text.replace('–','-').replace('·',' / '),styles[sty])
story += [para(e(D['name']),'CVName'),para('CURRICULUM VITAE','CVSmall'),para(e(D['role'])+' | '+e(D['affiliation'])+'<br/>'+e(D['email']))]
story += [para(' &nbsp; | &nbsp; '.join(f'<link href="{e(u)}" color="#176e72">{e(k)}</link>' for k,u in D['links'].items()),'CVSmall'),para('TEMPLATE / November 2026 / Bracketed fields to be completed','CVSmall')]
story += [para('Research Interests','CVSection'),para(e('; '.join(D['interests']))+'.'),para('Draft topics based on the publications listed below.','CVSmall')]
for key,label in [('education','Education'),('experience','Experience')]:
    story.append(para(label,'CVSection'))
    for x in D[key]: story.append(para(f'<b>{e(x["title"])}</b> &nbsp; {e(x["dates"])}<br/>{e(x["detail"])}'))
story.append(para('Manuscripts Under Review','CVSection'))
for p in D.get('under_review', []):
    story.append(KeepTogether([para('<b>'+e(p['title'])+'</b>'),para(e(p['authors']).replace('Solee Im','<b>Solee Im</b>'),'CVSmall'),para(e(p['venue'])+' / Under review','CVSmall'),Spacer(1,6)]))
story.append(para('* Equal contribution (co-first authors) for the manuscripts under review.','CVSmall'))
story.append(PageBreak())
story.append(para('Conference Publications','CVSection'))
for i,p in enumerate(D['publications'],1):
    title=f'<b>{i}. {e(p["title"])}</b>'
    authors=e(p['authors']).replace('Solee Im','<b>Solee Im</b>')
    venue=e(p['venue'])+', '+p['year']+(' / Poster' if p.get('status') == 'Poster' else '')+(' / pp. '+p['pages'] if p['pages'] else '')
    story.append(KeepTogether([para(title),para(authors,'CVSmall'),para(f'{venue}. <link href="{e(p["url"])}" color="#176e72">Publication link</link>','CVSmall'),Spacer(1,5)]))
story.append(para('* Equal contribution (co-first authors).','CVSmall'))
for key,label in [('awards','Honors & Awards'),('service','Academic Service')]:
    story.append(para(label,'CVSection'))
    for x in D[key]: story.append(para(f'{e(x["title"])} / {e(x["detail"])} / {e(x["dates"])}'))
def footer(c,doc):
    c.setFont('Helvetica',7);c.setFillColor(colors.HexColor('#69767c'))
    c.drawString(46,26,'Solee Im | CV template | Publication sources: DBLP and ACL Anthology')
    c.drawRightString(A4[0]-46,26,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'Solee_Im_CV.pdf'),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=34,bottomMargin=40,title='Solee Im — Curriculum Vitae (Template)',author='Solee Im')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Built homepage, online CV, and PDF CV.')
