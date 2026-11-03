"""Validate production SEO against approved content; no third-party dependencies."""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'public')
base = 'https://ivancl4udio.github.io/'
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

class Head(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.meta, self.titles = [], [], []
        self.in_title = False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'link': self.links.append(dict(attrs))
        if tag == 'meta': self.meta.append(dict(attrs))
        if tag == 'title': self.in_title = True
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.titles.append(data)

def check(condition, message):
    if not condition: raise SystemExit(message)

def output(url):
    check(url.startswith(base), f'External SEO URL: {url}')
    return root / url[len(base):] / 'index.html'

expected, translations, drafts = set(), {}, set()
for source in pathlib.Path('content').rglob('*.md'):
    text = source.read_text().split('+++')[1] if source.read_text().startswith('+++') else source.read_text().split('---')[1]
    def field(name):
        match = re.search(rf'^{name}\s*[:=]\s*["\']?([^\n"\']+)', text, re.M)
        return match.group(1).strip() if match else ''
    language, *parts = source.relative_to('content').parts
    name = pathlib.Path(*parts).with_suffix('').as_posix()
    name = name.removesuffix('_index').rstrip('/')
    url = base + ('' if language == 'en' else 'pt-br/') + (name + '/' if name else '')
    if field('draft') == 'true':
        drafts.add(url)
        check(not output(url).exists(), f'Draft published: {source}')
        continue
    check(field('editorialReview') == 'approved', f'Unapproved public content: {source}')
    expected.add(url)
    key = field('translationKey')
    if key: translations.setdefault(key, {})['en' if language == 'en' else 'pt-BR'] = url

index = ET.parse(root / 'sitemap.xml')
sitemaps = [x.text for x in index.findall('s:sitemap/s:loc', ns)]
check(set(sitemaps) == {base+'en/sitemap.xml', base+'pt-br/sitemap.xml'}, 'Unexpected sitemap index')
urls = []
for sitemap in sitemaps:
    tree = ET.parse(root / sitemap[len(base):])
    urls.extend(x.text for x in tree.findall('s:url/s:loc', ns))
check(set(urls) == expected and len(urls) == len(expected), 'Sitemap differs from approved public pages')
heads = {}
for url in expected:
    head = Head(output(url).read_text())
    heads[url] = head
    check(bool(''.join(head.titles).strip()), f'Missing title: {url}')
    descriptions = [m.get('content') for m in head.meta if m.get('name') == 'description']
    check(len(descriptions) == 1 and bool(descriptions[0]), f'Invalid description: {url}')
    check([l.get('href') for l in head.links if l.get('rel') == 'canonical'] == [url], f'Invalid canonical: {url}')
    for m in head.meta:
        if m.get('name', '').lower() in ('robots', 'googlebot'):
            check(not re.search(r'noindex|nofollow|none', m.get('content', ''), re.I), f'Indexing blocked: {url}')
    for prop in ('og:title', 'og:description', 'og:url', 'og:type'):
        values = [m.get('content') for m in head.meta if m.get('property') == prop]
        check(len(values) == 1 and bool(values[0]), f'Invalid {prop}: {url}')
    check(next(m['content'] for m in head.meta if m.get('property') == 'og:url') == url, f'Wrong OG URL: {url}')
for url, head in heads.items():
    group = next((g for g in translations.values() if url in g.values()), {})
    actual = [(l['hreflang'], l.get('href')) for l in head.links if l.get('rel') == 'alternate' and 'hreflang' in l]
    wanted = group if len(group) > 1 else {}
    check(dict(actual) == wanted and len(actual) == len(wanted), f'Invalid/missing reciprocal hreflang: {url}')
robots = (root / 'robots.txt').read_text()
check('Allow: /' in robots and not re.search(r'^Disallow:\s*/', robots, re.M), 'Crawling blocked')
check(f'Sitemap: {base}sitemap.xml' in robots, 'Missing absolute sitemap')
verification = list(pathlib.Path('static').glob('google*.html'))
check(bool(verification), 'Missing supplied Google verification')
for source in verification:
    check((root / source.name).read_bytes() == source.read_bytes(), 'Google verification changed')
check(len([u for u in expected if '/articles/' in u and not u.endswith('/articles/')]) == 4, 'Expected four approved articles')
print(f'SEO validated: {len(expected)} approved URLs, 2 language sitemaps, {len(drafts)} excluded drafts, canonical/hreflang/OG and Google verification.')
