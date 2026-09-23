from pathlib import Path
from lxml import etree, html
from PIL import Image
from urllib.parse import urlparse, unquote
import json, re, shutil, hashlib, zipfile, collections, uuid, datetime

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'战锤40K_LEX设定汇编_离线校订版.epub'
PKG=ROOT/'package'; BOOK=PKG/'EPUB'; TEXT=BOOK/'text'; IMAGES=BOOK/'images'
for d in [TEXT,IMAGES,PKG/'META-INF']:d.mkdir(parents=True,exist_ok=True)
NS='http://www.w3.org/1999/xhtml'; EPUB='http://www.idpf.org/2007/ops'; OPF='http://www.idpf.org/2007/opf'; DC='http://purl.org/dc/elements/1.1/'
rows=json.loads((ROOT/'rendered.json').read_text()); downloads=json.loads((ROOT/'image-downloads.json').read_text())
assert len(downloads)==4004 and not any('error' in r for r in downloads)
image_map={};manifest=[];spine=[];stats=collections.Counter();outputs=[];conservation=[]
image_hash_map={}

def add_item(id,href,mime,properties=None):
    item={'id':id,'href':href,'media-type':mime}
    if properties:item['properties']=properties
    manifest.append(item)

for info in sorted(downloads,key=lambda x:x['url']):
    digest=info['sha256']
    if digest not in image_hash_map:
        idx=len(image_hash_map)+1
        ext={'JPEG':'jpg','PNG':'png','GIF':'gif','WEBP':'png'}[info['format']]
        filename=f'img-{idx:04d}.{ext}'; dest=IMAGES/filename
        if info['format']=='WEBP':
            with Image.open(info['path']) as im:
                assert not getattr(im,'is_animated',False),'Animated WebP requires a lossless multi-frame fallback'
                im.save(dest,format='PNG')
            stats['webp_to_png']+=1
        else:shutil.copyfile(info['path'],dest)
        image_hash_map[digest]=filename
        add_item(f'image-{idx}',f'images/{filename}',{'jpg':'image/jpeg','png':'image/png','gif':'image/gif'}[ext])
    image_map[info['url']]=image_hash_map[digest]

shutil.copyfile(ROOT/'book.css',BOOK/'book.css');add_item('style','book.css','text/css')
def el(tag,text=None,**attrs):
    e=etree.Element(tag,**attrs)
    if text is not None:e.text=text
    return e

def document(title,body,name,properties=None,body_class=None):
    root=etree.Element('{'+NS+'}html',nsmap={None:NS,'epub':EPUB})
    root.set('lang','zh-CN');root.set('{http://www.w3.org/XML/1998/namespace}lang','zh-CN')
    head=etree.SubElement(root,'head');etree.SubElement(head,'meta',charset='utf-8');etree.SubElement(head,'title').text=title
    etree.SubElement(head,'link',rel='stylesheet',type='text/css',href='../book.css')
    b=etree.SubElement(root,'body')
    if body_class:b.set('class',body_class)
    for node in body:b.append(node)
    data=etree.tostring(root,xml_declaration=True,encoding='UTF-8',doctype='<!DOCTYPE html>',pretty_print=True)
    path=TEXT/name;path.write_bytes(data)
    ident=name[:-6];add_item(ident,'text/'+name,'application/xhtml+xml',properties)
    outputs.append(path)
    return ident

