from pathlib import Path
from lxml import etree
from urllib.parse import urlparse, unquote
import zipfile,json,collections,re,hashlib,posixpath,sys

ROOT=Path(__file__).resolve().parent
epub=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'战锤40K_LEX设定汇编_离线校订版.epub'
report_path=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else ROOT/'reports/最终完整性检查.json'
stats=collections.Counter();errors=[];raw=[]
ns={'h':'http://www.w3.org/1999/xhtml','o':'http://www.idpf.org/2007/opf'}
with zipfile.ZipFile(epub) as z:
    names=set(z.namelist())
    assert z.infolist()[0].filename=='mimetype'
    assert z.infolist()[0].compress_type==zipfile.ZIP_STORED
    assert z.read('mimetype')==b'application/epub+zip'
    assert z.testzip() is None
    docs={n:etree.fromstring(z.read(n)) for n in names if n.endswith(('.xhtml','.opf','.xml','.svg'))}
    package=docs['EPUB/content.opf']
    manifest={e.get('id'):e for e in package.xpath('//o:manifest/o:item',namespaces=ns)}
    manifested={posixpath.normpath('EPUB/'+e.get('href')) for e in manifest.values()}
    assert manifested=={n for n in names if n.startswith('EPUB/') and not n.endswith('.opf')}
    for itemref in package.xpath('//o:spine/o:itemref',namespaces=ns):assert itemref.get('idref') in manifest
    article_names={f'EPUB/text/article-{n:04d}.xhtml' for n in range(1,1588)}
    assert article_names<=names
    for name,d in docs.items():
        if not name.endswith('.xhtml'):continue
        stats['xhtml_files']+=1
        for e in d.xpath('//*[@src or @href]'):
            for attr in ['src','href']:
                ref=e.get(attr)
                if not ref:continue
                p=urlparse(ref)
                if p.scheme:
                    stats['external_'+attr]+=1
                    if attr=='src':errors.append([name,ref,'external resource'])
                    if p.scheme not in ['http','https','mailto']:errors.append([name,ref,'unexpected scheme'])
                else:
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(p.path))) if p.path else name
                    if target not in names:errors.append([name,ref,'missing file'])
                    elif p.fragment and target in docs and not docs[target].xpath('//*[@id=$id]',id=unquote(p.fragment)):errors.append([name,ref,'missing fragment'])
                    stats['local_'+attr]+=1
        if name in article_names:
            stats['articles']+=1
            stats['body_image_references']+=len(d.xpath('//h:img',namespaces=ns))
            assert d.xpath('count(//h:h1)',namespaces=ns)==1
            for e in d.xpath('//h:p|//h:li|//h:h2|//h:h3',namespaces=ns):
                text=''.join(e.itertext())
                if '**' in text:raw.append([name,text[:300]])
    nav=docs['EPUB/text/nav.xhtml']
    nav_articles=[e.get('href') for e in nav.xpath('//h:nav[@id="toc"]//h:a',namespaces=ns) if e.get('href','').startswith('article-')]
    assert len(nav_articles)==1587 and len(set(nav_articles))==1587
    assert stats['body_image_references']==4004
    stats['unique_embedded_original_images']=sum(n.startswith('EPUB/images/img-') for n in names)
    assert stats['unique_embedded_original_images']==3917
    # One title was corrected; original source metadata is retained separately.
    assert 'AIs' in ''.join(docs['EPUB/text/article-1218.xhtml'].itertext())
    assert not raw,raw
source=Path('/Users/bytedance/Documents/Codex/2026-09-20/https-www-bilibili-com-opus-1117594376438022184/outputs')
fingerprints=json.loads((ROOT/'reports/原始资料校验值.json').read_text())
assert all(hashlib.sha256((source/p).read_bytes()).hexdigest()==digest for p,digest in fingerprints.items())
assert not errors,errors
stats['original_source_files_unchanged']=len(fingerprints)
result={'passed':True,'stats':dict(stats),'errors':errors,'unparsed_bold_markers':raw,'sha256':hashlib.sha256(epub.read_bytes()).hexdigest()}
report_path.write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
