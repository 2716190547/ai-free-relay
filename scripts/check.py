from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
ROOT = Path(__file__).resolve().parents[1] / 'dist'
class Check(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path = path; self.h1 = 0; self.title = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.h1 += tag == 'h1'
        self.title += tag == 'title'
        for field in ['href', 'src']:
            value = attrs.get(field, '')
            if value and not urlparse(value).scheme and not value.startswith('#'):
                target = (self.path.parent / value.split('#')[0]).resolve()
                assert target.exists(), (self.path, value)
for path in ROOT.rglob('*.html'):
    check = Check(path); check.feed(path.read_text())
    assert check.h1 == 1 and check.title == 1, path
    text = path.read_text()
    schema = text.split('<script type="application/ld+json">')[1].split('</script>')[0]
    json.loads(schema)
assert len(list(ROOT.rglob('*.html'))) == 9
print('PASS: 9 pages, internal links, headings, titles and JSON-LD')
