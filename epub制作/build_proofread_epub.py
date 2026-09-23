from pathlib import Path
from lxml import etree
import zipfile,json,re,csv,hashlib,uuid,datetime,collections,posixpath
R=Path(__file__).resolve().parent.parent;W=R/'精校工作稿';D=W/'工作数据';OUT=R/'战锤40K_LEX设定汇编_全书精校版.epub';SRC=R/'战锤40K_LEX设定汇编_插画封面二次校订版.epub'
H='http://www.w3.org/1999/xhtml';EP='http://www.idpf.org/2007/ops';NS={'h':H,'o':'http://www.idpf.org/2007/opf','dc':'http://purl.org/dc/elements/1.1/'}
def tag(e):return etree.QName(e).localname
def clean(t):return re.sub(r'\s+',' ',t).strip()
def unesc(t):return re.sub(r'\\([\\*`\[\]<>])',r'\1',t)
def el(t,text=None,**attrs):
 e=etree.Element('{'+H+'}'+t,**attrs);e.text=text;return e
def serial(d):return etree.tostring(d,encoding='UTF-8',xml_declaration=True,doctype='<!DOCTYPE html>')
C=json.loads((D/'全书分段底稿.json').read_text());progress={int(r['篇号']):r for r in csv.DictReader((W/'精校进度.csv').open(encoding='utf-8-sig'))};titles={};expected={};notes_count=0;changed=0;add_count=0;replacements={};source_hashes={}
with zipfile.ZipFile(SRC) as z:
 for a in C:
  n=a['number'];p=W/progress[n]['稿件路径'];raw=p.read_text();source_hashes[str(p.relative_to(W))]=hashlib.sha256(p.read_bytes()).hexdigest();title=re.sub(r'^#\s*\d+\s*','',raw.splitlines()[0]);titles[n]=title
  name=f'EPUB/text/article-{n:04d}.xhtml';doc=etree.fromstring(z.read(name));body=doc.find('h:body',NS);nodes=[];inside=False
  for e in body:
   if e.get('class')=='metadata':inside=True;continue
   if e.get('class')=='article-links':break
   if inside:nodes.append(e)
  leaves=[]
  def walk(e):
   t=tag(e)
   if t in ['ul','ol','blockquote']:
    for c in e:walk(c)
   elif t=='figure':
    leaves.append(e.find('h:img',NS));cap=e.find('h:figcaption',NS)
    if cap is not None and clean(''.join(cap.itertext())):leaves.append(cap)
   elif t=='li':
    cp=etree.fromstring(etree.tostring(e,with_tail=False))
    for c in list(cp):
     if tag(c) in ['ul','ol']:cp.remove(c)
    if clean(''.join(cp.itertext())):leaves.append(e)
    for c in e:
     if tag(c) in ['ul','ol']:walk(c)
   elif clean(''.join(e.itertext())):leaves.append(e)
  for e in nodes:walk(e)
  assert len(leaves)==len(a['blocks']),(n,len(leaves),len(a['blocks']))
  footnotes=[]
  for b,e in zip(a['blocks'],leaves):
   bid=b['id'];e.set('data-block-id',bid)
   if b['kind']=='image':
    assert Path(e.get('src')).name==Path(b['src']).name;continue
   m=re.search(r'<!-- '+bid+r' -->\n(.*?)<!-- /'+bid+r' -->',raw,re.S);assert m,bid;chunk=m[1].strip();parts=chunk.split('**校注：** ',1);note=parts[1].strip() if len(parts)>1 else '';chunk=parts[0].strip();addition=None
   if '**补译**' in chunk:chunk,addition=chunk.split('**补译**',1);addition=unesc(addition.strip());chunk=chunk.strip()
   if b['kind']=='heading':text=unesc(re.sub(r'^#{2,6}\s+','',chunk.splitlines()[0]))
   elif b['language']=='en':
    text=unesc(chunk.split('**英文原文**',1)[1].strip());assert text==b['text'],bid
   else:
    assert '**校订译文**' in chunk,bid;text=unesc(chunk.split('**校订译文**',1)[1].strip())
   expected[bid]=text
   if text!=b['text']:
    changed+=1;nested=[c for c in e if tag(c) in ['ul','ol']]
    for c in list(e):e.remove(c)
    e.text=text
    for c in nested:e.append(c)
   if addition:
    ae=el('li' if tag(e)=='li' else 'p',addition,**{'class':'zh supplemental','data-addition-id':bid});e.addnext(ae);expected[bid+'-addition']=addition;add_count+=1
   if note:
    notes_count+=1;idx=len(footnotes)+1;fnid='note-'+bid;refid='ref-'+bid
    sup=el('sup',**{'class':'note-ref','id':refid});link=el('a',f'[{idx}]',href='#'+fnid);link.set('{'+EP+'}type','noteref');sup.append(link)
    if tag(e)=='li' and len(e):e.insert(0,sup)
    else:e.append(sup)
    item=el('li',id=fnid);item.set('{'+EP+'}type','footnote');item.append(el('a','↩ ',href='#'+refid));item[-1].tail=note;footnotes.append(item)
  h1=body.find('h:h1',NS);h1.clear();h1.set('id','article-title');h1.text=title;doc.find('h:head/h:title',NS).text=title
  if footnotes:
   section=el('section',**{'class':'editor-notes','id':'editor-notes'});section.append(el('h2','校注'));ol=el('ol');section.append(ol)
   for f in footnotes:ol.append(f)
   end=body.find('h:div[@class="article-links"]',NS)
   if end is None:body.append(section)
   else:end.addprevious(section)
  replacements[name]=serial(doc)
 # Update every navigation label, including previous/next links.
 for name in z.namelist():
  if not name.endswith('.xhtml'):continue
  doc=etree.fromstring(replacements.get(name,z.read(name)))
  for e in doc.xpath('//h:a[@href]',namespaces=NS):
   m=re.search(r'(?:^|/)article-(\d{4})\.xhtml$',e.get('href'))
   if not m:continue
   old=''.join(e.itertext());n=int(m[1]);prefix=''
   if '上一篇' in old:prefix='← 上一篇：'
   elif '下一篇' in old:prefix='下一篇：'
   elif re.match(r'^\s*\d{4}',old):prefix=f'{n:04d} '
   for child in list(e):e.remove(child)
   e.text=prefix+titles[n]
  replacements[name]=serial(doc)
 intro=etree.fromstring(replacements['EPUB/text/intro.xhtml']);body=intro.find('h:body',NS);body.clear()
 for t,text in [('p','WARHAMMER 40,000 · LEX'),('h1','战锤40K 设定汇编'),('p','中英双语 · 全书精校版'),('p','全书1,587篇，按13个分类编排。中文采用2026年9月23日制作本电子书时的精校工作稿，保留英文原文与全部本地配图。'),('h2','阅读说明'),('p','本版以精校中文替换旧译，保持双语阅读顺序。校注集中放在每篇末尾，点击正文注号可跳转，点击回箭头可返回。对照用的原译与完整CSV术语表保留在另行交付的Markdown编辑稿中。'),('p','目录、分类页和前后篇链接已同步精校篇名。图片可离线阅读；原文来源等外部链接需要联网。'),('h2','精校与术语'),('p','全书已逐段对照英文校读，修正错漏译、指代、数量、年代与不通顺的中文，并复核跨篇术语一致性。优先参考Games Workshop官方中文；未查得官方依据的译名仍为暂定。校注说明原文疑点、译名依据及同形词的不同含义。'),('p','沿用已确认的恶魔审判庭、异端审判庭、异形审判庭，首次出现附原稿别名。未经核实，不以记忆中的设定覆盖英文底稿。'),('p','原专栏作者：帝国神选罐头。译文、原作与配图权利归各自权利人所有。')]:body.append(el(t,text))
 p=el('p');p.append(el('a','进入全书目录 →',href='nav.xhtml'));body.append(p);replacements['EPUB/text/intro.xhtml']=serial(intro)
 opf=etree.fromstring(z.read('EPUB/content.opf'));opf.find('o:metadata/dc:title',NS).text='战锤40K LEX设定汇编 · 全书精校版';opf.find('o:metadata/dc:identifier',NS).text='urn:uuid:'+str(uuid.uuid4());opf.find('o:metadata/dc:description',NS).text='1587篇中英双语设定条目；中文采用全书精校稿，保留插画封面、离线图片及逐篇校注。';opf.find('o:metadata/o:meta[@property="dcterms:modified"]',NS).text=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');replacements['EPUB/content.opf']=etree.tostring(opf,xml_declaration=True,encoding='UTF-8')
 replacements['EPUB/book.css']=z.read('EPUB/book.css')+b'\n.note-ref { font-size:.65em; text-indent:0; vertical-align:super; margin-left:.2em; }\n.editor-notes { border-top:1px solid #bbb; margin-top:2em; font-size:.83em; line-height:1.65; }\n.editor-notes li { overflow-wrap:anywhere; text-align:left; }\n.supplemental { border-left:2px solid #a58c60; padding-left:.6em; }\n'
 with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
  out.writestr('mimetype',b'application/epub+zip',compress_type=zipfile.ZIP_STORED)
  for name in z.namelist():
   if name!='mimetype':out.writestr(name,replacements.get(name,z.read(name)))
