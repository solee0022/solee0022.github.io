import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_D = json.loads((ROOT / 'profile.json').read_text())
D = {**SITE_D, **SITE_D.get('cv', {})}
D['links'] = {k: v for k, v in D['links'].items() if k not in ('DBLP', 'ORCID')}
D['links']['GitHub'] = 'https://github.com/solee0022'
D['service'] = [x for x in D['service'] if x.get('title') and '[' not in x['title']]
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
e = html.escape
def detail_text(value):
    return e(value).replace('\n', '<br/>').replace('cum laude', '<i>cum laude</i>')
links = ' '.join(f'<a href="{e(url)}">{e(label)}</a>' for label, url in D['links'].items())

def papers():
    result = []
    for p in D['publications']:
        authors = e(p['authors']).replace('Solee Im', '<strong>Solee Im</strong>')
        result.append(f'''<article class="paper"><div class="paper-meta"><b>{e(p['year'])}</b><span>{e(p['tag'])}</span></div><h3><a href="{e(p['url'])}">{e(p['title'])}</a></h3><p class="authors">{authors}</p><p class="venue">{e(p['venue'])}, {e(p['year'])}{' · Poster' if p.get('status') == 'Poster' else ''}</p><a class="paper-link" href="{e(p['url'])}">Paper & publication details ↗</a></article>''')
    return '\n'.join(result)

def entries(key):
    return ''.join(f'<div class="entry"><div><strong>{e(x["title"])}</strong><p>{detail_text(x["detail"])}</p></div><time>{e(x["dates"])}</time></div>' for x in D[key])

def additional_section(key, title):
    items = []
    for p in D.get(key, []):
        authors = e(p['authors']).replace('Solee Im', '<strong>Solee Im</strong>')
        link = f'<a class="paper-link" href="{e(p["url"])}">Publication details ↗</a>' if p.get('url') else ''
        items.append(f'<article class="paper"><div class="paper-meta"><b>{e(p.get("year", p["venue"].split()[-1]))}</b><span>{e(p.get("tag", ""))}</span></div><h3>{e(p["title"])}</h3><p class="authors">{authors}</p><p class="venue">{e(p["venue"])} · {e(p["status"])}</p>{link}</article>')
    return '<section><div class="section-head"><h2>'+title+'</h2></div>'+''.join(items)+'</section>'

review_html = additional_section('under_review', 'Manuscripts Under Review').replace('</section>', '<p class="note">* Equal contribution (co-first authors).</p></section>')
poster_html = ''

