from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(k,t):e[f'A0573-B{k:04d}']=t
p(51,'黑暗灵族社会等级森严。残酷、奢靡的贵族居于科摩罗最高的尖塔；贫苦底层则蜷居最外围城区与口袋维度，生活近乎原始。两者之间，是无数亚文化群体与派系，在永不止息的暴力循环中相互掠夺。最底层则是成群的奴隶，在暗城眼中，不过是无处不在、可供剥削折磨的资源。')
p(53,'黑暗灵族最重要的派系，往往也是掌握最强武力的组织，主要包括：')
p(55,'阴谋团——规模庞大、独立行事的武装集团，许多与高科摩罗的统治贵族相连。它们由强大的执政官领导，拥有雄厚兵力，是进入现实宇宙捕掠奴隶的主力，也在科摩罗的权力网络中数量最多、势力最强。维克特的黑心阴谋团居于首位；其他重要组织包括剥皮颅骨、毒舌、黑曜玫瑰、最终仇恨、垂死之日、铁棘，以及破碎之印。')
p(57,'巫灵教团——以女性为主的角斗组织，将杀戮化作表演。竞技场上的生死搏斗散发出强烈痛苦，让观众得以从中“饱餐”。教团由血腥魔女领导，常受邀参加现实宇宙的劫掠；即使多数新入团者曾为奴隶，也能凭此积累巨大权力与影响。最显赫的是纷争教团，另有诅咒之刃、红色悲伤、七灾、拒绝之刃、无拘之怒、第十三夜，以及永恒痛苦。')
p(59,'血伶人巫会——由生物技术大师血伶人领导，成员或许是暗城最可怕、最阴险的居民。对阴谋团而言，它们不可或缺：既提供登峰造极的酷刑技艺、激进的军事技术，也实施生物强化。最重要的是，血伶人能以再生技术救回重伤的雇主。作为报酬，巫会通常从阴谋团掳来的奴隶中，收取一定份额。著名者包括血肉先知、黑暗信条、十二巫会、黑色血裔、咒厄、永恒螺旋，以及黑檀之刺。')
p(61,'雇佣组织——为任何出得起价钱的人效力，包括梦魇剑客神殿、精于用毒的蕾蜜恩交际花，以及来自异维度的可怕曼德拉。蛇人等其他种族，也会充当佣兵。')
p(63,'下层帮派——来自科摩罗低层地区，包括劫掠者、滑板暴徒与天灾。他们虽粗野凶暴，在暗城最危险、最贫困的地带，仍可掌握相当权势。')
p(65,'黑暗灵族与其他同族的关系十分复杂：他们有时劫掠方舟或蛮荒灵族，必要时也会合作。目标一致时，他们还会与灵族海盗、丑角一同袭击现实宇宙。')
p(68,'黑暗灵族借网道进入现实宇宙捕掠奴隶，作战以突袭、速度与恐惧为核心。掠袭者飞艇、破坏者飞艇、毒液飞艇等快速反重力载具，在强大空中火力支援下出击，通常只求击溃抵抗，抓获奴隶后带回科摩罗。因此，许多武器旨在致残或使敌人失去行动能力，而非立即杀死。除非预期能收获无比丰厚的痛苦，他们通常避免旷日持久的战役和消耗战。')
p(70,'尽管黑暗灵族社会充满背叛，其军队却运转精密。阴谋团、巫灵教团、血伶人巫会及各路佣兵，为奴隶与战利品的共同诱惑而结盟。只有最能干的战士才获准参与现实宇宙劫掠，因此格外危险。科摩罗内虽遍布阴谋，突袭时却因俘虏与痛苦的价值，往往展现出平日少有的合作与纪律。')
p(72,'如同科摩罗本身，黑暗灵族军队并无统一编制，而会根据每次袭击的需要组建。这正体现其谚语“K’lthrael Aht’Ynris Khlave”所说的：“为刀刃调配合适的毒药。”')
p(77,'阿赫拉——突击战蝎支派战士的前领袖，梦魇剑客阶层的创始者')
p(85,'达扎尔，“剑刃大师”——梦魇剑客冠军；有人认为他就是阿赫拉')
p(87,'莉莉丝·海斯佩拉克斯——纷争巫灵教团领袖')
p(89,'萨索尼克斯男爵——滑板暴徒领主')
p(91,'塔里尔——黑心阴谋团执政官，在考拉瓦战役期间率领黑暗灵族。他对乌斯维的大先知怀有敌意。')
p(93,'特拉维利亚斯·斯里斯克斯“公爵”——天空之蛇指挥官')
p(99,'埃尔·乌里亚克——沙多姆暴君')
p(102,'黑暗灵族概念的早期源头，是 Games Workshop 于1987年推出的限量“黑暗精灵太空战士”模型，时间略早于《战锤40,000：行商浪人》发行。第一版中已多次提到凶残的灵族海盗，但直到1998年的第三版《圣典：黑暗灵族》，这一阵营才获得完整的背景与军队设定。最初的背景和模型仍相对有限，因此2002年又推出了修订后的第三版圣典。')
p(104,'The original 1987 "Dark Elf Space Trooper" 1987年最初的“黑暗精灵太空战士”模型')
n.update({'A0573-B0053':'Dark Eldar为黑暗灵族，不是战锤幻想黑暗精灵。','A0573-B0057':'Succubi采用血腥魔女，Wych Cult统一巫灵教团；观众饱餐为吸收痛苦的设定，非普通饮食。','A0573-B0059':'英文not...just句法残缺，按所列三类服务还原并列关系。The Hex为咒厄，原六头无依据；Black Descent暂作黑色血裔，与普通颜色下降区分。tithe原文未指定精确比例，不擅自写成恰好十分之一。','A0573-B0063':'Reavers劫掠者与Raider掠袭者飞艇、Ravager破坏者飞艇分别定译，避免原文中掠夺者混用。','A0573-B0068':'grav-vehicles修复原“反重力再聚”错字；三个载具完整名称依GW09/GW10第20页核对。','A0573-B0070':'treacherous为背信弃义，不是笼统危险；coalition为共同逐利而结盟，不是彼此争夺潜力。','A0573-B0077':'创立者阿赫拉及达扎尔身份关系保留原文断言与推测各自强度，不把有人认为写成定论。','A0573-B0093':'斯里斯克斯与571统一，同一人物较长全名保留；天空之蛇与天蛇原译统一。','A0573-B0102':'lore在此为背景设定，不是民间传说；早期模型名Elf按黑暗精灵保留，区别后来阵营Dark Eldar黑暗灵族。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
pairs='''Kysaduras|凯萨杜拉斯
Port Demesnus|德梅斯努斯港
Crone Swords|老妪之剑
Seventh Path|第七道途
Eladrith Ynneas|艾拉德斯·伊涅阿斯
Pleasure Cults|欢愉教派
Age of Dark Genesis|黑暗起源时代
Age of Pain|痛苦时代
Age of Plenty|丰饶时代
Age of the Living Muse|活体缪斯时代
Dark Muse|黑暗缪斯
Khaine’s Gate|凯恩之门
Evolus Massacre|埃沃勒斯大屠杀
The Thirst|饥渴（黑暗灵族灵魂饥渴）
Kabal|阴谋团
High Commorragh|高科摩罗
Obsidian Rose|黑曜玫瑰
Last Hatred|最终仇恨
Dying Sun|垂死之日
Iron Thorn|铁棘
Broken Sigil|破碎之印
Wych Cults|巫灵教团
Cult of Strife|纷争教团
Cursed Blade|诅咒之刃（巫灵教团）
Red Grief|红色悲伤
Seventh Woe|七灾
Blade Denied|拒绝之刃
Wrath Unbound|无拘之怒
Thirteenth Night|第十三夜
Pain Eternal|永恒痛苦
Haemonculi Covens|血伶人巫会
Prophets of Flesh|血肉先知
Dark Creed|黑暗信条
Coven of Twelve|十二巫会
Black Descent|黑色血裔
The Hex|咒厄
The Everspiral|永恒螺旋
The Ebon Sting|黑檀之刺
Incubi Shrines|梦魇剑客神殿
Lhamaean|蕾蜜恩
Sslyth|蛇人
Arhra|阿赫拉
Aurelia Malys|奥瑞利亚·玛勒丝
Tahril|塔里尔
Kaurava|考拉瓦
Traevelliath Sliscus|特拉维利亚斯·斯里斯克斯'''
for line in pairs.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0572—0573','本篇语境或已有译名；同名组织、职衔与通称分列。'])))
u9='https://assets.warhammer-community.com/chi_06-05_wh40k_core%26key_munitorum_field_manual-5mrlucr2t1-fkybzzzoce.pdf';u10='https://assets.warhammer-community.com/eng_warhammer40000_munitorum_field_manual_march_2025-cims9ya3sg-s8j9m2haae.pdf'
for en,zh in [('Archon','执政官'),('Haemonculus','血伶人'),('Mandrakes','曼德拉'),('Reavers','劫掠者'),('Raider','掠袭者飞艇'),('Ravager','破坏者飞艇'),('Venom','毒液飞艇'),('Wyches','巫灵'),('Kabalite Warriors','阴谋团战士')]:by[en.casefold()]=dict(zip(cols,[en,zh,'官方已核对',f'GW-09 {u9}；GW-10 {u10}','两版PDF均第20页','逐项核对对应单位；其他阵营同形英文不可机械套用。']))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{573};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':573,'read_through_block':104,'complete':True},ensure_ascii=False,indent=2))
print('573 complete')
