from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(k,t):e[f'A0561-B{k:04d}']=t
p(242,'伽马·穆号——统御级大巡洋舰，荷鲁斯之乱时期。')
p(277,'阿克图里翁——次元铁匠。')
p(289,'所罗门·阿库拉——幽灵军团的折磨大师。')
p(302,'勒拿终结者——荷鲁斯之乱时期。')
p(304,'猎头者——荷鲁斯之乱时期。')
p(305,'Saboteur 破坏专家')
p(306,'Operative 特工')
for k in e:
 if k.startswith('A0561-'):e[k]=e[k].replace('欧兰尼奥斯·佩松','欧良尼乌斯·佩松')
n.update({'A0561-B0277':'Warpsmith 采用已核官方完整单位译名次元铁匠。','A0561-B0302':'本篇使用 Lernaen 与 Lernaean 两种英文拼形，按同一勒拿终结者编制处理，英文原字均保留。','A0561-B0306':'Operative 与本篇前文统一特工，原密探保留在对照。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
text='''Alpharius|阿尔法瑞斯
Omegon|欧米伽
Alpharius Omegon|阿尔法瑞斯·欧米伽
Ghost Legion|幽灵军团
Hydra Dominatus|九头蛇不朽
The Book of Malignancies|邪恶之书
The Apocrypha Terra|泰拉伪经
The Harrowing|折磨
Harrowmaster|折磨大师
Master of Diversion|佯动大师
Sparatoi|斯帕拉托伊
Operative|特工
Effrit Stealth Squad|埃弗里特潜行小队
Lernaen Terminator Squad|勒拿终结者小队
Lernaean|勒拿终结者
Corvus-Alpha|渡鸦-阿尔法
Tesstra Prime|特斯特拉主星
Chondax|香德克斯
Eskrador|埃斯卡多
Alaxxes Nebula|阿拉克斯星云
Actaea|阿克泰
Aeonid Thiel|伊奥尼德·希尔
Branne Nev|布兰·涅夫
Ingo Pech|因格·佩克
Mathias Herzog|马蒂亚斯·赫尔佐格
Armillus Dynat|阿尔梅琉斯·迪纳特
Exodus|伊克索底斯
Phocron|弗克伦
Siridor Vhen|希瑞多·维恩
Sheed Ranko|谢德·兰科
Autilon Skorr|奥帝隆·斯考尔
Arkos|阿尔科斯
Arkturion|阿克图里翁
Quetzel Carthach|奎泽尔·卡尔萨克
Sindri Myr|辛德里·米尔
Occam|奥卡姆
Vykus Skayle|维库斯·斯凯尔
Kassar|卡萨尔
Solomon Akurra|所罗门·阿库拉
Kernax Voldorius|克纳克斯·沃尔多里乌斯
Bale|贝尔
Firaeveus Carron|弗里维斯·卡伦
Cacadius Siron|卡卡迪乌斯·西隆
Deathrow the Warblind|战盲死囚
Anarchy's Heart|无序之心号
Gama Mu|伽马·穆号
Zeta Telios|泽塔终极号
Omega-Echidnax|欧米伽-厄喀德那号
Gamma Lycurgus|伽马·莱库古号
World Prince Campaign|世界王子战役
Cryptosi Purgation|隐生清洗
Guns of Freedom|自由之枪
The Faceless|无面者
The Faithless|无信者
First Strike|首击
Penitent Sons|忏悔之子
The Redacted|修订者
The Rustbloods|锈血者
Scaled Fang|鳞牙
Serpentine Scourge|蛇形灾祸
The Serpent's Teeth|巨蛇之牙
The Shadowed Ones|阴影众
Shrouded Hand|蔽影之手
Sons of Deception|欺骗之子
Sons of the Hydra|九头蛇之子
Sons of Venom|毒液之子
Soulfangs|魂牙
Splintered Sentients|破碎智灵
Subtle Blades|隐秘之刃
The Unsung|未颂者
Brotherhood of the Serpent's Eye|巨蛇之眼兄弟会'''
for line in text.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0561','采用已读上下文；同形的普通词及其他组织名称不机械替换。'])))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{561};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':561,'read_through_block':306,'complete':True},ensure_ascii=False,indent=2))
print('551-561 complete',len(e),'edits',len(by),'terms')
