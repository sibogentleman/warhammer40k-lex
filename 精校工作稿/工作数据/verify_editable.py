from pathlib import Path
from lxml import etree
from collections import Counter
import json,csv,re,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'工作数据'
corpus=json.loads((DATA/'全书分段底稿.json').read_text())
progress=list(csv.DictReader((ROOT/'精校进度.csv').open(encoding='utf-8-sig')))
by_number={int(r['篇号']):r for r in progress}
assert set(by_number)==set(range(1,1588)) and len(progress)==1587
stats=Counter();english_ids=[];allids=[]
compact=lambda s:re.sub(r'\s+','',s)
def unescape(s):return re.sub(r'\\([\\*`\[\]<>])',r'\1',s)
with zipfile.ZipFile(ROOT.parent/'战锤40K_LEX设定汇编_插画封面二次校订版.epub') as z:
    for a in corpus:
        n=a['number'];file=ROOT/by_number[n]['稿件路径'];text=file.read_text()
        d=etree.fromstring(z.read(f'EPUB/text/article-{n:04d}.xhtml'))
        source=[];inside=False
        for e in d.find('{http://www.w3.org/1999/xhtml}body'):
            if e.get('class')=='metadata':inside=True;continue
            if e.get('class')=='article-links':break
            if inside:source.append(''.join(e.itertext()))
        assert compact(''.join(source))==compact(''.join(b['text'] for b in a['blocks'])),(n,'extraction changed source text')
        for b in a['blocks']:
            bid=b['id'];allids.append(bid)
            assert text.count('<!-- '+bid+(' 图片 -->' if b['kind']=='image' else ' -->'))==1,bid
            if b['kind']=='image':
                stats['image_references']+=1
                assert (ROOT/'图片'/Path(b['src']).name).exists()
                continue
            m=re.search('<!-- '+bid+r' -->\n(.*?)<!-- /'+bid+' -->',text,re.S)
            assert m,bid
            if b['kind']=='heading':
                assert unescape(m.group(1)).startswith('##')
                assert b['text'] in unescape(m.group(1)),(bid,'original heading not preserved')
            elif b['language']=='en':
                english_ids.append(bid)
                original_section=m.group(1).split('**英文原文**\n\n',1)[-1]
                original_section=re.split(r'\n\n\*\*(?:补译|校注：)\*\*',original_section,1)[0]
                assert unescape(original_section).strip()==b['text'],bid
                stats['english_blocks_preserved']+=1
            elif b['kind']!='heading':
                m2=re.search(r'<summary>原译文</summary>\n\n(.*?)\n\n</details>',m.group(1),re.S)
                assert m2 and unescape(m2.group(1))==b['text'],bid
                stats['original_chinese_blocks_preserved']+=1
        for ref in re.findall(r'\]\(([^)]+)\)',text):
            if re.match('https?://',ref):continue
            assert (file.parent/ref).resolve().exists(),(file,ref)
        stats['articles_verified']+=1
    for name in z.namelist():
        if name.startswith('EPUB/images/'):
            assert (ROOT/'图片'/Path(name).name).read_bytes()==z.read(name),name
            stats['image_files_byte_identical']+=1
assert len(allids)==len(set(allids))
for p in (ROOT/'术语表').glob('*.csv'):
    rows=list(csv.reader(p.open(encoding='utf-8-sig')))
    assert all(len(r)==len(rows[0]) for r in rows),p
    assert len({r[0] for r in rows[1:]})==len(rows)-1,p
    stats['csv_files_verified']+=1
for p in DATA.glob('人工精校译文*.json'):
    rows=json.loads(p.read_text())
    assert set(rows)<=set(allids),p
    assert not (set(rows)&set(english_ids)),p
stats['language_reviewed_articles']=sum(r['状态'].startswith('中文行文已') for r in progress)
result={'passed':True,'stats':dict(stats)}
(DATA/'完整性核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
