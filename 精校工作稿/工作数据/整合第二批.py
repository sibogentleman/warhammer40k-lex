from pathlib import Path
import json,csv,re,io
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'工作数据'
corpus=json.loads((D/'全书分段底稿.json').read_text());blocks={b['id']:b for a in corpus for b in a['blocks']};edits={}
for f in sorted(D.glob('人工精校译文*.json')):edits.update(json.loads(f.read_text()))
extra={}
# These paragraph IDs were inspected individually against the English.
nav_ids=['A0001-B0046','A0004-B0006','A0005-B0009','A0006-B0023','A0009-B0099','A0010-B0047','A0010-B0049','A0018-B0100','A0018-B0138','A0018-B0395','A0023-B0060','A0024-B0046','A0024-B0048']
for bid in nav_ids:extra[bid]=edits.get(bid,blocks[bid]['text']).replace('导航者','导航员')
extra['A0010-B0021']='Battle Congregations 战斗集群'
extra['A0018-B0401']=edits['A0018-B0401'].replace('由 001 排至以 000 表示的第一千年','由 001 排至表示该千年最后一年的 000')
extra['A0018-B0108']='医疗部——负责公共卫生事务。'
extra['A0018-B0182']='修女会——完全由女性组成的组织，其中包括战斗修女。'
extra['A0024-B0090']=edits['A0024-B0090'].replace('埃弗森','艾弗森')
extra['A0023-B0062']=edits['A0023-B0062'].replace('灵族，尤其希望密切观察星辰之子事业的丑角，是其中一类。','灵族就是其中一类，尤其是希望密切关注星辰之子事业的丑角。')
extra['A0024-B0072']=edits['A0024-B0072'].replace('作者打趣说，这门手艺无疑是为了填饱自己的肚子而学会的','这门手艺无疑是为了填饱自己的肚子而学会的')
(D/'人工精校译文-15.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2));edits.update(extra)
core=list(csv.DictReader((D/'核心术语定译.tsv').open(),delimiter='\t'));lookup={r['英文标准词'].casefold():r for r in core};fields=list(core[0])
def term(en,zh,loc,note='',status='暂定·官方待核',ref='所给英文底稿',override=False):
 key=en.casefold()
 if key in lookup and not override:
  if lookup[key]['采用中文']!=zh:print('EXISTING',en,lookup[key]['采用中文'],'requested',zh)
  return
 row={'英文标准词':en,'采用中文':zh,'译名状态':status,'依据':ref,'定位':loc,'编辑说明':note}
 if key in lookup:lookup[key].update(row)
 else:core.append(row);lookup[key]=row
for en,zh,p,enp in [('Navigator','导航员',24,24),('Inquisitor','审判官',24,24),('Eversor Assassin','艾弗森刺客',24,24),('Magnus the Red','红魔马格努斯',36,35),('Ghazghkull Thraka','碎骨者·斯拉卡',30,29)]:
 term(en,zh,f'GW-09 中文 PDF 第 {p} 页；GW-10 英文 PDF 第 {enp} 页','依据同名单位对应核对；叙述中的同一人物或身份采用该译名。','官方已核对','GW-09',True)
term('Navigators','导航员','GW-09 中文第 24 页；GW-10 英文第 24 页 Navigator','Navigator 的规则复数；原译导航者保留供对照。','官方已核对','GW-09')
term('Navis Nobilite','导航员家族','A0010-B0049；A0018-B0100','机构名仍属暂定；成员称谓随已核官方 Navigator 统一。',override=True)
term('Battle Congregations','战斗集群','A0018-B0213；A0010-B0021','此处指机械修会多种武装合编的战场编队，修正原译战斗修会。',override=True)
term('Ghazghkull Mag Uruk Thraka','碎骨者·斯拉卡','A0018-B0055；GW-09 第 30 页；GW-10 第 29 页','同一人物的完整英文名；采用已核官方短名 Ghazghkull Thraka 的中文，不自造中间名。','暂定·官方短名对应','GW-09')
term('Ripper Gun','撕裂枪','GW-04 中文第 53—54 页；GW-11 英文第 53—54 页','欧格林装备；中英文同一单位卡对应。','官方已核对','GW-04')
term("Bone'ead",'聪明头','GW-04 中文第 54 页；GW-11 英文第 54 页','中文 Ogryn Bone’ead 为欧格林聪明头；简称取对应称号。','官方已核对','GW-04')
term('Eversor','艾弗森','A0024-B0089；GW-09 中文第 24 页；GW-10 英文第 24 页','Eversor Assassin 的简称；官译完整单位名为艾弗森刺客。','暂定·官方短名对应','GW-09')
# Curated names appearing in the newly reviewed passages.
data='''Era Indomitus|不屈时代|18
Imperial Regent|帝国摄政|18
Imperial Cult|帝皇信仰|18
Imperial Creed|帝国教义|24
Legiones Skitarii|护教军团|18
Planetary Defense Forces|行星防卫军|18
Enforcers|地方执法者|18
Nova Terra Interregnum|新泰拉空位期|18
Noisome Reek|恶臭瑞克|18
Ulumeathic League|乌卢梅亚蒂克联盟|18
Dark Imperium|黑暗帝国|18
Imperium Nihilus|帝国暗面|18
Imperium Sanctus|帝国圣疆|18
Indomitus Crusade|不屈远征|18
War of Beasts|野兽之战|18
Nachmund Rift War|纳克蒙德裂隙战争|18
Nachmund Gauntlet|纳克蒙德走廊|18
Devastation of Baal|巴尔之毁|18
Red Scar|红疤地区|18
Plague Wars|瘟疫战争|18
Nephilim Sector|拿非利星区|18
Pariah Nexus|驱灵死域|18
Prosperan Rift|普罗斯佩罗裂隙|18
Fifth Sphere of Expansion|第五次扩张|18
Nem'yar Atoll|奈姆亚尔环礁|18
Chalnath Expanse|查尔纳斯广域|18
Octarius|奥克塔琉斯|18
Kryptman|克瑞普特曼|18
Hive Fleet Leviathan|利维坦虫巢舰队|18
Nashir Sahansun|纳夏·沙汉森|18
Cordon Impenetra|绝对封锁线|18
Fourth Tyrannic War|第四次泰伦战争|18
Prestigus V|普雷斯蒂格斯五号|18
Malefactis|马勒弗里蒂斯|18
Sorrowfall|悲伤降临|18
Nova Purgatoria|炼狱新星|18
Inferni Gates|炼狱之门|18
Lord Commander of the Imperium|帝国最高统帅|18
Ordo Tempestus|暴风修会|18
Estate Imperium|帝国档案部|18
Merchant Fleet|商船队|18
Departmento Exacta|记校部|18
Officio Medicae|医疗部|18
Departmento Colonia|殖民部|18
Departmento Contagio|传染部|18
Departmento of Final Consideration|终虑部|18
Departmento Processium|流程部|18
Departmento Gradio|分级部|18
Officio Agricultae|农业部|18
Adeptus Fidicius|财政部|18
Officio Logisticarum|后勤部|18
Logis Strategos|情报部|18
League of Black Ships|黑船联盟|18
Lex Imperialis|帝国律法|18
Logos Historica Verita|历史真理部|18
Officio Communicatus|通信部|18
Officio Propagandum|宣传部|18
Ordo Hereticus|异端审判庭|18
Ordo Xenos|异形审判庭|18
Ordo Minoris|次级审判庭|18
Explorator Fleets|探索者舰队|18
Prefecture Magisterium|辖区裁判所|18
Sect Missionarius Mechanicus|机械传教士教派|18
Collegiate Extremis|绝境学院|18
Adnector Concillium|统合议会|18
Golden Throne|黄金王座|18
Holy Synod|最高圣会|18
Creed Temporal|世俗教务部|18
Missionarius Galaxia|银河传教团|18
Aeronautica Imperialis|帝国海航|18
Electro-Priesthood|流电祭司团|18
Ordo Reductor|源还修会|18
Auxilia Myrmidon|辅军精锐|18
Centurio Ordinatus|百机队|18
Knight Household Guard|骑士家族卫队|18
Inquisitorial Stormtroopers|审判庭风暴兵|18
Inquisitorial Black Ships|审判庭黑船|18
Inquisitorial Cruisers|审判庭巡洋舰|18
Arbitrators|仲裁官|18
Praeses Mercatura|贸易守护者|18
Literati|文士|18
Black Sentinels|黑色哨兵|18
Astynomia|律法督查|18
Frateris Militia|教会民兵|18
Legiones Astartes|阿斯塔特军团|18
Solar Auxilia|太阳辅助军|18
Imperialis Militia|帝国民兵|18
Imperialis Armada|帝国舰队|18
Taghmata Omnissiah|机神禁卫军|18
Order Elucidatum|澄清修会|18
Thunder Warriors|雷霆战士|18
Unification Wars|统一战争|18
Segmentum Solar|太阳星域|18
Segmentum Pacificus|太平星域|18
Segmentum Obscurus|朦胧星域|18
Segmentum Tempestus|暴风星域|18
Ultima Segmentum|极限星域|18
Segmentum|星域|18
Sector|星区|18
Subsector|次星区|18
Halo Zone|光环区|18
Halo Stars|光环群星|18
Ghoul Stars|食尸鬼群星|18
Veiled Region|帷幕地区|18
Mandragora Stars|曼德拉戈拉群星|18
Eastern Fringe|东部边缘|18
Low Gothic|低哥特语|18
High Gothic|高哥特语|18
Lingua-technis|技术之语|18
Treaty of Olympus|奥林匹斯条约|18
Machine God|万机神|18
Omnissiah|欧姆尼赛亚|18
Age of Terra|泰拉时代|19
Age of the Imperium|帝国时代|19
War in Heaven|天堂之战|19
Gue'vesa|古维萨|19
Damocles Crusade|达摩克利斯远征|19
Adrantis Five|阿德兰提斯五号|19
Prophets of Fury|狂怒先知|19
Krull|克鲁尔|19
Severan Dominate|赛维安帝国|19
Kingdom of Vanir|瓦尼尔王国|19
Men of Gold|金人|20
Men of Stone|石人|21
Perpetual|永生者|22
Fulgurite|雷击石|22
Dalia Cythera|达莉亚·库忒拉|22
Void Dragon|虚空龙|22
Cabal|密教|22
John Grammaticus|约翰·格拉马迪库斯|22
Ollanius Persson|欧兰尼奥斯·佩松|22
Oll Persson|欧尔·佩松|22
Erda|尔达|22
Homo Superior|超人类|22
Malcador the Sigillite|掌印者马卡多|22
Amar Astarte|阿玛尔·阿斯塔特|22
Mordrac|莫德拉克|22
Damon Prytanis|达蒙·普莱塔尼斯|22
Semyon|谢苗|22
Alivia Sureka|阿利维亚·苏雷卡|22
Anval Thawn|安瓦尔·索恩|22
Cyrene Valantion|昔兰尼·瓦兰蒂恩|22
Vulkan|沃坎|22
Sensei|导师|23
Star Child|星辰之子|23
Realm of Chaos: Slaves to Darkness|混沌领域：黑暗之奴|23
Realm of Chaos|混沌领域|23
Slaves to Darkness|黑暗之奴|23
Illuminati|光照会|23
Grey Sensei|灰导师|23
Mark of the Star Child|星辰之子印记|23
Protector|守护者|23
Daemon Slayer|屠魔者|23
Sword Master|剑术大师|23
Marksman|神射手|23
Endurance|坚韧|23
Athletic|矫健|23
Rescuer|救援者|23
Never Kills|不杀生|23
Heroic Name|英雄之名|23
Redeemer|救赎者|23
Redeemed|被救赎者|23
Apotheosis|神化|23
Sensei Master|导师大师|23
Adventurer Bands|冒险团|23
Ronin|浪人|23
Levilnor IV|莱维诺四号|23
Temple of the Star Child|星辰之子圣堂|23
Star Cult|星辰教派|23
Fortez|福尔特兹|23
Inquisition War|审判庭战争|23
Dark Master|黑暗之主|23
Eternity Project|永恒计划|23
Thrandos|斯冉多斯|23
Great Sorcerer|大巫师|23
Salamanders|火蜥蜴|23
Jaq Draco|贾克·德拉科|23
Brotherhood|兄弟会|23
Long Watch|万古守望|23
Sensei Knights|导师骑士|23
New Man|新人类|23
Sensei-Emperor|导师—帝皇|23
Zephro Carnelian|泽夫罗·红玉|23
Ordo Hydra|九头蛇修会|23
Wandering Inquisitor|流浪审判官|23
Captain Eternal|永恒队长|23
Lucifer Princip|路西法·普林西普|23
Psyk-out Weaponry|反灵武器|23
Ian Watson|伊恩·沃森|23
Afriel Strain|阿弗里尔变体|24
Amphi|两栖人|24
Lampra|兰普拉|24
Avenians|阿维尼亚人|24
Ark Reach Secundus|方舟河段二号|24
Old Night|旧夜|24
Beastmen|野兽人|24
packmasters|兽群首领|24
Drepanes|镰人|24
Azetium IV|阿泽提姆四号|24
Felinids|菲林人|24
Carlos McConnell|卡洛斯·麦康奈尔|24
Gland Warriors|腺体战士|24
Dantris III|丹特里斯三号|24
Genetor|基因士|24
Katara|卡塔拉人|24
Lazul|拉祖人|24
Garganus Prime|加尔加诺主星|24
Longshanks|长腿人|24
Neandors|尼安德人|24
Hyannoth IV|海恩诺四号|24
Nightsiders|夜人|24
Biochemical Ogryn Neural Enhancement|欧格林生化神经增强|24
Grey Ogryns|灰欧格林|24
Feral Ogryns|蛮野欧格林|24
Warriors of Tohruk|托鲁克战士|24
Konrad Curze|康拉德·科兹|24
Thramas Crusade|萨拉玛斯远征|24
Pelagers|海栖人|24
Scalies|鳞人|24
Squats|矮人|24
Stiltlimbs|长肢人|24
Subs|劣人|24
Thrix|羽人|24
Thugrock Goliaths|暴岩歌利亚|24
Thugrock Secundus|暴岩次星|24
Troth|特洛斯人|24
Verdant|青翠世界|24
Deeper|深人|24
Saathlaa|萨斯拉|24
Phaedra|菲德拉|24
Siskans|西斯克人|24
Slave Levies|奴隶征召兵|24'''
for line in data.splitlines():
 en,zh,n=line.split('|');term(en,zh,f'篇 {int(n):04d}')
# Individually checked planet lists, in English order; reuse existing names when present.
for n in range(295,334,2):
 eb=blocks[f'A0018-B{n:04d}'];zb=edits[f'A0018-B{n+1:04d}']
 if 'Notable examples include ' not in eb['text']:continue
 en=eb['text'].split('Notable examples include ',1)[1]
 ens=re.split(r', (?:and )?| and ',en)
 zhs=re.split('、|与',zb.split('包括',1)[1].rstrip('。')) if '包括' in zb else [zb.split('有',1)[1].rstrip('。')]
 assert len(ens)==len(zhs),(n,ens,zhs)
 for en,zh in zip(ens,zhs):term(en,re.sub('（[^）]+）','',zh),eb['id'],'行星名；同一名称在本批各清单中保持一致。')
# Context-specific notes avoid merging distinct entities or claiming official certainty.
for en,note in {
 'Imperial Cult':'指宗教信仰，与负责管理的 Ecclesiarchy（国教会）区分。',
 'Imperial Creed':'指帝国的信仰教义；宗教名称 Imperial Cult 采用帝皇信仰，机构 Ecclesiarchy 采用国教会。',
 'Lex Imperialis':'本篇的英文拼写；前文 Lex Imperia 也指帝国律法，英文原样保留。',
 'Taghmata Omnissiah':'沿用工作译名；此处是机械教军队的组织形式，不能与 Adeptus Custodes 混淆。',
 'Imperialis Armada':'帝国早期海军组织，依本段英文与后来的 Imperial Navy 区分。',
 'Cabal':'永生者条目中的组织，与黑暗灵族 Kabal（阴谋团）不是同一专名。',
 'Sensei':'帝皇后裔的旧版设定名称，与 Perpetual（永生者）及 Tutors（导师组织）分别登记。',
 'Brotherhood':'本词在第 23 篇指光照会招揽导师的兄弟会；不是第 14 篇奥瑞提安技术联盟的 The Brotherhood。',
 'The Lost and the Damned':'同一英文既可指混沌群体，也可指第 23 篇旧版资料书，中文相同但实体不同。',
 'Ronin':'第 23 篇出现的称谓，所述设定出处尚待独立核验；不要与 Rogue Trader（行商浪人）混为一谈。',
 'Felinids':'正文采用菲林人，猫人为帮助识别的别称；拉丁分类名原样保留。',
 'Goliath':'第 24 篇为涅克罗蒙达歌利亚家族成员，与 Thugrock Goliaths（暴岩歌利亚）区分。',
 'Oll Persson':'Ollanius Persson 的简称，同一人物；中文简称跟随英文用法。',
 'UR-025':'保留字母数字名称；“最后幸存的铁人之一”为说明，不属于译名。'
}.items():
 if en.casefold() in lookup:lookup[en.casefold()]['编辑说明']=note
if 'ur-025 -' in lookup:
 row=lookup.pop('ur-025 -');row.update({'英文标准词':'UR-025','采用中文':'UR-025','编辑说明':'保留字母数字名称；最后幸存的铁人之一为说明，不属于译名。'});lookup['ur-025']=row
# Known proper names and astronomical objects do not become official GW translations merely by being familiar.
with (D/'核心术语定译.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(core)
notes=json.loads((D/'编辑疑点与说明.json').read_text())
notes.update({
'A0001-B0046':'Navigator 采用 GW-09 中文第 24 页与 GW-10 英文第 24 页对应的官方译名“导航员”；本批同时回查已精校篇目的相同称谓。',
'A0010-B0021':'Battle Congregations 依据第 18 篇的编队说明统一暂译“战斗集群”，与组织或宗教意义的修会区分。',
'A0018-B0016':'本篇“现任”“目前”“近来”等时间词均对应原条目记述时点；本次校订不据此断言 2026 年最新出版设定。',
'A0018-B0026':'原文对帝国世界数量列举了从百万到十亿级的不同说法。中文保留其估计范围，不将其当作已核实的统一数字。',
'A0018-B0041':'Noisome Reek 暂译“恶臭瑞克”；原译中的“世界编织者”没有对应英文，不纳入定译。',
'A0018-B0056':'采用已核官方 Ghazghkull Thraka 的中文短名“碎骨者·斯拉卡”；英文完整名 Ghazghkull Mag Uruk Thraka 仍在原文保留。',
'A0018-B0082':'本段称主要机构向帝国参议院负责，后文又称审判庭只向帝皇及自身负责。现有英文对正式组织结构与实际独立权限表述不同，译文分别保留，不擅自合并为单一隶属关系。',
'A0018-B0096':'英文 most subvert 语法异常，结合刺客庭语境暂按“最隐秘的”理解，英文原文保留待核。',
'A0018-B0130':'length of Warp Jumps 结合第 6 篇同一部门估算旅程时间的语境，译为“亚空间跳跃所需的时间”。',
'A0018-B0196':'unaugmented 指未接受强化改造，原译“未经审计”误解词义。',
'A0018-B0262':'Taghmata Omnissiah 沿用暂定译名“机神禁卫军”；按本段仅指机械教的军队组织形式，不是帝皇禁军。',
'A0018-B0291':'Imperium Nihilus 统一暂译“帝国暗面”；本篇另有 Dark Imperium，保留为“黑暗帝国”，不将不同英文写法直接替换成同一个术语。',
'A0018-B0306':'Tanith 暂译“塔尼斯”，与本篇战争世界清单中的 Tarnis（塔尔尼斯）区分；不是同名拼写替换。',
'A0018-B0320':'Piscina IV 为行星名及编号，原译“皮希纳四海”改为“皮希纳四号”。',
'A0018-B0374':'以下收入数值针对《黑暗异端》语境中的侍从职业，原文未给出统一结算周期；未补写为月薪或现实货币。',
'A0018-B0401':'三位年份码 000 指千年中的最后一年；原文日期示例 0150930/M32 及公元 31930 年照录，不据此推算书中其他事件日期。',
'A0019-B0017':'原文将“当前”放在第 41 千年，属于原条目年代视角。中文标明该时点，不擅自改写为后续年代。',
'A0019-B0036':'英文 successions 在叛乱独立语境下疑为 secessions；暂按“分离行动”译，英文保留。',
'A0021-B0004':'half-life 在本段为人工生命的“半生命状态”，不是放射性物质的半衰期。',
'A0022-B0008':'此段将达莉亚的转化归于帝皇，B0016 的人物表却写由谢苗创造。两种说法均来自所给英文，暂保留差异，待核原始资料的直接施行者与授权者关系。',
'A0022-B0013':'“人工永生者”是本段对原体计划的称法。译文忠实保留，但不能据此推断所有原体都具备后文所述的再生能力；人物与年代关系仍待回查原始出版物。',
'A0023-B0011':'英文明确写混沌力量对导师“不可见”，但后文又写导师能感知恶魔与亚空间扰动。可能存在主客体或措辞问题；中文照录此处指向并提示，不擅自反转成“混沌看不见导师”。',
'A0023-B0013':'本篇汇集不同旧版资料，《黑暗之奴》的“空白者、直接子嗣、不育”与第二卷的“灵能者、血脉后裔”相互冲突；后文“来源冲突”节进一步对照。书名为暂定工作译名。',
'A0023-B0024':'此处至“神化”条目的能力说明包含旧版游戏规则，不是当前规则建议。补回原译遗漏的失败豁免重掷效果；未为其增添每回合次数。',
'A0023-B0036':'without the implications of time 含义不够明确，暂译“不受时间因素影响”；不据此增补瞬移、时间停止或具体行动规则。',
'A0023-B0038':'undead 此处泛指亡灵类存在，不是 Necrons（太空死灵）的阵营名称。',
'A0023-B0042':'原文 slays 与随后 spare him 字面上存在冲突；结合本节“伤亡不必然代表死亡”的规则说明，译为“击倒”以保持上下文可理解。',
'A0023-B0062':'钛族叛逃者与 Ronin 的说法照所给英文保留，其原始出版出处尚待核验；不将其自动与本篇两部旧书的内容归为同一来源。',
'A0023-B0082':'本段为光照会设想的计划，不是已经发生的事件；此处 Brotherhood 与第 14 篇同译为兄弟会的另一组织分开登记。',
'A0023-B0099':'关于 Games Workshop 后续是否再使用导师的说法，只代表原条目记述时点。是否被永生者取代仍是条目所述读者推测，未作官方确认。',
'A0024-B0009':'本段将帝皇亲政年代与 Imperial Guard 并列，和第 18 篇“荷鲁斯之乱后才拆分帝国卫队”的叙述有年代称谓差异。保留源文用词，待核是否为追述性泛称。',
'A0024-B0048':'依已核官方 Navigator 统一为“导航员”；旧译“导航者”保留在原译对照中。',
'A0024-B0061':'Ripper Gun 与 Bone’ead 分别采用官译“撕裂枪”“聪明头”，见 GW-04 与 GW-11 第 53—54 页。文中的拉丁分类名称不另造中文音译。',
'A0024-B0063':'本段以“七类”列举现有欧格林类型，随后又要求进一步区分，分类层级表述不够明确。译文保留其争议性，没有自行增删分支。',
'A0024-B0090':'Eversor Assassin 依 GW-09 中文第 24 页、GW-10 英文第 24 页统一为“艾弗森刺客”；暴岩歌利亚与歌利亚家族不是同一群体。',
'A0024-B0101':'levies 在征兵语境中指被征召者，原译“奴隶税”误解词义，改为“奴隶征召兵”。'
})
(D/'编辑疑点与说明.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
(D/'语言精校篇目.json').write_text(json.dumps(list(range(1,25))))
print('core_terms',len(core),'extra_blocks',len(extra),'notes',len(notes))
