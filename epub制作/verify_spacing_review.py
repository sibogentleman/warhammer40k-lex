from pathlib import Path
from lxml import etree
from collections import Counter
import json, re, zipfile, hashlib, time
from recover_source_spacing import compact, gap_positions, aligned_blocks, content_nodes

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / 'reports/英文二次校对'
inventory = json.loads((REPORTS/'原始网页文本.json').read_text())
restored = {r['number']: r for r in json.loads((REPORTS/'恢复原始空格记录.json').read_text())}
manual = json.loads((REPORTS/'人工复核修订.json').read_text())
stats = Counter()
residual = {}
with zipfile.ZipFile(ROOT.parent/'战锤40K_LEX设定汇编_插画封面版.epub') as old, zipfile.ZipFile(ROOT.parent/'战锤40K_LEX设定汇编_插画封面二次校订版.epub') as new:
    assert set(old.namelist()) == set(new.namelist())
    article_files = {f'EPUB/text/article-{i:04d}.xhtml' for i in range(1,1588)}
    for name in new.namelist():
        if name not in article_files and name != 'EPUB/content.opf':
            assert old.read(name) == new.read(name), name
            stats['unchanged_nonarticle_files'] += 1
            if name.startswith('EPUB/images/'):
                stats['byte_identical_images_including_cover'] += 1
    for row in inventory:
        i = row['number'];name = f'EPUB/text/article-{i:04d}.xhtml'
        olddoc = etree.fromstring(old.read(name));newdoc = etree.fromstring(new.read(name))
        before = ''.join(''.join(n.itertext()) for n in content_nodes(olddoc))
        after = ''.join(''.join(n.itertext()) for n in content_nodes(newdoc))
        b, a = compact(before), compact(after)
        # Reverse only the four explicitly reviewed hyphens; all other changes
        # must consist solely of whitespace or logged source-absent asterisks.
        for edit in manual:
            if edit['number'] == i and compact(edit['after']) != compact(edit['before']):
                a = a.replace(compact(edit['after']), compact(edit['before']), edit['occurrences'])
        bi = ai = removed = 0
        while bi < len(b):
            if ai < len(a) and b[bi] == a[ai]:
                bi += 1;ai += 1
            else:
                assert b[bi] == '*', (i, b[max(0,bi-30):bi+30], a[max(0,ai-30):ai+30])
                bi += 1;removed += 1
        assert ai == len(a), (i, 'unexpected added non-whitespace text')
        assert removed == restored.get(i,{}).get('source_absent_markers_removed',0)
        stats['verified_removed_source_absent_markers'] += removed
        source = '';wanted = set()
        for part in row['parts']:
            text,gaps = gap_positions(part)
            wanted.update(len(source)+p for p in gaps)
            source += text
        current, existing = gap_positions(after)
        mapper = [-1]*len(source)
        for sa,ca,size in aligned_blocks(row['parts'],current):
            mapper[sa:sa+size] = range(ca,ca+size)
        for p in wanted:
            left,right = mapper[p-1],mapper[p]
            if left >= 0 and right == left+1:
                assert right in existing, (i, 'missing source whitespace', source[max(0,p-30):p+30])
                stats['verified_original_space_boundaries'] += 1
            else:
                stats['boundaries_at_edited_characters'] += 1
        for edit in manual:
            if edit['number'] == i:
                assert edit['after'] in after, edit
                assert not re.search(r'(?<![A-Za-z])'+re.escape(edit['before'])+r'(?![A-Za-z])', after), edit
        for node in content_nodes(newdoc):
            for text in node.itertext():
                for m in re.finditer(r'\b[A-Za-z]*[a-z][A-Z][A-Za-z]*\b',text):
                    residual.setdefault(m.group(),set()).add(i)
        stats['articles_verified'] += 1
    for term in ['McNeill','McConnell','AIs','BONEheads','anathame','MkII']:
        stats['preserved_proper_forms_checked'] += 1
        assert any(term in ''.join(etree.fromstring(new.read(n)).itertext()) for n in article_files),term
stats['manual_corrections'] = sum(r['occurrences'] for r in manual)
(REPORTS/'空格与内容保持核验.json').write_text(json.dumps({'passed':True,'stats':dict(stats)},ensure_ascii=False,indent=2))
(REPORTS/'最终混合大小写词复核.json').write_text(json.dumps({k:sorted(v) for k,v in residual.items()},ensure_ascii=False,indent=2))
print(json.dumps({'passed':True,'stats':dict(stats)},ensure_ascii=False))
