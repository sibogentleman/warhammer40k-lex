from pathlib import Path
from lxml import etree
from collections import Counter,defaultdict
import json,zipfile,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent
NS={'h':'http://www.w3.org/1999/xhtml'}
CN=re.compile(r'[\u3400-\u9fff]')
tag=lambda e:etree.QName(e).localname
def clean(s):return re.sub(r'\s+',' ',s).strip()
def split_bilingual(s):
    s=clean(s)
    if not CN.search(s) or not re.search('[A-Za-z]',s):return None
    m=re.match(r'^([^\u3400-\u9fff]*[A-Za-z][^\u3400-\u9fff]*)\s*([\u3400-\u9fff].*)$',s)
    if m:
        en,zh=m.groups()
    else:
        m=re.match(r'^([\u3400-\u9fff][^A-Za-z]*?)\s+([A-Za-z].*)$',s)
        if not m:return None
        zh,en=m.groups()
    en=en.strip(' —:：-\t');zh=zh.strip(' —:：-\t')
    if not (2<=len(en)<=95 and 1<=len(zh)<=38):return None
    if re.search(r'[。！？；;!?]',en+zh) or len(en.split())>12:return None
    return en,zh

metadata=json.loads((PROJECT/'epub制作/articles.json').read_text())
terms={};corpus=[];counts=Counter()
def addterm(en,zh,article,source,context):
    en=re.sub(r'\s+',' ',en).strip();key=en.casefold().replace('’',"'")
    r=terms.setdefault(key,{'english':en,'translations':{},'articles':set(),'contexts':[],'sources':set()})
    if zh:r['translations'][zh]=r['translations'].get(zh,0)+1
    r['articles'].add(article);r['sources'].add(source)
    if len(r['contexts'])<3:r['contexts'].append({'article':article,'text':context[:360]})

with zipfile.ZipFile(PROJECT/'战锤40K_LEX设定汇编_插画封面二次校订版.epub') as z:
    for meta in metadata:
        i=meta['number'];doc=etree.fromstring(z.read(f'EPUB/text/article-{i:04d}.xhtml'))
        nodes=[];inside=False
        for e in doc.find('h:body',NS):
            if e.get('class')=='metadata':inside=True;continue
            if e.get('class')=='article-links':break
            if inside:nodes.append(e)
        blocks=[]
        def push(e,kind,depth):
            nonlocal_dummy=None
            text=clean(''.join(e.itertext()))
            if not text:return
            b={'id':f'A{i:04d}-B{len(blocks)+1:04d}','kind':kind,'depth':depth,'text':text,
               'language':'zh' if CN.search(text) else 'en','html':etree.tostring(e,encoding='unicode',with_tail=False)}
            blocks.append(b);counts['blocks']+=1;counts['characters']+=len(text)
            if kind=='heading':counts['headings']+=1
            if kind in ('heading','list','caption'):
                pair=split_bilingual(text)
                if pair:addterm(*pair,i,kind,text)
        def walk(e,depth=0):
            t=tag(e)
            if t in ['ul','ol']:
                for child in e:walk(child,depth+1)
            elif t=='blockquote':
                for child in e:walk(child,depth)
            elif t=='figure':
                image=e.find('h:img',NS);caption=e.find('h:figcaption',NS)
                blocks.append({'id':f'A{i:04d}-B{len(blocks)+1:04d}','kind':'image','depth':depth,'text':'','language':'none','src':image.get('src'),'alt':image.get('alt','')})
                counts['images']+=1
                if caption is not None:push(caption,'caption',depth)
            elif t=='li':
                # Own inline text first, nested lists retain their own records.
                copy=etree.fromstring(etree.tostring(e,with_tail=False))
                for c in list(copy):
                    if tag(c) in ['ul','ol']:copy.remove(c)
                push(copy,'list',depth)
                for c in e:
                    if tag(c) in ['ul','ol']:walk(c,depth)
            else:push(e,'heading' if re.fullmatch('h[1-6]',t) else 'paragraph',depth)
        for e in nodes:walk(e)
        pair=split_bilingual(meta['title'])
        if pair:addterm(*pair,i,'article-title',meta['title'])
        for n,b in enumerate(blocks):
            if b['language']=='zh' and b['kind'] in ['paragraph','list']:
                prev=blocks[n-1] if n else None
                if prev and prev['language']=='en' and prev['kind']==b['kind']:
                    b['english_id']=prev['id'];b['english']=prev['text'];counts['paired_chinese_blocks']+=1
                b['review_status']='待逐段精校'
        corpus.append({k:meta[k] for k in ['number','id','title','major','subpath','url','metadata']}|{'blocks':blocks})
    for name in z.namelist():
        if name.startswith('EPUB/images/'):
            out=ROOT/'图片'/Path(name).name;out.parent.mkdir(exist_ok=True)
            out.write_bytes(z.read(name))
    counts['image_files']=len(list((ROOT/'图片').iterdir()))

for r in terms.values():
    r['articles']=sorted(r['articles']);r['sources']=sorted(r['sources'])
    r['article_count']=len(r['articles'])
termrows=sorted(terms.values(),key=lambda r:(-'article-title' in r['sources'] if False else 0,-r['article_count'],r['english'].casefold()))
(ROOT/'工作数据/全书分段底稿.json').write_text(json.dumps(corpus,ensure_ascii=False))
(ROOT/'工作数据/双语术语候选.json').write_text(json.dumps(termrows,ensure_ascii=False,indent=2))
(ROOT/'工作数据/底稿提取统计.json').write_text(json.dumps(dict(counts)|{'articles':len(corpus),'bilingual_term_candidates':len(termrows)},ensure_ascii=False,indent=2))
print(json.dumps(dict(counts)|{'articles':len(corpus),'bilingual_term_candidates':len(termrows)},ensure_ascii=False))
