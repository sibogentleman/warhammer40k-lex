from pathlib import Path
from lxml import etree
from collections import Counter
import json,re,zipfile,difflib,time
import sys

ROOT=Path(__file__).resolve().parent
CACHE=Path('/Users/bytedance/Documents/Codex/2026-09-20/https-www-bilibili-com-opus-1117594376438022184/work/cache')
SOURCE=ROOT.parent/'战锤40K_LEX设定汇编_插画封面版.epub'
REPORTS=ROOT/'reports/英文二次校对'
REPORTS.mkdir(exist_ok=True)
NS={'h':'http://www.w3.org/1999/xhtml'}

def inline(nodes):
    result=[]
    for n in nodes or []:
        w=n.get('word') or {};r=n.get('rich') or {};f=n.get('formula') or {}
        result.append(w.get('words') or r.get('text') or r.get('orig_text') or f.get('text') or '')
    return ''.join(result).replace('&nbsp;',' ').replace('\u200b','').replace('\ufeff','')

def blocktexts(b):
    if b.get('heading'):return [inline(b['heading'].get('nodes'))]
    if b.get('text'):return [inline(b['text'].get('nodes'))]
    if b.get('pic'):return [p['comment'] for p in b['pic'].get('pics',[]) if p.get('comment')]
    if b.get('list'):
        return [t for item in b['list'].get('children',[]) for child in item.get('children',[]) for t in blocktexts(child)]
    if b.get('blockquote'):return [t for child in b['blockquote'].get('children',[]) for t in blocktexts(child)]
    if b.get('link_card'):
        c=b['link_card'].get('card') or {};c=c.get('opus') or c.get('archive') or c.get('ugc') or c.get('common') or c
        return [c.get('title') or '']
    return []

def load_source(id):
    s=(CACHE/(id+'.html')).read_text()
    start=s.index('window.__INITIAL_STATE__=')+len('window.__INITIAL_STATE__=')
    obj=json.loads(s[start:s.index(';(function(){',start)])
    detail=obj.get('detail') or (obj.get('opus') or {}).get('detail')
    content=next(m['module_content'] for m in detail['modules'] if m['module_type']=='MODULE_TYPE_CONTENT')
    return [t for b in content['paragraphs'] for t in blocktexts(b) if t.strip()]

def content_nodes(doc):
    body=doc.find('h:body',NS);inside=False;nodes=[]
    for child in body:
        if child.get('class')=='metadata':inside=True;continue
        if child.get('class')=='article-links':break
        if inside:nodes.append(child)
    return nodes

def compact(s):return re.sub(r'\s+','',s)

def slots_in(node):
    if node.text:yield node,'text'
    for child in node:
        yield from slots_in(child)
        if child.tail:yield child,'tail'

def gap_positions(text):
    positions=set();n=0;chars=[]
    for c in text:
        if c.isspace():positions.add(n)
        else:chars.append(c);n+=1
    value=''.join(chars)
    return value,{p for p in positions if 0<p<len(value) and re.search(r'[A-Za-z0-9]',value[p-1:p+1])}

def aligned_blocks(parts,current):
    source=''.join(compact(p) for p in parts)
    if source==current:return [(0,0,len(source))]
    # Anchor whole original paragraphs first. Only small intervals changed by
    # previous proofreading need character alignment, avoiding whole-book guesses.
    blocks=[];sc=cc=0;pending=0
    for part in parts:
        plain=compact(part)
        if not plain:continue
        pos=current.find(plain,cc)
        if pos>=0 and (len(plain)>=12 or pos==cc):
            if pending<sc or cc<pos:
                a=source[pending:sc];b=current[cc:pos]
                for m in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
                    if m.size:blocks.append((pending+m.a,cc+m.b,m.size))
            blocks.append((sc,pos,len(plain)))
            pending=sc+len(plain);cc=pos+len(plain)
        sc+=len(plain)
    if pending<len(source) or cc<len(current):
        a=source[pending:];b=current[cc:]
        for m in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
            if m.size:blocks.append((pending+m.a,cc+m.b,m.size))
    return blocks

