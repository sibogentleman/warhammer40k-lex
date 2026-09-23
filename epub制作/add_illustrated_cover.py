from pathlib import Path
from lxml import etree
import zipfile, hashlib, json, datetime

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'战锤40K_LEX设定汇编_离线校订版.epub'
TARGET=ROOT/'战锤40K_LEX设定汇编_插画封面版.epub'
COVER=ROOT/'战锤40K_设定汇编_封面.png'
NS={'o':'http://www.idpf.org/2007/opf','h':'http://www.w3.org/1999/xhtml'}
with zipfile.ZipFile(SOURCE) as src:
    opf=etree.fromstring(src.read('EPUB/content.opf'))
    cover_item=opf.xpath('//o:item[@properties="cover-image"]',namespaces=NS)
    assert len(cover_item)==1
    old_image='EPUB/'+cover_item[0].get('href')
    cover_item[0].set('href','images/cover.png')
    cover_item[0].set('media-type','image/png')
    for meta in opf.xpath('//o:meta[@property="dcterms:modified"]',namespaces=NS):
        meta.text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    page=etree.fromstring(src.read('EPUB/text/cover.xhtml'))
    imgs=page.xpath('//h:img',namespaces=NS)
    assert len(imgs)==1
    imgs[0].set('src','../images/cover.png')
    imgs[0].set('alt','战锤40K 设定汇编：金色书名与星图环绕的哥特式帝国巨舰。LEX 专栏，中英双语，离线校订版。')
    changes={
        'EPUB/content.opf':etree.tostring(opf,xml_declaration=True,encoding='UTF-8',pretty_print=True),
        'EPUB/text/cover.xhtml':etree.tostring(page,xml_declaration=True,encoding='UTF-8',doctype='<!DOCTYPE html>',pretty_print=True),
        'EPUB/images/cover.png':COVER.read_bytes(),
    }
    with zipfile.ZipFile(TARGET,'w') as dst:
        for item in src.infolist():
            if item.filename==old_image:continue
            dst.writestr(item,changes.get(item.filename,src.read(item.filename)))
        dst.writestr('EPUB/images/cover.png',changes['EPUB/images/cover.png'],compress_type=zipfile.ZIP_STORED)

with zipfile.ZipFile(SOURCE) as old, zipfile.ZipFile(TARGET) as new:
    assert new.testzip() is None
    assert new.infolist()[0].filename=='mimetype'
    assert new.infolist()[0].compress_type==zipfile.ZIP_STORED
    allowed={'EPUB/content.opf','EPUB/text/cover.xhtml',old_image}
    unchanged=0
    for name in old.namelist():
        if name not in allowed:
            assert old.read(name)==new.read(name),name
            unchanged+=1
    assert new.read('EPUB/images/cover.png')==COVER.read_bytes()
    assert old_image not in new.namelist()
    manifests=etree.fromstring(new.read('EPUB/content.opf')).xpath('//o:item',namespaces=NS)
    assert all('EPUB/'+x.get('href') in new.namelist() for x in manifests)

report={'output':str(TARGET),'cover':str(COVER),'mode':'built-in image_gen',
        'prompt':str(ROOT/'epub制作/封面生成提示词.txt'),'unchanged_package_files':unchanged,
        'all_original_article_text_and_images_preserved':True,'bytes':TARGET.stat().st_size,
        'sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest()}
(ROOT/'epub制作/reports/封面替换检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
