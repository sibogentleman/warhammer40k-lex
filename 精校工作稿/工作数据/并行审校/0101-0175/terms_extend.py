import csv,json,re
from save import P,SOURCE
fields=['英文标准词','采用中文','译名状态','依据','定位','编辑说明']
rows={r['英文标准词']:r for r in csv.DictReader((P/'terms.tsv').open(),delimiter='\t')}
baseurl='https://assets.warhammer-community.com/'
zurl=baseurl+'chi_06-05_wh40k_core%26key_munitorum_field_manual-5mrlucr2t1-fkybzzzoce.pdf'
eurl=baseurl+'eng_warhammer40000_munitorum_field_manual_march_2025-cims9ya3sg-s8j9m2haae.pdf'
# All page pairs below were read in full where the named units occur.
official={
3:'''Aleya|阿莱亚
Allarus Custodians|阿拉鲁斯亲卫
Anathema Psykana Rhino|巫咒犀牛装甲车
Blade Champion|利刃勇士
Custodian Guard|禁军卫队
Custodian Wardens|禁军守卫
Knight-Centura|百骑长
Prosecutors|审判修女
Shield-Captain|盾卫连长
Shield-Captain in Allarus Terminator Armour|阿拉鲁斯终结者护甲盾卫连长
Shield-Captain on Dawneagle Jetbike|晨鹰喷气摩托盾卫连长
Trajann Valoris|图拉真·瓦洛瑞斯
Valerian|瓦里瑞安
Venerable Contemptor Dreadnought|神圣蔑视者无畏机甲
Venerable Land Raider|神圣兰德掠袭者坦克
Vertus Praetors|骁骑禁军
Vigilators|警戒修女
Witchseekers|寻巫修女
Agamatus Custodians|阿伽玛图斯禁军
Aquilon Custodians|天鹰卫士
Ares Gunship|阿瑞斯炮艇机
Caladius Grav-tank|神鸟反重力坦克
Contemptor-Achillus Dreadnought|阿喀琉斯型蔑视者无畏机甲
Contemptor-Galatus Dreadnought|角斗士型蔑视者无畏机甲
Coronus Grav-carrier|克洛诺斯反重力运兵车
Custodian Guard with Adrasite and Pyrithite Spears|装备遗迹长矛或炙烈长矛的禁军卫队
Orion Assault Dropship|猎户座突击运输机
Pallas Grav-attack|帕拉斯反重力战车
Sagittarum Custodians|禁军射手
Telemon Heavy Dreadnought|特拉蒙重型无畏机甲
Venatari Custodians|翔猎禁军
Oblivion Knight|湮灭骑士
Null Maiden Vigil|虚无之女警戒团
Shield Host|盾卫军团
Veteran of the Kataphraktoi|铁骑结社的老兵''',
4:'''Belisarius Cawl|贝利萨留斯·考尔
Corpuscarii Electro-Priests|科普斯卡驭电祭司
Fulgurite Electro-Priests|电岩驭电祭司
Cybernetica Datasmith|智控数据技师
Tech-Priest Dominus|技术祭司主宰者
Tech-Priest Enginseer|技术祭司机械教士
Tech-Priest Manipulus|技术祭司操纵者
Technoarcheologist|科技考古学家
Kastelan Robots|卡斯特兰机器人
Kataphron Breachers|铁甲攻坚者
Kataphron Destroyers|铁甲破坏者
Onager Dunecrawler|沙丘爬行者
Pteraxii Skystalkers|佩莱克斯天空追猎者
Pteraxii Sterylizors|佩莱克斯净化者
Serberys Raiders|塞波利斯掠夺者
Serberys Sulphurhounds|塞波利斯硫磺猎手
Sicarian Infiltrators|斯卡里亚渗透者
Sicarian Ruststalkers|斯卡里亚锈蚀追猎者
Skitarii Marshal|护教军元帅
Skitarii Rangers|护教军游骑兵
Skitarii Vanguard|护教军先锋
Skorpius Disintegrator|天蝎粉碎者
Skorpius Dunerider|天蝎沙行船
Sydonian Skatros|西多尼亚斯卡特罗射手
Ironstrider Ballistarii|巴利斯塔铁骑兵''',
24:'''Exaction Squad|强征小队
Subductor Squad|冲覆者小队
Vigilant Squad|警戒者小队
Culexus Assassin|丘里克斯刺客''',
26:'''Armiger Helverin|护卫侍从
Armiger Warglaive|战刃侍从
Canis Rex|狼王号
Knight Castellan|堡主骑士
Knight Crusader|远征骑士
Knight Errant|游侠骑士
Knight Gallant|勇武骑士
Knight Paladin|圣堂骑士
Knight Preceptor|教导骑士
Knight Valiant|英勇骑士
Knight Warden|守望骑士
Acastus Knight Asterius|牛头怪型阿卡斯托斯骑士
Acastus Knight Porphyrion|巨人王型阿卡斯托斯骑士
Armiger Moirax|天命型侍从
Cerastus Knight Acheron|黄泉型角蝰骑士
Cerastus Knight Atrapos|命运女神型角蝰骑士
Cerastus Knight Castigator|惩戒者型角蝰骑士
Cerastus Knight Lancer|枪骑兵型角蝰骑士
Questoris Knight Magaera|复仇女神型巡游骑士
Questoris Knight Styrix|冥河型巡游骑士'''}
for page,lines in official.items():
 for line in lines.splitlines():
  en,zh=line.split('|');note='官方中英手册同名单位逐项对应，不依点数或条目位置硬配。'
  if en in ['Oblivion Knight','Veteran of the Kataphraktoi']:note='官方强化名称；采用该同名职衔或衍生阶层时须注明证据层级。'
  if en in ['Null Maiden Vigil','Shield Host']:note='官方分遣队名称；泛用组织编制的译法参考此项，不混淆全称与构词。'
  rows[en]=dict(zip(fields,[en,zh,'官方已核对','GW-09 '+zurl+'；GW-10 '+eurl,f'GW-09 简中 PDF 第{page}页；GW-10 英文 PDF 第{page}页',note]))