sections = ''.join(f'<section id="{key}"><div class="section-head"><h2>{label}</h2>{('<span>To be completed</span>' if any('[' in x['title'] for x in D[key]) else '')}</div>{entries(key)}</section>' for key, label in [('education','Education'),('experience','Experience'),('awards','Honors & Awards'),('service','Academic Service')])
head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Solee Im — academic homepage, publications, and curriculum vitae."><link rel="stylesheet" href="style.css">'
from home import render
(OUT / 'index.html').write_text(render(SITE_D))
cv = f'''{head}<title>Solee Im | Curriculum Vitae</title></head><body><main class="cv-page"><div class="toolbar"><a href="index.html">← Homepage</a><a href="Solee_Im_CV.pdf" download>Download PDF ↓</a><button onclick="window.print()">Print CV</button></div><h1>{e(D['name'])}</h1><p>Curriculum Vitae</p><p class="note">{e(D['role'])} · {e(D['affiliation'])}{('<br>'+e(D['email'])) if D.get('email') and '[' not in D['email'] else ''}</p><div class="social">{links}</div><section><h2>Research Interests</h2><p>{e('; '.join(D['interests']))}.</p></section>{sections.split('<section id="awards">')[0]}{review_html}<section><h2>Conference Publications</h2>{papers()}<p class="note">* Equal contribution (co-first authors).</p></section>{poster_html}<section><h2>Honors & Awards</h2>{entries('awards')}</section>{('<section><h2>Academic Service</h2>'+entries('service')+'</section>') if D['service'] else ''}</main></body></html>'''
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

# Reference-inspired academic PDF: serif type, monochrome, and aligned dates.
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_RIGHT

styles = {
    'body': ParagraphStyle('Body', fontName='Times-Roman', fontSize=10.5, leading=13),
    'name': ParagraphStyle('Name', fontName='Times-Bold', fontSize=19, leading=23),
    'right': ParagraphStyle('Right', fontName='Times-Roman', fontSize=10.5, leading=13, alignment=TA_RIGHT),
    'section': ParagraphStyle('Section', fontName='Times-Bold', fontSize=15, leading=18, spaceBefore=17, spaceAfter=10, keepWithNext=True),
    'paper': ParagraphStyle('Paper', fontName='Times-Roman', fontSize=10.5, leading=13, leftIndent=24, firstLineIndent=-24, spaceAfter=10),
}
def para(text, sty='body'):
    return Paragraph(text.replace('–', '-').replace('—', '-'), styles[sty])

def row(left, right, name=False):
    t = Table([[para(left, 'name' if name else 'body'), para(right, 'right')]], colWidths=[353, 133], hAlign="LEFT")
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'BOTTOM' if name else 'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return t

story = [row(e(D['name']), e(D['role'])+' @ KT', True), Spacer(1,5), HRFlowable(width='100%', thickness=0.8, color='black'), Spacer(1,5)]
contact = '<link href="https://solee0022.github.io">solee0022.github.io</link>'
if D.get('email') and '[' not in D['email']:
    contact = e(D['email'])+' &nbsp; | &nbsp; '+contact
contact += ' &nbsp; | &nbsp; '+' &nbsp; | &nbsp; '.join(f'<link href="{e(u)}">{e(k)}</link>' for k,u in D['links'].items())
story += [para(contact), Spacer(1,10), para('Employment','section')]
for x in D['experience']:
    role, _, org = x['title'].partition(' · ')
    story.append(KeepTogether([row('<b>'+e(org or role)+'</b> @ South Korea', e(x['dates'])), para('<i>'+e(role)+'</i>'), para(detail_text(x['detail'])), Spacer(1,12)]))
story.append(para('Education','section'))
for x in D['education']:
    story.append(KeepTogether([row('<b>'+e(x['title'])+'</b>',e(x['dates'])),para(detail_text(x['detail'])),Spacer(1,12)]))
for key,label in [('awards','Honors and Awards')]:
    items=[x for x in D[key] if '[' not in x['title']]
    if items:
        story.append(para(label,'section'))
        for x in items:
            story.append(para(e(x['title'])+' - '+e(x['detail'])+(' ('+e(x['dates'])+')' if x.get('dates') else '')))
story += [para('Research Interests','section'),para(e('; '.join(D['interests']))+'.')]
story.append(PageBreak())
story.append(para('Conference Publications','section'))
for i,p in enumerate(D['publications'],1):
    authors=e(p['authors']).replace('Solee Im','<b>Solee Im</b>')
    title=f'<link href="{e(p["url"])}">{e(p["title"])}</link>'
    venue='<i>'+e(p['venue'])+'</i>, '+p['year']+(' (Poster)' if p.get('status')=='Poster' else '')
    story.append(para(f'[{i}] {authors}. &quot;{title}.&quot; {venue}.','paper'))
story.append(para('* Equal contribution (co-first authors).'))
story.append(para('Manuscripts Under Review','section'))
for i,p in enumerate(D.get('under_review',[]),1):
    authors=e(p['authors']).replace('Solee Im','<b>Solee Im</b>')
    story.append(para(f'[U{i}] {authors}. &quot;{e(p["title"])}.&quot; Under review, <i>{e(p["venue"])}</i>.','paper'))
story.append(para('* Equal contribution (co-first authors).'))
items=[x for x in D['service'] if '[' not in x['title']]
if items:
    story.append(para('Academic Service','section'))
    for x in items:
        story.append(para(e(x['title'])+' - '+e(x['detail'])+(' ('+e(x['dates'])+')' if x.get('dates') else '')))
def footer(c,doc):
    c.setFont('Times-Roman',10)
    c.drawCentredString(letter[0]/2,26,str(doc.page))
doc=SimpleDocTemplate(str(OUT/'Solee_Im_CV.pdf'),pagesize=letter,rightMargin=57,leftMargin=57,topMargin=51,bottomMargin=48,title='Solee Im - Curriculum Vitae',author='Solee Im')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Built homepage, online CV, and reference-styled PDF CV.')
