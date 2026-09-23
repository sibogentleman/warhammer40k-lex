import json,re
from pathlib import Path
base=Path('精校工作稿/工作数据');src=json.loads((base/'全书分段底稿.json').read_text());blocks={b['id']:b for a in src for b in a['blocks']}
common={'重型伐木枪':'重机枪','重型火焰枪':'重型火焰喷射器','守望大师':'守望堡主','托尔克马达·科特兹':'托尔克马达·克提兹','塞姆-罕':'塞姆罕','凯莉娅·德拉克瑟斯':'凯里亚·德拉克瑟斯','基里娅·德拉克斯':'凯里亚·德拉克瑟斯','马尔多瓦·柯肯':'马尔多瓦·科尔泉'}
specific={'A0101-B0041':{'审判官领主':'领主审判官'},'A0134-B0088':{'保民官':'护民官'},'A0138-B0019':{'保民官':'护民官'},'A0156-B0102':{'火卫二':'迪莫斯'},'A0170-B0035':{'亵渎者':'污染者'},'A0781-B0066':{'备用音阵发射器':'备用通讯器'},'A0833-B0014':{'风暴忠嗣军首席利奥卡杜斯':'风暴忠嗣统领利奥卡杜斯'},'A0833-B0050':{'风暴兵指挥官奈奥德':'风暴忠嗣队长奈奥德'},'A0836-B0119':{'保民官':'护民官'}}
core={}
for line in (base/'核心术语定译.tsv').read_text().splitlines()[1:]:
 c=line.split('\t')
 if len(c)==6:core[c[0]]=c
for folder,lo,hi in [('0101-0175',101,175),('0316-0400',316,400),('0776-0850',776,850)]:
 p=base/'并行审校'/folder;e=json.loads((p/'edits.json').read_text());changes=0
 for a in src:
  if not lo<=a['number']<=hi:continue
  for b in a['blocks']:
   if b['language']!='zh':continue
   old=e.get(b['id'],b['text']);s=old
   for f,t in {**common,**specific.get(b['id'],{})}.items():s=s.replace(f,t)
   if s!=old:e[b['id']]=s;changes+=1
 (p/'edits.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
 rows=[]
 for line in (p/'terms.tsv').read_text().splitlines():
  c=line.split('\t')
  if len(c)==6:
   for f,t in common.items():c[1]=c[1].replace(f,t)
   if c[0]=='Tribune':c[1]='护民官'
   if c[0]=='Deimos':c[1]='迪莫斯'
   if c[0]=='Tempestor Prime Liocardus':c[1]='风暴忠嗣统领利奥卡杜斯'
   if c[0]=='Tempestor Naiod':c[1]='风暴忠嗣队长奈奥德'
   if c[0] in ['Heavy stubber','Heavy flamer','Multi-melta','Vox-caster','Tempestor','Tempestor Prime','Kyria Draxus','Defiler','Watch Master'] and c[0] in core:c=core[c[0]]
  rows.append('\t'.join(c))
 (p/'terms.tsv').write_text('\n'.join(rows)+'\n')
 print(folder,changes,'updated blocks')
# Annotation holds semantic scopes, not a second purported official certification.
p=base/'并行审校/0101-0175/notes.json';n=json.loads(p.read_text());n['A0156-B0102']=n.get('A0156-B0102','')+' Deimos 按全书统一暂定为迪莫斯，原稿火卫二留对照；同名天体。';n['A0134-B0088']=n.get('A0134-B0088','')+' Tribunes 此处为护教军精英类别，译名词根统一护民官，不与禁军同名职衔混并组织身份。';n['A0138-B0019']=n.get('A0138-B0019','')+' Tribune 此处在辅军精锐的等级列表中，沿护民官词根；不是在说帝皇禁军职衔。';p.write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
# Exact structural checks and English preservation on Chinese mixed blocks.
for folder,lo,hi in [('0101-0175',101,175),('0316-0400',316,400),('0776-0850',776,850)]:
 p=base/'并行审校'/folder;errs=[]
 for fn in ['edits','notes','titles','additions','reviewed']:o=json.loads((p/(fn+'.json')).read_text())
 e=json.loads((p/'edits.json').read_text());r=json.loads((p/'reviewed.json').read_text())
 if sorted(r)!=list(range(lo,hi+1)):errs.append('reviewed range mismatch')
 for k,v in e.items():
  if k not in blocks or blocks[k]['language']!='zh' or not lo<=int(k[1:5])<=hi:errs.append(k+' invalid target')
  elif re.match(r'^[A-Za-z]',blocks[k]['text']):
   prefix=re.split(r'[\u4e00-\u9fff]',blocks[k]['text'],maxsplit=1)[0].rstrip()
   if prefix and not v.startswith(prefix):errs.append(k+' changed Latin prefix: '+prefix)
 for i,row in enumerate((p/'terms.tsv').read_text().splitlines(),1):
  if len(row.split('\t'))!=6:errs.append('TSV row '+str(i))
 for k,v in json.loads((p/'additions.json').read_text()).items():
  if k not in blocks or blocks[k]['language']!='en':errs.append(k+' invalid addition')
 print(folder,{'reviewed':len(r),'edits':len(e),'errors':errs})