# Contextual names: no claim of independent official certification.
provisional='''Lectitio Divinitatus|神性论|书名《神性论》；同名信仰称神性论信仰，按主审已定全书译名。
Fabricator-General|铸造将军|主审与另一校对线最终统一；为机械修会专门职衔，不视作普通军队将军军衔。
Fabricator Locum|铸造代理|铸造将军副手。
Archmagos Dominus|统御大贤者|与 Tech-Priest Dominus 完整官方兵种名区分；Dominus 不译神圣。
Archmagos Domina|统御大贤者|同上，Domina 为阴性形式。
Magos Dominus|统御贤者|军事指挥职衔，完整兵种 Tech-Priest Dominus 另用官译。
Magos Autokratoris|独裁贤者|负责泰坦维护，避免与统御贤者混同。
Magos Juris|律法贤者|防范技术异端的职衔。
Electro-priest|驭电祭司|从两个官方完整兵种名抽取泛称；非独立核实。
Electro-Priesthood|驭电祭司团|从官方单位用词统一组织名，替代此前流电祭司团。
Genetor|基因士|核心沿用；GW09/10第4页同形强化译基因师，不足以强制覆盖历史职业。
Logis|逻辑士|历史职业与组织；同形官方强化名预言师暂不直接覆盖。
Artisan|铸造士|历史职业与组织；官方强化名工匠师与具体语境有别。
Enginseer|工造士|单独历史职业暂沿用；完整 Tech-Priest Enginseer 用官译技术祭司机械教士。
Trifactor|三联技师|155篇漏译补出，暂定。
Xenarites|异技派|研究异形技术的机械教派别；原异务派统一。
Khamrians|卡姆里派|原书英文派名音译。
Tenninites|特尼派|原书英文派名音译。
Logicians|逻辑派|与职业 Logis 区分。
Imperio-Cognisticians|帝国认知派|机械教异端派别。
Levelists|平等派|机械教异端派别。
Tech Adept|技术专家|火星祭司体系专家等级，非泛指任何熟练者。
Acolytum|技术侍僧|单数；Acolyta复数，中文统一。
Oud Oudia Raskian|乌德·乌迪亚·拉斯基安|人名统一124、154；其任期按各篇叙述保留。
Zagreus Kane|扎格列欧斯·凯恩|人名统一124、154。
Gastaph Hediatrix|加斯塔夫·赫德特里克斯|人名统一119、154。
Xasandera Valdet|克桑德拉·瓦尔德特|154篇内部统一；现任仅原稿时间。
Qvo|克沃|人名，155邱弗统一。
Friedisch Adum Silip Qvo|弗里德里希·阿杜姆·西利普·克沃|原稿完整人名。
Faustinius|弗斯蒂尼乌斯|134、155、156统一。
Hieronomus Tezla|希罗诺穆兹·特兹拉|124、155统一。
Inar Satarael|伊纳尔·萨塔拉埃尔|124、137、156统一。
Vianco Locard|维安科·洛卡德|124、156、157统一。
Felicia Tayber|菲莉希亚·泰伯尔|124、156统一。
Delphan Gruss|德尔芬·格鲁斯|124、156统一。
Vethorel|维索雷尔|124、155统一。
Hadron Omega-7-7|哈德隆·欧米伽—7—7|Hadron人名不直接译物理粒子强子。
Kappa-Nu AX77446|卡帕—努 AX77446|Nu希腊字母，不误作数字13。
Chen Phi-8|陈·斐—8|Phi希腊字母，不误作数字21。
Ordinatus|百机战争机器|区别组织 Centurio Ordinatus 百机队；原将军炮等统一。
Thallax|死隶战兵|机械教兵种，不套普通奴隶。
Taghmata Omnissiah|机神禁卫军|沿用核心；与帝皇禁军区分。
Skit-code|护教军暗码|134篇军事通讯用语。
Praetorian|禁卫兵|护教军精锐类型，非帝皇禁军。
Pteraxii|佩莱克斯|由官译完整单位名抽取。
Serberys Corps|塞波利斯兵团|由官译单位名前缀抽取。
Kataphron Battle Servitor|卡塔弗隆战斗机仆|泛称保留音译；Breachers/Destroyers全名采用铁甲攻坚者/破坏者。
Castigator Class Robot|惩戒型机兵|不能把同名修女坦克译名套入历史自动机兵。
Negavolt Cultists|负伏教徒|机械教异端战士。
Rapier Scout Titan|刺剑侦察泰坦|Rapier不是Raptor，原猛禽错误。
Princeps|首席|泰坦与机械教骑士统领，按具体语境。
Moderati|次级操作员|泰坦驾驶辅助人员。
Lance|骑士矛阵|骑士编制，不按武器普通词替换。
Questor Imperialis|帝国骑士|效忠帝皇的一支；Imperial Knights总称中文同形，注明语境。
Questor Mechanicus|机械教骑士|效忠机械教的一支。
Sacristan|圣物保管者|骑士世界技术与礼仪人员。
Ritual of Becoming|成骑仪式|152篇骑士与机甲结合仪式。
Aspirant|候补骑士|仅骑士后裔编制；一般招募语境为候选者。
Uhlan|乌兰枪骑|骑士战斗之道，避免与Lancer机甲同译。
Dolorus|多洛鲁斯|骑士猎兽者职衔。
House Hawkshroud|覆隼家族|152、153统一。
House Procon Vi|普罗孔·维家族|152篇名称完整保留Vi。
Banner of Macharius Triumphant|马卡里亚凯旋旗|仅英文官方表有匹配名称，中文新版未找到对应；不硬配白银怒火战旗。
Genebound|基因缚誓者|霍尔德家族卫队。
Joviann Watchmen|乔维安守望者|专名暂音译，不认定指木星。
Conduit Wars|导流战争|驭电祭司两派之战。
Elucidan Schism|埃卢西丹分裂|专名不直译阐明。
Brotherhood of Petrified Light|石化之光兄弟会|电岩驭电祭司组织。
Cenobyte Servitors|修士机仆|辅佐黑色圣堂教士的单位。
Samech Redemption Servitor|萨米奇赎罪机仆|159篇特殊拾荒机仆。
Transmuter Core|转化核心|不是变速器。
H-Grade Combat Servitor|H级战斗机仆|H等级标识，不擅译高级。
Heavenly Host|天军|Host在此不是主人。
Obliviate|遗忘者|被判技术异端的无魂机仆。
Signa-IX|西尼亚九号|罗马数字IX=9，原四号错误。
Carnicula|血肉延寿派|基因士派别，非普通动作。
Apexists|顶点派|基因士派别。
Companions of Vogel|沃格尔之友|基因士派别。
Circle Varnak|瓦尔纳克之环|与Varnak人名一致。
Divisio Genetor|基因分部|拉特诸世界派别。
Dread Biologis|恐怖生物学派|技术异端派别。
Hippocrasian Sect|希波克拉底派|专名保留原稿音译。
Incunablis order|因库纳布利斯修会|名称不译古版。
Primus Humanum|人类至上派|157篇主张人类形体完美的派系。
Lathe Worlds|拉特诸世界|地点专名，不直接作车床世界。
Anathema Psykana|巫咒修女会|参考官方Anathema Psykana Rhino巫咒犀牛装甲车；机构译名仍暂定。
Blank|空白者|原稿也称无魂者；非灵能者。
Chamber Astra|星界厅|寂静修女负责黑船的部门。
Mistress of the Black Fleet|黑色舰队女主事|165、168统一专门职位。
Vigil|警戒团|参照官方分遣队虚无之女警戒团，历史通用编制暂定。
Vigil Indomitus|不屈警戒团|原不屈守夜人，作为部队而非个人。
Cadre|骨干连|只限寂静修女的连级编制。
Excruciatus|刑讯者|行动人员并非受刑者，原受难者施受关系有误。
Witchseeker Pursuivant|寻巫传令官|高级修女职衔，高于湮灭骑士，非一般随从。
Silent Furies|寂静复仇女神|寂静修女喷气摩托部队。
Null Maiden|虚无之女|参考官方分遣队全称组成部分，独立称呼暂定。
Tanau Aleya|塔瑙·阿莱亚|Aleya官译，Tanau全名部分暂音译。
Magadan Orbital Construct|马加丹轨道设施|元数据Magdan，正文Magadan，中文统一。
Imperial Assignment|帝国灵能评级|165篇等级体系，不直译分配。
Primary psyker|一级灵能者|166篇能力分类，不是初学者，也不与Primaris Psyker混同。
Astropathic Choir|星语唱诗团|169篇星语协同组织。
Astropathic Relay|星语中继站|设施包含唱诗团，原译倒置。
Arbitrator|仲裁官|按核心复数Arbitrators同译。
Grand Provost Marshal|宪兵大元帅|法务部最高职衔。
Precinct-Fortress|警区堡垒|170、171统一。
Lord Marshal|领主元帅|法务部高级职衔。
Execution team|处决小队|不可与强征小队Exaction混同。
Subductor|冲覆者|由官方Subductor Squad冲覆者小队抽取。
Malocator|寻恶者|生物追踪人员。
Leashmaster|牵犬师|机械獒犬操控人员。
Captain-General|禁军元帅|禁军最高领导者。
Companions|近侍|帝皇禁军的贴身护卫，原伙友；与其他派别同名单位区分。
Custodian Tribunate|禁军护民官团|组织而非单个军衔。
Tribune|护民官|禁军高级职衔。
Hykanatoi|亥卡纳托|禁军重步兵阶层，与Custodian Guard语境相近但不抹去原专名。
Hetaeron Guard|伴卫卫队|原侍从卫士、伙友卫队统一。
Kataphraktoi|铁骑结社|由GW09/10第3页强化铁骑结社的老兵抽取。
Tharanatoi|雷殇卫士|禁军终结者阶层。
Vexilus Praetor|掌旗执政官|禁军旗手，非consul领事。
Dread Host|恐惧军团|盾卫军团名，不译恐怖之主。
Solar Watch|太阳守望|盾卫军团名。
Whetted Blade|淬锋之刃|盾卫军团名，不是刺激之刃。
Martial Ka'tah|卡塔武艺|禁军战斗流派体系。
Lockwarden|秘库守监|禁军职衔。
Beyreuth|贝鲁斯|172、173统一暂定音译。
Aesoth Koumadra|伊索特·科马德拉|172、173统一。
Andros Launceddre|安德罗斯·朗塞德尔|172、173统一。
Diocletian Coros|戴克里先·科罗斯|172、174统一。
Caecaltus Dusk|凯卡尔图斯·达斯克|Dusk不是Dust，原达斯特修正。
Arrian Porphyrius|阿里安·波菲里乌斯|保留英文音节，原帕里纽斯遗漏。
Pyrithite Spear|炙烈长矛|从官方完整禁军卫队武器条目抽取，证据是并列全称。
Falchion Class Battleship|弯刀级战列舰|Falchion不是Falcon；舰级按原文保留，型号来源待核。
Emerald Clave|翡翠结社|盾卫连队名称；Clave不是普通棍棒。
'''
for line in provisional.strip().splitlines():
 en,zh,note=line.split('|');rows[en]=dict(zip(fields,[en,zh,'暂定·官方待核','所给英文底稿；当前审校与主审统一决定','第101—175篇',note]))
for en in ['Ordo Xenos','Ordo Hereticus','Ordo Malleus']:
 rows[en]['译名状态']='用户指定';rows[en]['编辑说明']='沿用现稿；原稿别名仅在全书首次出现，已由主审处理，本范围不重复。'
# Add precise official URLs to the previously verified page-2 names too.
for r in rows.values():
 if r['译名状态']=='官方已核对' and r['依据']=='GW-09；GW-10':r['依据']='GW-09 '+zurl+'；GW-10 '+eurl
with (P/'terms.tsv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows.values())
print(len(rows),'terms;',sum(r['译名状态']=='官方已核对' for r in rows.values()),'official')
