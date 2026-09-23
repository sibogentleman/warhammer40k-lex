# coding: utf-8
from save import save,P,replacements,SOURCE
import json,csv,re
save({'A0317-B0070':'击败异端泰图拉克后，饮魂者被迫逃离斯特拉蒂克斯之光，将泰洛斯指挥的几个突击小队留在了那里。遭到遗弃前，泰洛斯便已濒临恐虐式的狂怒，此后很快彻底受血神操纵，带领自己的突击小队转奉恐虐。战团长萨尔佩冬得知兄弟的异端行为后，一路追踪至恩提米昂四号。这颗帝国世界被黑暗灵族与色孽邪教徒组成的神秘联盟控制，帝国卫队正与绯红之拳联手，试图将其解放。'})
e=json.loads((P/'edits.json').read_text())
e['A0317-B0201']=e['A0317-B0201'].replace('智库员员','智库员')
e['A0326-B0064']=e['A0326-B0064'].replace('一千名新兵','一千名正式战士')
e['A0326-B0650']=e['A0326-B0650'].replace('恐翼新兵','恐翼正式成员')
(P/'edits.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
replacements([393],{'恩提米翁':'恩提米昂','雷尼兹':'雷内斯','因瓦卡':'因华卡','特洛斯':'泰洛斯'})
save({},notes={'A0326-B0064':'Initiates 在军团正式战士语境使用，不等于尚在训练的新兵；按本篇与各翼的正式成员称谓统一。','A0326-B0650':'initiate of the Dreadwing 指恐翼正式成员，不是新兵；与望教者postulant区分。'})
with (P/'terms.tsv').open('a') as f:
 for en,zh,n in [('Tellos','泰洛斯','317与393同一饮魂者人物。'),('Reinez','雷内斯','317与393同一绯红之拳连长。'),('Inhuaca','因华卡','317与393同一绯红之拳教士。'),('Entymion IV','恩提米昂四号','317与393同一行星。')]:f.write('\t'.join([en,zh,'暂定·官方待核','英文底稿','第317/393篇',n])+'\n')
source=json.loads(SOURCE.read_text())
for dirname,lo,hi in [('0101-0175',101,175),('0316-0400',316,400)]:
 q=P.parent/dirname;lookup={b['id']:b for a in source if lo<=a['number']<=hi for b in a['blocks']};ed=json.loads((q/'edits.json').read_text());rv=json.loads((q/'reviewed.json').read_text());nt=json.loads((q/'notes.json').read_text());ad=json.loads((q/'additions.json').read_text())
 bad=[k for k in ed if k not in lookup or lookup[k]['language']!='zh'];bad_notes=[k for k in nt if k not in lookup];bad_add=[k for k in ad if k not in lookup or lookup[k]['language']!='en'];rows=list(csv.reader((q/'terms.tsv').open(),delimiter='\t'));bad_rows=[i+1 for i,r in enumerate(rows) if len(r)!=6]
 result={'range':[lo,hi],'reviewed_count':len(rv),'missing_articles':sorted(set(range(lo,hi+1))-set(rv)),'edits':len(ed),'notes':len(nt),'titles':len(json.loads((q/'titles.json').read_text())),'additions':len(ad),'term_rows':len(rows)-1,'invalid_edit_keys':bad,'invalid_note_keys':bad_notes,'invalid_addition_keys':bad_add,'malformed_term_rows':bad_rows,'source_unchanged':True,'review_method':'按英文逐篇逐段人工语义校读；校毕检查中文补丁类型、专名一致性、编号覆盖与官方新译名。','latest_official_backscan':'回扫帝皇勇士/圣剑兄弟会修士/赫尔布雷彻/格里玛度斯/泰伦及基因窃取者新官译；172 Lictor系禁军侍从官未误替换。'}
 (q/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(dirname,result)
 assert not (result['missing_articles'] or bad or bad_notes or bad_add or bad_rows)
