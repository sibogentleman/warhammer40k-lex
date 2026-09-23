from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(a,k,t):e[f'A{a:04d}-B{k:04d}']=t
p(558,283,'狂怒深渊号——特制的深渊级战列舰，由舰队连长扎德基尔指挥；尚未抵达马库拉格发动攻击，便已被重创而失去行动能力。')
p(558,291,'荷鲁斯之乱后，怀言者已知拥有以下舰船：')
p(558,295,'黑暗圣歌号——荒芜使者级战列舰。')
p(558,299,'十字诅咒号——可容纳泰坦的巨型货运舰。')
p(558,301,'神音号——腐尸级巨舰，由黑暗使徒纳赫伦指挥。第三天军的大部分成员在舰上时，它曾在亚空间中失踪数秒。重返现实空间后，舰上船员全部死亡，纳垢花园也已在舰内生根。')
p(558,313,'艾瑞巴斯——怀言者首席教士。')
p(558,319,'阿米里克·凯尔——科技战士。')
p(558,323,'夏芬——教士，后来加入受祝之子。')
p(558,329,'科尔·巴达尔——连长。')
p(558,337,'巴图萨·纳瑞克——侦察战士。')
p(558,339,'库尔·旺达——首席智库员。')
p(558,354,'布里亚斯·德拉克沙尔——曾是第三十四天军的附魔战士兼圣像承载者，现为混沌无畏机甲。')
p(558,358,'埃努萨特——接替阿什卡内兹担任第三十四天军第一侍僧，曾被遗留在神音号上蔓生的纳垢花园中，后由马杜克与萨博泰克救出。')
p(558,362,'马杜克——黑暗使徒，曾任贾鲁克的第一侍僧。')
p(558,364,'科尔·巴达尔——先后担任贾鲁克与马杜克的领唱者。')
p(558,366,'索尔·塔格隆——黑暗使徒，亦为混沌无畏机甲。')
p(558,368,'萨尔贡·埃雷格什——教士，阿巴顿的盟友。')
p(558,372,'隐修士——忠于帝皇的无畏机甲。')
p(558,384,'附魔无畏机甲（荷鲁斯之乱时期）。')
p(560,2,'灰烬之环，是大远征与荷鲁斯之乱时期怀言者特有的部队编制。')
p(560,6,'灰烬之环的设立，是为督行对文化、学识与信仰的摧毁。他们与毁灭者并肩作战，充当圣像破坏者，追索被判为异端教义的人物、著作与圣物，再用喷火手枪将其焚灭。除火焰武器外，灰烬之环战士还配备跳跃背包与耙斧链锯武器，装备方式与突击战士相似。')
e['A0558-B0086']=e['A0558-B0086'].replace('原文称他找到了七艘','他设法找到了七艘')
e['A0558-B0237']=e['A0558-B0237'].replace('怀言者的一个显著特点，是仍保有成体系的教士团体，只是如今称为“黑暗使徒”；本篇将其称作唯一如此的叛徒军团。','怀言者是唯一仍保有成体系教士团体的叛徒军团，只是这些教士如今被称为“黑暗使徒”。')
e['A0558-B0239']=e['A0558-B0239'].replace('本篇将怀言者与黑色军团、死亡守卫并列，称为荷鲁斯之乱后未分裂的三大叛徒军团。','怀言者与黑色军团、死亡守卫并列，是荷鲁斯之乱后未曾分裂的三大叛徒军团之一。')
n.update({'A0558-B0313':'First Chaplain 统一首席教士，与0013艾瑞巴斯条目一致。','A0558-B0323':'later member 为后来加入的成员，不是最后一名成员。','A0558-B0329':'Captain 为连长，原译牧师误认职务。','A0558-B0354':'原译遗漏 possessed，已补附魔战士；该人物后来成为无畏机甲，按源文时间关系保留。','A0560-B0006':'learning 指知识与学术，不是学习动作；iconoclasts 在本军团沿用圣像破坏者。Destroyers 军团毁灭者，不与40K Devastators破坏者小队混同。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
text='''Lorgar|珞珈
Lorgar Aurelian|珞珈·奥瑞利安
Imperial Heralds|帝国传道者
Iconoclasts|圣像破坏者
Chaos Undivided|混沌无分
Colchis|科尔基斯
Sicarus|西卡鲁斯
Ghalmek|加尔梅克
Erebus|艾瑞巴斯
Kor Phaeron|科尔·法伦
Zardu Layak|扎度·拉亚克
Gal Vorbak|受祝之子
Argel Tal|安格尔·塔尔
Serrated Sun|锯齿烈阳
Primordial Truth|原初真理
Ingethel the Ascended|升天者英格泰尔
Ingethel|英格泰尔
Monarchia|摩纳齐亚
Khur|库尔
Corrinos Campaign|科里诺斯战役
Shadow Crusade|暗影远征
Bitter War|苦难战争
Dark Council|黑暗议会
Master of the Union|联合之主
Voice of Lorgar|珞珈之声
Coryphaus|领唱者
First Acolyte|第一侍僧
Martio Imprimis|第一征战
Martio Secundus|第二征战
Anointed|受膏者
Annunake|安努纳克
Harbingers of Death|死亡先驱
Zar Hraval|扎尔·赫拉瓦尔
Fidelitas Lex|信仰之律号
Infidus Imperator|伪帝号
Destiny's Hand|命运之手号
Kamiel|卡米尔号
Furious Abyss|狂怒深渊号
Abyss Class Battleship|深渊级战列舰
Trisagion|三圣颂号
Blessed Lady|受祝女士号
De Profundis|来自深渊号
Dark Chorus|黑暗圣歌号
Crucius Maledictus|十字诅咒号
Vox Dominus|神音号
Ayamandar|阿亚曼达尔号
Infidus Diabolus|背信恶魔号
Firebrand|火焰烙印号
Amyric Kel|阿米里克·凯尔
Xaphen|夏芬
Zadkiel|扎德基尔
Jarulek|贾鲁克
Kol Badar|科尔·巴达尔
Sor Talgron|索尔·塔格隆
Barthusa Narek|巴图萨·纳瑞克
Quor Vondar|库尔·旺达
Paristur|帕里斯图尔
Mothac|莫塔奇
Pridor Vrakon|普里多·弗拉肯
Burias Drak'Shal|布里亚斯·德拉克沙尔
Eliphas the Inheritor|继承者艾里法斯
Enusat|埃努萨特
Ashkanez|阿什卡内兹
Sabtec|萨博泰克
Marduk|马杜克
Sargon Eregesh|萨尔贡·埃雷格什
Maloq Kartho|马洛克·卡尔托
Anchorite|隐修士
Anakatis Kul|阿纳卡蒂斯剑奴
Mhara Gal|附魔无畏机甲
Ashen Circle|灰烬之环
Axe-Rake|耙斧
Asps of the Sacred Sands|圣沙之蛇
Graven Star|镌刻之星
Scold's Bridle|禁言嚼口
Opening Eye|睁开之眼
Sundered Tower|破碎之塔
Tri-Fold Crown|三重王冠
Benediction|祝福星'''
for line in text.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0558—0560','以已读英文和全书现稿统一；未称官方定译，相关源文矛盾见段落校注。'])))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{558,560};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':558,'read_through_block':386,'complete':True},ensure_ascii=False,indent=2))
print('551-560 all complete',len(e),'edits')