# Verify all rendered content against the current Markdown, not just presence of article files.
with zipfile.ZipFile(OUT) as z,zipfile.ZipFile(SRC) as old:
 count=0
 for a in C:
  d=etree.fromstring(z.read(f'EPUB/text/article-{a["number"]:04d}.xhtml'))
  for e in d.xpath('//*[@data-block-id or @data-addition-id]'):
   if tag(e)=='img':continue
   bid=e.get('data-block-id') or e.get('data-addition-id')+'-addition';cp=etree.fromstring(etree.tostring(e,with_tail=False))
   for c in list(cp):
    if tag(c) in ['ul','ol'] or c.get('class')=='note-ref':cp.remove(c)
   assert clean(''.join(cp.itertext()))==clean(expected[bid]),bid;count+=1
 for name in old.namelist():
  if name.startswith('EPUB/images/'):assert z.read(name)==old.read(name),name
 assert z.testzip() is None
report={'epub':str(OUT),'articles':len(C),'verified_text_blocks':count,'revised_blocks':changed,'added_translations':add_count,'editor_notes':notes_count,'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'markdown_sha256':source_hashes}
P=R/'epub制作/reports/全书精校版';P.mkdir(exist_ok=True);(P/'制作与逐段核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='markdown_sha256'},ensure_ascii=False))
