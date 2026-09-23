from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent

def save(article, edits, notes=None, terms=None, title=None, additions=None):
 for fn,new in [('edits.json',edits),('notes.json',notes or {}),('additions.json',additions or {})]:
  target=P/fn;data=json.loads(target.read_text()) if target.exists() else {}
  data.update({(f'A{article:04d}-B{k:04d}' if isinstance(k,int) else k):v for k,v in new.items()})
  target.write_text(json.dumps(data,ensure_ascii=False,indent=2))
 if terms:
  rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
  for en,zh in terms:
   by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿',f'篇{article:04d}','按英文语境沿现稿或修正；官方对应待核。'])))
  with (P/'terms.tsv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
 if title:
  t=P/'titles.json';d=json.loads(t.read_text()) if t.exists() else {};d[str(article)]=title;t.write_text(json.dumps(d,ensure_ascii=False,indent=2))
 rv=set(json.loads((P/'reviewed.json').read_text()))|{article};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
 print(article,'complete')
