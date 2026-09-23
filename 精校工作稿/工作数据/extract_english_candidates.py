from pathlib import Path
from collections import Counter,defaultdict
import json,re,csv,hashlib,io
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'工作数据'
corpus=json.loads((DATA/'全书分段底稿.json').read_text())
bilingual={r['english'].casefold():r for r in json.loads((DATA/'双语术语候选.json').read_text())}
core={r['英文标准词'].casefold():r for r in csv.DictReader((DATA/'核心术语定译.tsv').read_text().splitlines(),delimiter='\t')}
decision_file=DATA/'用户术语决定.json'
decisions=json.loads(decision_file.read_text()) if decision_file.exists() else {}
word=r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ0-9'’\-]*"
pattern=re.compile(r"(?<![A-Za-z])"+word+r"(?:(?:\s+(?:(?:of|the|and|in|on|for|to|von|de|da)\s+)*)"+word+r"){0,8}")
stop=set('A An And As At Be Before But By During Each Even First For From He Her Here His However I If In Into It Its Many More Most Much No Not Now Of On Once One Only Or Other Others Our Over Rather Several She Since So Some Such That The Their Them Then There These They This Those Though Through Thus To Until Upon Was We Were What When Where Whether Which While Who Whose With Without Would You Your After Along All Also Although Among Any Both Despite Due Each Either Else Every Following Furthermore Given Having Hence How Instead Indeed Just Later Like Meanwhile Nevertheless Nor Often Originally Perhaps Prior Recently Second Still Subsequently Third Together Unlike Usually Various Within Yes'.split())
single_exclude=set('Imperial Human Humans Space Marine Marines Chapter Legion Great Dark Black White Red High Lord Lords War Battle World Worlds System Planet Sector Galaxy Mankind Humanity Chaos Imperial Guard'.split())
result={}
for a in corpus:
    blocks=a['blocks']
    for ix,b in enumerate(blocks):
        if b['language']!='en':continue
        for m in pattern.finditer(b['text']):
            value=m.group().strip()
            parts=value.split()
            while parts and parts[0] in stop:parts.pop(0)
            value=' '.join(parts).rstrip('-')
            if not value or len(value)<3 or len(value)>100:continue
            if len(parts)==1 and (value in single_exclude or value in stop):continue
            if re.fullmatch(r'[A-Z]*\d+[A-Z0-9]*',value):continue
            key=value.casefold().replace('’',"'")
            row=result.setdefault(key,{'english':value,'count':0,'articles':set(),'contexts':[]})
            row['count']+=1;row['articles'].add(a['number'])
            if len(row['contexts'])<2:
                zh=blocks[ix+1]['text'] if ix+1<len(blocks) and blocks[ix+1]['language']=='zh' and blocks[ix+1]['kind']==b['kind'] else ''
                row['contexts'].append({'id':b['id'],'english':b['text'],'original_chinese':zh})
rows=[]
for key,r in result.items():
    if r['count']==1 and ' ' not in r['english'] and key not in bilingual and key not in core:continue
    known=core.get(key);bi=bilingual.get(key,{})
    first=r['contexts'][0]
    rows.append(['E-'+hashlib.sha1(key.encode()).hexdigest()[:10],r['english'],known['采用中文'] if known else '',
     known['译名状态'] if known else '英文候选·待识别与定译','；'.join(bi.get('translations',{})),r['count'],len(r['articles']),','.join(f'{i:04d}' for i in sorted(r['articles'])),first['id'],first['english'],first['original_chinese'],decisions.get(key,{}).get('用户决定','')])
rows.sort(key=lambda r:(-r[5],r[1].casefold()))
out=io.StringIO();writer=csv.writer(out);writer.writerow(['候选ID','英文候选','采用中文','状态','原书双语标签译名','英文检出次数','篇数','篇号','示例段落ID','英文上下文','相邻原译','你的定译']);writer.writerows(rows)
p=ROOT/'术语表/英文正文术语候选.csv'
mf=DATA/'导出文件校验值.json';manifest=json.loads(mf.read_text());key=str(p.relative_to(ROOT))
if p.exists() and key in manifest:assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest[key],'手工编辑已存在，拒绝覆盖'
p.write_text(out.getvalue(),encoding='utf-8-sig');manifest[key]=hashlib.sha256(p.read_bytes()).hexdigest();mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(DATA/'英文正文提词统计.json').write_text(json.dumps({'candidates':len(rows),'method':'英文大写名称模式，排除常见句首词；结果为候选，含待排除的普通短语，未冒充逐项语义识别'},ensure_ascii=False,indent=2))
print(json.dumps({'english_candidates':len(rows),'top':[[r[1],r[5]] for r in rows[:15]]},ensure_ascii=False))
