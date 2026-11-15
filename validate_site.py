"""Check deployable files and relative links without third-party dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

root = Path(__file__).resolve().parent
dist = root / 'dist'
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])

pages = {}
for path in dist.rglob('*.html'):
    page = Page(path)
    page.feed(path.read_text())
    pages[path.resolve()] = page

for path, page in pages.items():
    for link in page.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        if u.path.startswith('/'):
            errors.append(f'{path.name}: root-relative link breaks project Pages: {link}')
            continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        if not target.is_file():
            errors.append(f'{path.name}: missing file: {link}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing anchor: {link}')

assert (dist / 'index.html').is_file()
assert (dist / '.nojekyll').is_file()
assert (dist / 'Solee_Im_CV.pdf').read_bytes().startswith(b'%PDF')
profile = json.loads((root / 'profile.json').read_text())
for item in profile['publications'] + profile['posters']:
    if item.get('image') and not (dist / item['image']).is_file():
        errors.append(f'Missing publication figure: {item["image"]}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} HTML pages, local links, anchors, PDF, and publication figures.')
