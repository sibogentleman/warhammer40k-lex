from pathlib import Path
import json,csv,re,hashlib
D=Path(__file__).resolve().parent
core=list(csv.DictReader((D/'核心术语定译.tsv').open(),delimiter='\t'))
by={r['英文标准词'].casefold():r for r in core}
proposals={}
for folder in sorted((D/'并行审校').iterdir()):
 p=folder/'terms.tsv'
 if not p.exists():continue
 for r in csv.DictReader(p.open(encoding='utf-8-sig'),delimiter='\t'):
  proposals.setdefault(r['英文标准词'].casefold(),[]).append(dict(r,来源文件=folder.name))
conflicts=[]
for key,rows in proposals.items():
 allrows=([dict(by[key],来源文件='既有核心表')] if key in by else [])+rows
 if len({r['采用中文'] for r in allrows})>1:
  conflicts.extend([[key,r['采用中文'],r['译名状态'],r['来源文件'],r['编辑说明']] for r in allrows])
with (D/'并行术语待整合.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['英文词','采用中文','状态','来源','说明']);w.writerows(conflicts)
(D/'并行术语候选快照.json').write_text(json.dumps(proposals,ensure_ascii=False,indent=2))
print('proposal terms',len(proposals),'conflicting keys',len(set(r[0] for r in conflicts)))