# Original vector cover: compact and resolution independent, with no remote assets.
cover='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1800" viewBox="0 0 1200 1800">
<rect width="1200" height="1800" fill="#111c28"/>
<rect x="70" y="70" width="1060" height="1660" fill="none" stroke="#a89164" stroke-width="2"/>
<rect x="88" y="88" width="1024" height="1624" fill="none" stroke="#57616b"/>
<g fill="none" stroke="#596774" opacity=".5"><circle cx="600" cy="890" r="390"/><circle cx="600" cy="890" r="300"/>
<ellipse cx="600" cy="890" rx="440" ry="145" transform="rotate(-25 600 890)"/>
<path d="M600 405V1375M115 890H1085M260 550L940 1230M260 1230L940 550"/></g>
<g fill="#e1cea2"><circle cx="208" cy="720" r="6"/><circle cx="923" cy="1112" r="8"/><circle cx="716" cy="521" r="4"/>
<circle cx="871" cy="633" r="5"/><circle cx="392" cy="1174" r="5"/><circle cx="599" cy="1349" r="4"/></g>
<rect x="170" y="620" width="860" height="525" fill="#111c28" opacity=".92"/>
<g text-anchor="middle" font-family="PingFang SC, Noto Sans CJK SC, sans-serif">
<text x="600" y="270" fill="#c4ae7e" font-size="27" letter-spacing="10">LEXICANUM · ARCHIVE</text>
<text x="600" y="758" fill="#f0eadd" font-size="115" font-weight="600">战锤 40K</text>
<text x="600" y="907" fill="#f0eadd" font-size="87" font-weight="500">设定汇编</text>
<path d="M430 977H770" stroke="#c4ae7e" stroke-width="2"/>
<text x="600" y="1059" fill="#c4ae7e" font-size="30" letter-spacing="6">LEX 专栏 · 中英双语</text>
<text x="600" y="1455" fill="#c4ae7e" font-size="30">1,587 篇条目　·　13 个分类</text>
<text x="600" y="1530" fill="#c3c7cd" font-size="25">帝国神选罐头　译文与专栏整理</text>
<text x="600" y="1610" fill="#7f8b98" font-size="22" letter-spacing="4">离线校订版 · 2026.09</text>
</g></svg>'''
(IMAGES/'cover.svg').write_text(cover);add_item('cover-image','images/cover.svg','image/svg+xml','cover-image')
cover_img=el('img',src='../images/cover.svg',alt='战锤40K 设定汇编：LEX 专栏，中英双语离线校订版',**{'class':'cover-image'})
spine.append(document('封面',[cover_img],'cover.xhtml',body_class='cover'))

edits=json.loads((ROOT/'reports/文字校对明细.json').read_text())
substantive=[e for e in edits if not e['type'].startswith('恢复')]
intro=[el('p','WARHAMMER 40,000 · LEX',**{'class':'eyebrow'}),el('h1','战锤40K 设定汇编',**{'class':'book-title'}),el('p','中英双语 · 离线校订版',**{'class':'subtitle'}),
       el('p','本书收录原目录中的 1,587 篇专栏，按 13 个非空分类整理，保留中文译文、英文正文、图片、图注及来源信息。',**{'class':'lead'}),
       el('p','原专栏作者：帝国神选罐头'),el('p','原资料生成于 2026 年 9 月 21 日；本版整理于同日。'),el('h2','阅读说明'),
       el('p','使用阅读器目录可进入分类与任意条目；每篇文末提供前后篇和分类目录入口。正文与 4,004 处插图均已嵌入本书，可离线阅读。相同图片按内容去重，保留原有分辨率。'),
       el('p','原始资料的“全量汇编”文件实际只含“人类帝国”部分。本版以 chapters 内完整分章及条目清单交叉核对，收录编号 1—1587，未重复叠加总文件。原目录中的空分类不单独成章，已有分类名称及文章归属予以保留。'),
       el('h2','校订说明'),el('p','本版对全文进行排版修复，并修正已核实的重复字、明显错别字、英文拼写和语法问题；少数中文句子依据紧邻的英文正文校正指代、并列关系或语序。专有名词和不确定的译法尽量保留。'),
       el('p','这是适度校订版，并非逐句重新翻译或对战锤设定进行全面考据。英文原文也可能含有原有疏漏；需要辨析译文时，可参考保留的双语正文及原页面。完整修改记录另附于交付目录。'),
       el('p','原页面标题、作者及发布时间作为来源信息原样保留。正文中指向已收录条目的链接尽可能改为书内链接；原页面、未收录文章和延伸阅读等外部链接仍需联网打开。'),
       el('h2','来源')]
sourcep=el('p');sourcep.append(el('a','B 站 LEX 专栏总目录',href='https://www.bilibili.com/opus/1117594376438022184'));intro.append(sourcep)
intro.append(el('p','译文、原作与配图的权利归各自权利人所有。本文件为用户所提供资料的整理阅读版本。',**{'class':'small'}))
tocp=el('p');tocp.append(el('a','进入全书目录 →',href='nav.xhtml'));intro.append(tocp)
spine.append(document('扉页与阅读说明',intro,'intro.xhtml'))

categories=collections.OrderedDict()
for r in rows:categories.setdefault(r['major'],[]).append(r)
cat_ids={name:f'category-{i:02d}' for i,name in enumerate(categories,1)}
urlmap={}
for r in rows:
    target=f'article-{r["number"]:04d}.xhtml'
    urlmap['opus/'+r['id']]=target
    if r.get('cv'):urlmap['read/'+r['cv']]=target

def local_target(url):
    p=urlparse(url)
    if p.netloc in ('www.bilibili.com','bilibili.com','m.bilibili.com'):
        return urlmap.get(p.path.strip('/'))

def clean_body(row):
    root=html.fragment_fromstring(row['html'],create_parent='div')
    # Intra-article prose is untrusted input. No active or unsupported content.
    for node in list(root.iter()):
        if node.tag in ['script','style','iframe','object','embed','input']:
            node.drop_tree();stats['removed_active_nodes']+=1
        for k in list(node.attrib):
            if k.lower().startswith('on') or k in ('style','class','id'):del node.attrib[k]
    # Whitespace repairs around emphasis use the parsed tree to avoid confusing
    # closing markers with opening markers in long multi-emphasis paragraphs.
    for node in root.iter():
        if node.tag not in ('em','strong'):continue
        text=''.join(node.itertext())
        if node.tail and text and re.match(r'[A-Za-z]',node.tail) and re.search(r'[A-Za-z]$',text):
            node.tail=' '+node.tail;stats['emphasis_spaces']+=1
        par=node.getparent()
        if par is not None and text and re.match(r'[A-Za-z]',text):
            prev=node.getprevious()
            before=prev.tail if prev is not None else par.text
            if before and re.search(r'[A-Za-z]$',before):
                if prev is not None:prev.tail=before+' '
                else:par.text=before+' '
                stats['emphasis_spaces']+=1
    for a in root.findall('.//a'):
        href=a.get('href','')
        target=local_target(href)
        if target:a.set('href',target);stats['internal_links']+=1
        elif href.startswith(('javascript:','data:')):a.attrib.pop('href');stats['removed_active_links']+=1
    pic_index=0
    for img in root.findall('.//img'):
        pic_index+=1;url=img.get('src');assert url in image_map,(row['number'],url)
        img.set('src','../images/'+image_map[url]);img.set('alt',f'{row["title"]} · 插图 {pic_index}')
        stats['image_references']+=1
        parent=img.getparent()
        if parent.tag=='p' and len(parent)==1 and not (parent.text or '').strip() and not (img.tail or '').strip():
            parent.tag='figure'
            nxt=parent.getnext()
            if nxt is not None and nxt.tag=='p' and len(nxt)==0:
                caption=''.join(nxt.itertext()).strip()
                if 1<len(caption)<=240 and not re.search(r'[。！？.!?]$',caption) and not caption.startswith(('http','- ')):
                    nxt.tag='figcaption';nxt.getparent().remove(nxt);parent.append(nxt)
                    img.set('alt',caption);stats['captions']+=1
    heading_number=0
    for node in list(root):
        if node.tag != 'p':continue
        txt=''.join(node.itertext()).strip()
        if len(node)==1 and node[0].tag=='strong' and not (node.text or '').strip() and not (node[0].tail or '').strip() and len(txt)<=110 and not re.search(r'[。！？.!?]$',txt):
            node.tag='h2';heading_number+=1;node.set('id',f'section-{heading_number}');stats['headings']+=1
        elif len(node)==0 and len(txt)<=88 and re.match(r'[A-Z]',txt) and re.search(r'[\u4e00-\u9fff]',txt) and not re.search(r'[。！？.!?；;：:]|https?://',txt):
            node.tag='h3';heading_number+=1;node.set('id',f'section-{heading_number}');stats['subheadings']+=1
    for p in root.findall('.//p'):
        text=''.join(p.itertext()).strip()
        if re.search(r'[\u4e00-\u9fff]',text):p.set('class','zh')
        elif re.search(r'[A-Za-z]',text):p.set('class','en');p.set('lang','en');p.set('{http://www.w3.org/XML/1998/namespace}lang','en')
    # Non-whitespace rendered text must survive structural transformations.
    before=html.fragment_fromstring(row['html'],create_parent='div')
    compact=lambda s:re.sub(r'\s+','',s)
    orig=compact(''.join(before.itertext()));now=compact(''.join(root.itertext()))
    assert orig==now,('Rendered text changed during layout',row['number'])
    conservation.append({'number':row['number'],'text_characters':len(now),'images':pic_index,'rendered_text_preserved':True})
    assert pic_index==row['raw_images'],(row['number'],pic_index,row['raw_images'])
    return list(root)

nav=el('nav');nav.set('{'+EPUB+'}type','toc');nav.set('id','toc');nav.append(el('h1','全书目录'))
navlist=etree.SubElement(nav,'ol')
def navlink(parent,text,target):
    li=etree.SubElement(parent,'li');etree.SubElement(li,'a',href=target).text=text;return li
navlink(navlist,'扉页与阅读说明','intro.xhtml')

for name,group in categories.items():
    cat=cat_ids[name]
    li=navlink(navlist,f'{name}（{len(group)} 篇）',cat+'.xhtml');child=etree.SubElement(li,'ol')
    body=[el('p','LEX · 分类目录',**{'class':'eyebrow'}),el('h1',name),el('p',f'{len(group)} 篇条目',**{'class':'subtitle'})]
    current_path=None;listing=None
    for r in group:
        path=' / '.join(r['subpath']+([r['group']] if r['group'] else []))
        if path!=current_path:
            if path:body.append(el('p',path,**{'class':'toc-group'}))
            listing=el('ol',**{'class':'toc-list'});body.append(listing);current_path=path
        linkli=etree.SubElement(listing,'li');a=etree.SubElement(linkli,'a',href=f'article-{r["number"]:04d}.xhtml')
        etree.SubElement(a,'span',**{'class':'toc-number'}).text=f'{r["number"]:04d}'
        a[-1].tail=' '+r['title']
        navlink(child,f'{r["number"]}. {r["title"]}',f'article-{r["number"]:04d}.xhtml')
    spine.append(document(name+' · 分类目录',body,cat+'.xhtml'))
    for i,r in enumerate(group):
        breadcrumb=' / '.join([r['major']]+r['subpath']+([r['group']] if r['group'] else []))
        body=[el('p',breadcrumb,**{'class':'breadcrumb'}),el('p',f'条目 {r["number"]:04d}',**{'class':'entry-number'}),el('h1',r['title'],id='article-title')]
        md=el('div',**{'class':'metadata'})
        meta=r['metadata']
        md.append(el('p','原页面标题：'+meta.get('原页面标题',r['pageTitle'])))
        md.append(el('p','作者：'+meta.get('作者','帝国神选罐头')+'　｜　'+meta.get('发布时间','')))
        sourcep=el('p');a=el('a','原文来源',href=r['url']);sourcep.append(a)
        if r.get('cv'):a.tail='　'+r['cv']
        md.append(sourcep);body.append(md)
        body.extend(clean_body(r))
        foot=el('p',**{'class':'article-links'})
        links=[]
        if i>0:links.append(('← 前一篇',f'article-{group[i-1]["number"]:04d}.xhtml'))
        links.append(('返回分类目录',cat+'.xhtml'));links.append(('全书目录','nav.xhtml'))
        if i<len(group)-1:links.append(('后一篇 →',f'article-{group[i+1]["number"]:04d}.xhtml'))
        for j,(label,target) in enumerate(links):
            node=el('a',label,href=target);foot.append(node)
            if j<len(links)-1:node.tail='　·　'
        body.append(foot)
        spine.append(document(r['title'],body,f'article-{r["number"]:04d}.xhtml'))

catalog=json.loads((Path('/Users/bytedance/Documents/Codex/2026-09-20/https-www-bilibili-com-opus-1117594376438022184/outputs')/'战锤40K_LEX专栏条目清单.json').read_text())
external_source=Path('/Users/bytedance/Documents/Codex/2026-09-20/https-www-bilibili-com-opus-1117594376438022184/outputs/战锤40K_LEX专栏外链清单.md').read_text()
external_urls=list(dict.fromkeys(re.findall(r'https?://[^\s)<>]+',external_source)))
appendix=[el('h1','附录 · 延伸阅读与外部链接'),el('p','以下链接来自原资料的外链清单，相关正文未另行收录，打开时需要联网。')]
for card in catalog.get('externalReadCards',[]):
    p=el('p');p.append(el('a',card['title'],href=card['url']));appendix.append(p)
ul=el('ul')
for url in external_urls:
    li=el('li');li.append(el('a',url,href=local_target(url) or url));ul.append(li)
appendix.append(ul);spine.append(document('附录 · 延伸阅读与外部链接',appendix,'appendix.xhtml'))
navlink(navlist,'附录 · 延伸阅读与外部链接','appendix.xhtml')
landmarks=el('nav');landmarks.set('{'+EPUB+'}type','landmarks');landmarks.set('hidden','hidden');landmarks.append(el('h2','阅读入口'))
lm=etree.SubElement(landmarks,'ol')
for label,target,typ in [('封面','cover.xhtml','cover'),('目录','nav.xhtml','toc'),('正文','article-0001.xhtml','bodymatter')]:
    li=navlink(lm,label,target);li[0].set('{'+EPUB+'}type',typ)
document('全书目录',[nav,landmarks],'nav.xhtml','nav');spine.insert(2,'nav')

uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://www.bilibili.com/opus/1117594376438022184/epub-2026-09-21'))
package=etree.Element('{'+OPF+'}package',nsmap={None:OPF,'dc':DC},version='3.0',attrib={'unique-identifier':'book-id'})
metadata=etree.SubElement(package,'metadata')
etree.SubElement(metadata,'{'+DC+'}identifier',id='book-id').text=uid
etree.SubElement(metadata,'{'+DC+'}title').text='战锤40K LEX设定汇编｜离线校订版'
etree.SubElement(metadata,'{'+DC+'}creator').text='帝国神选罐头'
etree.SubElement(metadata,'{'+DC+'}language').text='zh-CN';etree.SubElement(metadata,'{'+DC+'}language').text='en'
etree.SubElement(metadata,'{'+DC+'}description').text='收录1,587篇LEX双语设定专栏、4,004处离线图片引用；分类导航、来源保留与适度文字校订。'
etree.SubElement(metadata,'{'+DC+'}source').text='https://www.bilibili.com/opus/1117594376438022184'
etree.SubElement(metadata,'{'+DC+'}rights').text='译文、原作及配图版权归各自权利人所有。'
etree.SubElement(metadata,'meta',property='dcterms:modified').text='2026-09-21T06:00:00Z'
etree.SubElement(metadata,'meta',property='rendition:layout').text='reflowable'
man=etree.SubElement(package,'manifest')
for item in manifest:etree.SubElement(man,'item',**item)
sp=etree.SubElement(package,'spine',attrib={'page-progression-direction':'ltr'})
for id in spine:etree.SubElement(sp,'itemref',idref=id)
(BOOK/'content.opf').write_bytes(etree.tostring(package,xml_declaration=True,encoding='UTF-8',pretty_print=True))
(PKG/'mimetype').write_text('application/epub+zip')
(PKG/'META-INF/container.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')

with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.write(PKG/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
    for file in sorted(PKG.rglob('*')):
        if file.is_file() and file.name!='mimetype':
            z.write(file,str(file.relative_to(PKG)),compress_type=zipfile.ZIP_STORED if file.suffix in ['.jpg','.png','.gif'] else zipfile.ZIP_DEFLATED)
stats.update({'articles':len(rows),'categories':len(categories),'unique_image_files':len(image_hash_map),'epub_bytes':OUT.stat().st_size})
(ROOT/'reports/制作统计.json').write_text(json.dumps(dict(stats),ensure_ascii=False,indent=2))
(ROOT/'reports/正文完整性核对.json').write_text(json.dumps(conservation,ensure_ascii=False,indent=2))
(ROOT/'reports/图片本地化映射.json').write_text(json.dumps(image_map,ensure_ascii=False,indent=2))
print(json.dumps(dict(stats),ensure_ascii=False))
print(OUT)
