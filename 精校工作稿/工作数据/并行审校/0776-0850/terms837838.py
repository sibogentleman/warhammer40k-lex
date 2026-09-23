from pathlib import Path
p=Path(__file__).parent
core=(p.parent.parent/'核心术语定译.tsv').read_text();prior=(p/'terms.tsv').read_text()
known={l.split('\t')[0].casefold() for l in (core+'\n'+prior).splitlines()}
raws={837:'''Kyria Draxus|凯莉娅·德拉克瑟斯|姓氏依官方审判官德拉克瑟斯；全名暂定。
Draxus|德拉克瑟斯|简称取官方全衔词根。
Oruskh Dynasty|奥鲁斯赫王朝|区别本篇 Oruscar。
Oruscar Dynasty|奥鲁斯卡王朝|英文另名，与 Oruskh 不强并。
The Stilling|沉寂效应|驱灵死域导致精神萎靡与心智沉寂，不是时间停滞。
Liminal Abraisers|阈限消蚀器|据装置消蚀现实与亚空间间屏障的用途暂译；原阈限激活。
Orphaeus|俄耳甫斯|不屈远征战斗群。
Hephaestus|赫菲斯托斯|不屈远征战斗群。
Iolus|伊奥劳斯|不屈远征战斗群。
Draix|德雷克斯|同篇德莱克斯并回首处。
Suleyman Khefre|苏莱曼·凯夫雷|同篇赫夫雷并回首处。
Nektarrik|内克塔里克|索科特法皇，英文明确女性代词。
Shemvokh|舍姆沃克|同篇舍姆沃赫统一。
Vordreska|沃尔德雷斯卡|原文另拼 Vordeska，暂视同处异拼。
Urtep|厄特普|原文另拼 Uretp，暂视同处异拼。
Kaspar Marius Todoric Marran|卡斯帕·马里乌斯·托多里奇·马兰|沿本篇人名暂定。
Legio Castigatum|惩戒泰坦军团|原智控军团为错认组织；与 Legio Cybernetica 分开。
Precept Magnificat|崇高戒律号|帝国舰名暂定。
Saint Aster|圣阿斯特号|帝国舰名暂定。
Deus Redemptor|神救赎者|战将级泰坦名暂定。
dataphages|噬数据体|对数据和机魂的侵袭，不是生物噬菌体。
Vie Almus Majora|神圣大道|另有 Majoria、Vic Almnus Majora 异拼；沿原稿中文，不编定拉丁词源。
Bigelis Thao|比杰利斯·塔奥|原比杰伦斯多一伦字，按拼写修正。
Ishlarn Thermokarst|伊什拉恩热融洼地|thermokarst 为热融地貌，不是人名头衔。
Kalliphor|卡利普尔|同篇卡利弗尔统一。
Tredica|特雷迪卡|地名暂定。
Tredica Decitor|特雷迪卡·德西托尔|所属星体，与 Fortis、Ardaxis 区分。
Tredica Fortis|特雷迪卡·福蒂斯|所属星体。
Tredica Ardaxis|特雷迪卡·阿达克斯|所属星体。
Paladin’s Shadow|圣骑之影号|舰名暂定。
Mnemetic Crystals|记忆晶体|按语境暂定技术名。
Song of Oblivion|遗忘之歌号|沿原稿舰名。
Zeta IIX Hespus|泽塔 IIX 赫斯普斯|IIX 非标准罗马数字，保留原拼，不擅改八号。
Noctilith Decree|夜石法令|沿本篇概念暂定。
Psolt|普索尔特|人名暂定。
Vergoyz Alphic|韦尔戈伊兹·阿尔法克|人名暂定。
Lundkest|伦德克斯特|人名暂定。
Yoctoparticulate Crucible|幺科粒子熔炉|沿原稿暂名，技术细节未明。
Dvorel’s Necrocastigatrix|德沃雷尔的死灵惩戒者|沿原稿武器名暂定。
Cyclophox Determination|环迅决断|沿原稿暂名，词源与构造待核。
Eyes of the Void|虚空之眼|三位技术牧首的合称。
Lomorr System|洛莫尔星系|沿原稿地名。
Torantis|托兰蒂斯|沿原稿地名。
Dracos Apocalystor|天龙启示|沿原稿泰坦名，非泛称战将级。
Oradi|奥拉迪|与 Behzt 在正文为两人。
Behzt|贝赫特|女性人物，与 Oradi 分开。
Manipulus-Prime|首席操纵祭司|参考官译 Tech-Priest Manipulus 技术祭司操纵者词根，完整职衔暂定。
Ark of Oblivion|遗忘方舟|武器名，不当作运输舰。
ExMachinus|极限机械号|沿原稿舰名暂定，不声明词源意译正确。
Iash’Uddra|亚什·乌德拉|星神名，原拼撇号统一。
Endless Swarm|无尽虫群|亚什·乌德拉称号语境。
Thalcifer|塔尔西菲尔|地名暂定。
Mohrgar Fex’s Hyper-Alembic|莫尔加·费克斯的超蒸馏器|武器暂名。
Silence in Suffering|苦难沉默号|圣杯级巡洋舰。
Shen’Tai|申·泰|星系名暂定。
Skahren|斯卡伦|星系名，Breach 译裂口。
Santis-Magna|桑蒂斯·马格纳|蛮荒世界暂名。
Shivarik’s Constellation|希瓦里克星座|古代卫星武器系统名，不是变成星座的人。
Ghelf|格尔夫|统御贤者人名。
Wyrmwood|龙林星|沿原稿恶魔世界名。
Zakkis Armon|扎基斯·阿蒙|黑暗使徒人名。
Calathir|卡拉蒂尔|国教控制世界。
Forzare|弗扎雷|星系暂名。
Restitution|归还星|镀金之子母星，沿原稿。
Gilded Sons|镀金之子|战团名沿原稿。''',838:'''Isaish Khestrin|以赛亚·赫斯特林|舰队司令人名，沿原稿。
Eorloid|厄洛莱德|战团长人名沿原稿。
Edermo|埃德莫|人名沿原稿。
Odrameyer|奥德拉梅耶|帝国卫队上校，不改为星际战士。
Septicus Seven|塞普提克斯·赛文|沿原稿人物全名；与败血军团不合并。
Septicus|塞普提克斯|人物简称。
Tartella System|塔尔泰拉星系|沿原稿地名。
Spear of Espandor|埃斯潘多之矛|反击作战名，沿原稿。
Plains of Hecatone|赫卡顿平原|地名暂定。
Vengeance Campaigns|复仇战役|军事实践，不是群众运动。
Knights Cerulean|蔚蓝骑士|战团名沿原稿。
Legio Fortis|勇壮军团|泰坦军团名沿原稿。
House Konor|康诺家族|骑士家族名沿原稿。
Household (Knight battle formation)|家族战斗群|同一家族出动的战斗编组，非多个家族；规模未定。
Plague Guard|瘟疫守卫|恶魔军团，不与死亡守卫合并。
Legions of the Three-Eyed Fly|三眼之蝇军团|参战恶魔军团合称。
Poxdroners|瘟疫蜂鸣者|恶魔军团名，不套无人机。
Bouncing Tide|跃动潮汐|纳垢灵大群名。
Slimepack|黏液之群|纳垢野兽战帮名，非野兽人。
Sporewalker|孢子步行者|巨兽专名沿原稿。
Cult of Renewal|重生教派|教派名沿原稿。
Cult of Blessed Protrusion|受祝凸起教派|沿原稿教派名，词义待核。
Poxguard|毒疹守卫|军队名称沿原稿。
Dontorian Heavy Artillery|东托利亚重型火炮部队|沿原稿单位名；不径认与 Dontorian Ur-Dynasty 为同一势力。
Chem Squads|化学小队|沿原稿编组名。
Contamination Corp|污染之团|军队名称，数量为两个连。
Legio Pestis|瘟疫军团|泰坦军团名。
Infernal Devices|炼狱装置|三台战争机器，沿原稿名。
Drudgewalkers|苦工步行者|瘟疫使军团合称沿原稿。
Zzzzartap’s Circus|滋阿塔普马戏团|原之环不符 circus，修为马戏团。
Flylords|苍蝇领主|部队名，非单个人物职衔。
Winged Rotflies|带翼腐蝇|突变蝇群名。
Children of Blight|枯萎之子|部队名沿原稿。
Befoulers|污染者|本处部队名，区别 Defiler 同名单位。
Claw Corps|利爪军|编制名暂定，不推定人数。
Rot Reapers|腐烂收割者|部队名沿原稿。
Blight Guard|枯萎守卫|部队名沿原稿。
Filth Engines|污秽引擎|部队名沿原稿。
Steel Tide|钢铁潮汐|部队名沿原稿。
Ironhulks|钢铁巨躯|陆战部队名，不能由 hulk 认作废船。
Seven Blights|七重枯萎|七座枯萎之塔合称。
The Scabbed|结痂者|scab 为痂，原有疤者混同 scar。
Heltrenchers|地狱掘壕者|部队名沿原稿。
Sloughskins|蜕皮者|恶魔部队名沿原稿。
Carrion Legion|腐尸军团|恶魔部队名沿原稿。
Talliers of the Dead|记死者|恶魔部队名沿原稿。
House Drear|德瑞尔家族|骑士家族名沿原稿。
Keepers of the Cauldron|巨釜守卫|与本章 Cauldron of Nurgle 纳垢巨釜词根统一。
Infumers|焚香者|部队名沿原稿。
Slimehorn Legions|黏液犄角军团|瘟角兽军团合称沿原稿。'''}
rows=[]
for n,raw in raws.items():
 for l in raw.splitlines():
  en,zh,note=l.split('|')
  if en.casefold() in known:continue
  known.add(en.casefold());status='暂定·官方待核'
  if en in ['Draxus','Manipulus-Prime']:status='官方词根参考·全称待核' if en=='Manipulus-Prime' else '官方词根参考·简称'
  rows.append('\t'.join([en,zh,status,'所给英文底稿；已逐段核读及核心对照',f'篇{n:04}',note]))
with (p/'terms.tsv').open('a') as f:f.write('\n'.join(rows)+'\n')
print('new terms',len(rows))
