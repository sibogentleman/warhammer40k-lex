from pathlib import Path
import json,re
D=Path(__file__).resolve().parent
corpus=json.loads((D/'全书分段底稿.json').read_text());a_by={a['number']:a for a in corpus};snap={}
for f in sorted(D.glob('人工精校译文*.json'),key=lambda p:0 if p.stem=='人工精校译文' else int(p.stem.rsplit('-',1)[1])):snap.update(json.loads(f.read_text()))
def standard(s):
 for old,new in [('罗伯特·基里曼','罗保特·基里曼'),('罗布特·基里曼','罗保特·基里曼'),('赤红之马格努斯','红魔马格努斯'),('赤红马格努斯','红魔马格努斯'),('恶魔王子','恶魔亲王'),('莱昂·艾尔庄森','莱昂·艾尔’庄森'),('欧兰尼奥斯·佩松','欧良尼乌斯·佩松'),('欧兰尼奥斯·庇乌斯','欧良尼乌斯·庇乌斯')]:s=s.replace(old,new)
 return re.sub('比拉克(?!尔)','比拉克尔',s)
changed=[]
for folder in [D/'并行审校/0025-0025',D/'并行审校/0251-0325',D/'并行审校/0551-0625']:
 f=folder/'edits.json';ed=json.loads(f.read_text());rv=json.loads((folder/'reviewed.json').read_text())
 for num in rv:
  for b in a_by[num]['blocks']:
   if b['language']=='en' or b['kind']=='image':continue
   before=ed.get(b['id'],snap.get(b['id'],b.get('text','')));after=standard(before)
   if after!=before:ed[b['id']]=after;changed.append(b['id'])
 f.write_text(json.dumps(ed,ensure_ascii=False,indent=2))
 for name in ['notes.json','titles.json']:
  f=folder/name
  if f.exists():
   obj=json.loads(f.read_text());obj={k:standard(v) for k,v in obj.items()};f.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
 # Only change Chinese values; English names and URLs are not rewritten.
 f=folder/'terms.tsv'
 import csv,io
 rows=list(csv.DictReader(f.open(),delimiter='\t'))
 if rows:
  cols=list(rows[0])
  for row in rows:
   for col in ['采用中文','编辑说明']:row[col]=standard(row.get(col,''))
  with f.open('w',newline='') as stream:w=csv.DictWriter(stream,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(rows)
f=D/'人工精校译文-18.json';ed=json.loads(f.read_text()) if f.exists() else {}
for num in range(1,25):
 for b in a_by[num]['blocks']:
  if b['language']=='en' or b['kind']=='image':continue
  before=ed.get(b['id'],snap.get(b['id'],b.get('text','')));after=standard(before)
  if before!=after:ed[b['id']]=after;changed.append(b['id'])
f.write_text(json.dumps(ed,ensure_ascii=False,indent=2))
(D/'本轮人名回查记录.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2));print(len(changed),'already-reviewed blocks harmonized')
