from pathlib import Path
from lxml import etree
from collections import Counter
import json, re, zipfile, difflib, uuid
from datetime import datetime, timezone
from recover_source_spacing import content_nodes, slots_in, compact, NS

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / 'reports/英文二次校对'
TARGET = ROOT.parent / '战锤40K_LEX设定汇编_插画封面二次校订版.epub'

# Individually reviewed in their original sentence, including original-source
# errors that cannot be repaired by recovering rich-text boundary whitespace.
FIXES = [
    (23, 'everpresent', 'ever-present', 1),
    (27, 'mainhives', 'main hives', 1),
    (53, 'neverending', 'never-ending', 1),
    (68, 'eachother', 'each other', 1),
    (159, 'halfalive', 'half-alive', 1),
    (282, 'OccultBodyguards', 'Occult Bodyguards', 1),
    (463, 'offbalance', 'off balance', 1),
    (545, 'HomeWorld', 'Home World', 1),
    (561, 'longlost', 'long-lost', 1),
    (576, 'headstart', 'head start', 1),
    (579, 'plantlife', 'plant life', 1),
    (639, 'shipsUnrelenting', 'ships Unrelenting', 1),
    (770, 'safehaven', 'safe haven', 1),
    (834, 'soonafter', 'soon after', 1),
    (864, 'HeliosHellgraceHephaesto', 'Helios Hellgrace Hephaesto', 1),
    (864, 'LliaxLucius', 'Lliax Lucius', 1),
    (932, 'foodsource', 'food source', 1),
    (1252, 'patternstorm', 'pattern storm', 1),
    (1433, 'roadN/A', 'road N/A', 3),
    (1488, 'MarkIV-b', 'Mark IV-b', 2),
    (1498, 'MantletN/A', 'Mantlet N/A', 1),
]

records = []
changed = {}
with zipfile.ZipFile(ROOT / 'spacing-pass1.epub') as z:
    for number in sorted({f[0] for f in FIXES}):
        name = f'EPUB/text/article-{number:04d}.xhtml'
        doc = etree.fromstring(z.read(name))
        slots = [s for n in content_nodes(doc) for s in slots_in(n)]
        flat = ''.join(getattr(n, a) for n, a in slots)
        additions = {}
        for _, old, new, expected in [f for f in FIXES if f[0] == number]:
            matches = list(re.finditer(r'(?<![A-Za-z])' + re.escape(old) + r'(?![A-Za-z])', flat))
            assert len(matches) == expected, (number, old, expected, len(matches))
            for m in matches:
                for tag, a, b, c, d in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
                    if tag == 'equal':
                        continue
                    assert tag == 'insert' and new[c:d] in (' ', '-'), (old, new, tag)
                    assert m.start() + a not in additions
                    additions[m.start() + a] = new[c:d]
            records.append({'number': number, 'before': old, 'after': new, 'occurrences': len(matches)})
        offset = 0
        for node, attr in slots:
            text = getattr(node, attr)
            value = ''.join(additions.get(offset + i, '') + c for i, c in enumerate(text))
            setattr(node, attr, value)
            offset += len(text)
        expected_text = ''.join(additions.get(i, '') + c for i, c in enumerate(flat))
        assert ''.join(getattr(n, a) for n, a in slots) == expected_text
        changed[name] = etree.tostring(doc, xml_declaration=True, encoding='UTF-8', doctype='<!DOCTYPE html>', pretty_print=True)
    opf = etree.fromstring(z.read('EPUB/content.opf'))
    opf.find('{http://www.idpf.org/2007/opf}metadata/{http://purl.org/dc/elements/1.1/}title').text = '战锤40K LEX设定汇编 · 插画封面二次校订版'
    identifier = opf.find('{http://www.idpf.org/2007/opf}metadata/{http://purl.org/dc/elements/1.1/}identifier')
    identifier.text = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, identifier.text + ':spacing-review-2'))
    for meta in opf.findall('{http://www.idpf.org/2007/opf}metadata/{http://www.idpf.org/2007/opf}meta'):
        if meta.get('property') == 'dcterms:modified':
            meta.text = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    changed['EPUB/content.opf'] = etree.tostring(opf, xml_declaration=True, encoding='UTF-8', pretty_print=True)
    with zipfile.ZipFile(TARGET, 'w') as out:
        for info in z.infolist():
            out.writestr(info, changed.get(info.filename, z.read(info.filename)))

(REPORTS / '人工复核修订.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
print(json.dumps({'file': str(TARGET), 'manual_corrections': sum(r['occurrences'] for r in records), 'manual_articles': len({r['number'] for r in records})}, ensure_ascii=False))