def restore():
    inventory=json.loads((REPORTS/'原始网页文本.json').read_text())
    report=[];stats=Counter();changed={};start=time.time()
    with zipfile.ZipFile(SOURCE) as z:
        for row in inventory:
            name=f'EPUB/text/article-{row["number"]:04d}.xhtml'
            doc=etree.fromstring(z.read(name));nodes=content_nodes(doc)
            slots=[slot for node in nodes for slot in slots_in(node)]
            flat=''.join(getattr(n,a) for n,a in slots)
            initial_flat=flat
            current,existing=gap_positions(flat)
            source='';wanted=set()
            for part in row['parts']:
                plain,gaps=gap_positions(part)
                wanted.update(len(source)+p for p in gaps)
                source+=plain
            blocks=aligned_blocks(row['parts'],current)
            # The first conversion also left a few literal Markdown asterisks.
            # Remove only insertion-only runs proven absent from the raw source.
            a0=b0=0;remove=set()
            for a,b,size in blocks+[(len(source),len(current),0)]:
                if a==a0 and b>b0 and current[b0:b].strip('*')=='':
                    remove.update(range(b0,b))
                a0=a+size;b0=b+size
            if remove:
                k=0
                for node,attr in slots:
                    value=getattr(node,attr);out=[]
                    for c in value:
                        if c.isspace():out.append(c)
                        else:
                            if k not in remove:out.append(c)
                            k+=1
                    setattr(node,attr,''.join(out))
                flat=''.join(getattr(n,a) for n,a in slots)
                current,existing=gap_positions(flat)
                blocks=aligned_blocks(row['parts'],current)
                stats['removed_source_absent_markers']+=len(remove)
            mapper=[-1]*len(source)
            for a,b,size in blocks:mapper[a:a+size]=range(b,b+size)
            mapped=set();unmapped=[]
            for p in wanted:
                left,right=mapper[p-1],mapper[p]
                if left>=0 and right==left+1:mapped.add(right)
                else:unmapped.append(p)
            required=mapped-existing
            stats['source_whitespace_boundaries']+=len(wanted)
            stats['aligned_source_boundaries']+=len(mapped)
            stats['unmapped_boundaries']+=len(unmapped)
            stats['restored_spaces']+=len(required)
            if required or remove:
                stats['articles_changed']+=1
                k=0;article_edits=[]
                for node,attr in slots:
                    text=getattr(node,attr);out=[];count=0
                    for c in text:
                        if not c.isspace():
                            if k in required:out.append(' ');count+=1
                            k+=1
                        out.append(c)
                    if count:
                        new=''.join(out)
                        article_edits.append({'before':text,'after':new,'inserted_spaces':count})
                        setattr(node,attr,new)
                for figure in doc.xpath('//h:figure',namespaces=NS):
                    cap=figure.find('h:figcaption',NS);img=figure.find('h:img',NS)
                    if cap is not None and img is not None and compact(img.get('alt',''))==compact(''.join(cap.itertext())):
                        img.set('alt',''.join(cap.itertext()))
                after=''.join(''.join(n.itertext()) for n in nodes)
                assert compact(flat)==compact(after),(row['number'],'non-whitespace content changed')
                changed[name]=etree.tostring(doc,xml_declaration=True,encoding='UTF-8',doctype='<!DOCTYPE html>',pretty_print=True)
                report.append({'number':row['number'],'title':row['title'],'restored_spaces':len(required),'edits':article_edits})
                report[-1]['source_absent_markers_removed']=len(remove)
            if unmapped:
                stats['articles_with_unmapped_boundaries']+=1
                row['unmapped_contexts']=[source[max(0,p-35):p]+' | '+source[p:p+35] for p in sorted(unmapped)]
            stats['articles_checked']+=1
    target=ROOT/'spacing-pass1.epub'
    with zipfile.ZipFile(SOURCE) as old,zipfile.ZipFile(target,'w') as new:
        for item in old.infolist():new.writestr(item,changed.get(item.filename,old.read(item.filename)))
    (REPORTS/'恢复原始空格记录.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    (REPORTS/'原始空格恢复统计.json').write_text(json.dumps(dict(stats),ensure_ascii=False,indent=2))
    (REPORTS/'因既有校订未直接对齐的片段.json').write_text(json.dumps([{'number':r['number'],'contexts':r['unmapped_contexts']} for r in inventory if r.get('unmapped_contexts')],ensure_ascii=False,indent=2))
    print(json.dumps(dict(stats),ensure_ascii=False),'seconds',round(time.time()-start,1),flush=True)

def build_inventory():
    rows=json.loads((ROOT/'articles.json').read_text());inventory=[];stats=Counter();start=time.time()
    with zipfile.ZipFile(SOURCE) as z:
        for row in rows:
            parts=load_source(row['id']);source='\n\n'.join(parts)
            name=f'EPUB/text/article-{row["number"]:04d}.xhtml';doc=etree.fromstring(z.read(name))
            current=''.join(''.join(n.itertext()) for n in content_nodes(doc))
            identical=compact(source)==compact(current)
            stats['exact' if identical else 'changed']+=1
            inventory.append({'number':row['number'],'id':row['id'],'title':row['title'],'parts':parts,'exact':identical})
    (REPORTS/'原始网页文本.json').write_text(json.dumps(inventory,ensure_ascii=False))
    print(dict(stats),'seconds',round(time.time()-start,1),flush=True)
    print('changed articles',[(x['number'],x['title']) for x in inventory if not x['exact']],flush=True)

if __name__=='__main__':
    if '--restore' in sys.argv:restore()
    else:build_inventory()
