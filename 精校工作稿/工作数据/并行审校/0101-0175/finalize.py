import csv,json,re
from save import save,replacements,P,SOURCE
replacements(range(101,176),{'内务部长':'内政部之主','内务部':'内政部','帝皇圣言录':'神性论','圣言诵读':'神性论信仰','邱利萨斯刺客':'丘里克斯刺客','艾丽西亚·多米尼卡':'艾丽西亚·多米尼克','国教部':'国教会'})
replacements([117],{'国教牧师':'教廷牧师','国教会牧师':'教廷牧师'})
replacements([168],{'国教教会':'国教会'})
save({'A0165-B0023':'收齐灵能者贡赋后，黑船舰长对受押人员初作评估，再驶向巡回路线上的下一世界。满载后便返回泰拉，将灵能者交给灵能学院，然后再次出航，继续无休止的搜寻。若内政部宣布放弃某个世界，黑船便停止到访。审判官常搭乘黑船，借机调查行星上潜在的灵能腐化。'})
t=json.loads((P/'titles.json').read_text());t.update({'124':'机械修会 Adeptus Mechanicus','136':'机神禁卫军 Taghmata Omnissiah','145':'机械教派战斗集群 Cult Mechanicus Battle Congregation','155':'技术祭司 Tech-priest','156':'贤者 Magi','158':'驭电祭司 Electro-priest','171':'仲裁官 Arbitrator','172':'帝皇禁军 Adeptus Custodes','174':'禁军卫队 Custodian Guard','175':'阿拉鲁斯亲卫 Allarus Custodian'})
(P/'titles.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
# Keep source languages immutable; corrections are merged only into Chinese blocks.
s=json.loads(SOURCE.read_text());index={b['id']:b for a in s for b in a['blocks']};ed=json.loads((P/'edits.json').read_text());errors=[]
for bid,x in ed.items():
 b=index.get(bid)
 if not b or b.get('language')!='zh' or b['kind']=='image' or not 101<=int(bid[1:5])<=175:errors.append((bid,'invalid edit target'))
 if not x.strip():errors.append((bid,'empty text'))
# Every Latin lexical run from a mixed source block must remain, including apostrophes and identifiers.
for bid,x in ed.items():
 b=index[bid]
 if re.match('[A-Za-z]',b['text']) and re.search('[\u4e00-\u9fff]',b['text']):
  prefix=re.split('[\u4e00-\u9fff]',b['text'],1)[0].rstrip()
  if prefix and prefix not in x:errors.append((bid,'English prefix missing: '+prefix))
for bid in ['A0169-B0017','A0169-B0032']:
 oldwords=re.findall(r'[A-Za-z]+',index[bid]['text']);newwords=re.findall(r'[A-Za-z]+',ed[bid])
 if oldwords!=newwords:errors.append((bid,'English token sequence changed'))
assert json.loads((P/'reviewed.json').read_text())==list(range(101,176))
(P/'validation.json').write_text(json.dumps({'reviewed':75,'edits':len(ed),'notes':len(json.loads((P/'notes.json').read_text())),'errors':errors},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':75,'edits':len(ed),'errors':errors},ensure_ascii=False))
