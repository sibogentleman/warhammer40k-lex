from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
pairs='''Anhrathe|安赫拉特
Asuryani|阿苏焉尼
Maiden Worlds|少女世界
Crone Worlds|老妪世界
Dathedian|达瑟迪安
Dysjunction|析离
Biel-Tan|比耶坦
Vaul|瓦尔
Kaela Mensha Khaine|血手凯恩
Shuriken|星镖
Shuriken Catapult|星镖枪
Shuriken Cannon|星镖炮
Spirit Stone|魂石
Infinity Circuit|无限回路
Wraithbone|灵骨
Bonesinger|吟骨者
Aspect Warrior|支派战士
Exarch|主教（灵族道途）
Alaitoc|阿莱托克
Altansar|奥坦萨
Swordwind|剑风
Wild Riders|狂野骑士
Black Guardians|黑色守护者
Cegorach|西高奇
Great Harlequin|大丑角（神祇尊号）
Commorragh|科摩罗
Eldritch Raiders|骇人突袭者
Ynnari|死神军
Reborn|重生者（死神军自称）
Whispering God|低语之神
Amallyn Shadowguide|阿玛琳·循影
Amon Harakht|阿蒙·哈拉卡特
Eagle Pilots|雄鹰飞行员
Phoenix Lord|凤凰领主
Asuryan|阿苏焉
Drastanta|德拉斯坦塔
Eiladar Ys|艾拉达尔·伊斯
Lugganath|拉格奈什
Black Council|黑色议会
Ffaid Karhedra|法伊德·卡尔海德拉
Eyslk-Tan|艾斯利可坦
Illic Nightspear|伊利克·夜矛
Iqbraesil|伊克布雷西尔
Irillyth|伊瑞利斯
Shadow Spectres|影灵
Iyanna Arienal|伊扬娜·阿里埃纳尔
Karandras|卡兰德拉斯
Kelmon|科洛蒙
Morcan Fiorinintal|莫坎·菲奥里宁塔尔
Nuadhu|努阿杜
Yriel|伊瑞尔
Isarion Stormsmourn|伊萨里昂·风暴哀悼
Ephraeleon|埃弗拉龙
Laryin Sil Cadaiyth|拉里因·西尔·卡戴伊思
Worldsinger|世界歌者
Lileathanir|利莱萨瑟尼尔
El’uriaq|埃尔·乌里亚克
Wei-yannil|魏亚尼尔
Halathel|哈拉瑟尔
Ailill Nuada|艾利尔·努阿达
Conclave of Tears|泪之密会
Kyganil|基加尼尔
Ephrael Stern|埃弗雷尔·斯特恩
Lathrangil|兰吉尔
Lhaerial Rey|勒亚尔·雷伊
Masque of the Ceaseless Song|不休之歌剧团
Motley|莫特利
Sylandri Veilwalker|西兰德里·帷幕行者
Masque of the Veiled Path|朦胧之路剧团
Asdrubael Vect|阿斯鲁拜尔·维克特
Kabal of the Black Heart|黑心阴谋团
Lady Malys|玛勒丝女士
Kabal of the Poisoned Tongue|毒舌阴谋团
Baron Sathonyx|萨索尼克斯男爵
Kheradruakh|坎杜拉克
Wych Cult of Strife|纷争巫灵教团
Duke Sliscus|斯里斯克斯公爵
Sky Serpents|天空之蛇
Urien Rakarth|乌瑞恩·拉卡斯
Vraesque|弗雷斯克
Kabal of the Flayed Skull|剥皮颅骨阴谋团
Shaa-Dom|沙多姆
Amharoc|阿姆哈洛克
Conanmaol|科南莫尔
Executioners|处刑者（灵族海盗团）
Count Erandael|埃兰代尔伯爵
Sunblitz Brotherhood|日闪兄弟会
Duke Siriolas|西里奥拉斯公爵
Ebahn Lauma|伊班·劳玛
Baelstorm Avengers|巴力风暴复仇者
Ferianwyr Greensteel|费里安维尔·绿钢
Greensteel Warriors|绿钢勇士
Galadhar the Grey|灰袍加拉达
Duro|杜罗
Kaelis Carnelia|凯利斯·卡内利娅
Steeleye Reavers|钢眼掠夺者
Lady Hale’drithea|海尔德利西亚女士
Black Suns|黑日
Lord Phaendris|芬德里斯领主
Saaraina|萨拉伊娜
Void Dragons|虚空之龙
Illiyanne Natasé|伊利亚恩·纳塔塞
Abriel Hum|阿布里埃尔·休姆'''
for line in pairs.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0571','对照本篇英文专名；人物尊号、海盗组织与普通同形词按语境使用。'])))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
p=P/'edits.json';e=json.loads(p.read_text());e['A0571-B0091']=e['A0571-B0091'].replace('黑暗灵族与其他同族的不同之处，在于其主要家园不在现实宇宙的行星上，而是','按本篇描述，黑暗灵族与其他同族的不同之处，在于不占据现实宇宙中的行星，而是栖居于');e['A0571-B0156']='拉里因·西尔·卡戴伊思——利莱萨瑟尼尔的世界歌者，埃尔·乌里亚克的灾星';e['A0571-B0158']='魏亚尼尔——来自哈拉瑟尔';e['A0571-B0191']='埃尔·乌里亚克——沙多姆暴君';p.write_text(json.dumps(e,ensure_ascii=False,indent=2))
p=P/'notes.json';n=json.loads(p.read_text());n['A0571-B0091']='不占据现实行星是所给英文的概括叙述，保留其说法并加来源限定，不据此判断所有时代前哨及劫掠据点归属。';p.write_text(json.dumps(n,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{571};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':571,'read_through_block':244,'complete':True},ensure_ascii=False,indent=2))
print('571 complete')
