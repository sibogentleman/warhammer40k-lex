from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(k,t):e[f'A0574-B{k:04d}']=t
p(122,'Nobz 强蛮人')
p(124,'强蛮人（原稿又称“老大”）构成欧克的统治阶层，比其他同族更壮、更具攻击性。他们或担任小队领袖，或组成自己的战群。强蛮人享有优良装备、武器与护甲，也常与装备相近的同阶成员一同行动。因此，战场上可见多种不同的强蛮人战群，包括：')
p(126,'重甲强蛮人——身穿超重型护甲的强蛮人')
p(128,'怪枪小子——装备最奇异、最昂贵远程武器的强蛮人')
p(130,'赛博欧克——本处指自愿接受、或因负伤而接受痛苦小子大规模外科改造的强蛮人')
p(132,'摩托强蛮人——骑战斗摩托投入战场的强蛮人')
p(133,'Boyz 蛮人小子')
p(135,'蛮人小子是最常见的欧克。依照地位与装备，又可分成许多类别：')
p(137,'蛮人小子——“标准”的欧克，通常依远程或近战装备编成战群')
p(139,'硬皮小子——身穿重型护甲的蛮人小子，地位通常仅次于强蛮人')
p(141,'特种兵——欧克狡诈本性的集中体现，编队潜入敌后，制造破坏与混乱')
p(143,'喷火小子——偏爱火焰武器的欧克，通常由技师小子而非强蛮人领导')
p(145,'坦克破坏者——专门摧毁敌方载具的欧克部队')
p(147,'蛮人拾荒者——装备搜罗来的最重型武器，擅长从战场或敌营中搜刮装备')
p(149,'风暴小子——装备跳跃背包，多为年轻欧克，却有着同族少见的纪律性')
p(151,'摩托小子——酷爱速度，骑战斗摩托作战的欧克')
p(153,'飞空小子——驾驶飞行器的极速怪胎')
p(155,'野猪小子——骑战猪投入战斗的欧克')
p(157,'跳跳猪小子——骑四足史古格战猪作战的兽霸')
p(159,'豢兽师小子——步行作战的兽霸')
p(162,'欧克的“技术”看似破烂、东拼西凑，威力却不逊于帝国兵器。技师不断进行欠缺周详考虑的实验，竞相制造更大的枪、更庞大的加冈特、更快的战斗越野车。因此，装备缺乏统一标准，战帮看起来总像杂乱的拼盘。技师小子擅长制造强大防护力场，也精于战场抢修，几乎任何烧毁残骸都能回收利用。许多欧克载具据报已被摧毁数十次，仍能拼回原样，随便刷层漆——有时连漆都省了——又开回战场。欧克身体强韧，也能轻易承受粗糙的机械义体强化、器官移植，以及种种胡来的医疗操作。')
p(164,'Ork Battlewagon 欧克战斗堡垒')
p(166,'许多欧克技术不可靠，在其他种族看来甚至根本无法运转；有些设备确实只有落到欧克手中，才能正常工作。部分机械修会成员因此推测，欧克的灵能特性可能影响装备，帮助其运作。但这一理论是否成立，仍无定论。')
p(169,'欧克能借类似帝国亚空间引擎的装置，实现超光速航行。有些引擎由回收的帝国残骸重建；另一些则是围绕取出体外的灵能小子大脑，拼成的诡异机器。技术粗糙、危险，随时可能酿成灾难，欧克似乎全不在乎。')
p(172,'欧克是分布最广的智慧种族，足迹遍及银河。多数时候，他们行动无定，“疆域”也缺乏统一组织。不过，奥克塔琉斯与查拉顿等强大欧克帝国，是显著的例外。')
p(174,'Primary Ork Domains 主要欧克势力疆域')
p(178,'最凶名远播、最成功的战争头目，被称作“军阀”或“大头目”。他们统率数个部落，占据若干世界，建立通常规模不大的帝国。格外强大者还会自封独有头衔，例如“头号纵火狂”。')
p(180,'碎骨者·斯拉卡——高夫军阀，因两度入侵阿玛吉多顿星系而闻名')
p(184,'奥克塔琉斯暴君——奥克塔琉斯欧克帝国统治者')
p(204,'Mekboss Buzzgob 技师头目巴兹戈布')
p(213,'老祖格沃特——强大的灵能小子')
p(215,'鬼祟鼠——欧克特种兵头目')
p(217,'瓦兹达卡·古茨梅克——传奇欧克摩托骑手')
p(221,'佐德格罗德·沃茨纳加——著名牧奴者')
p(223,'莫兹罗格·斯夸格巴德——兽霸')
p(226,'严格说来，欧克是最早进入后来《战锤40,000》宇宙的概念。1985年，Games Workshop 推出编号 LE1 的“太空兽人”限量模型，略早于编号 LE2 的星际战士模型。两者都先于1987年《战锤40,000：行商浪人》发行。')
p(230,'第一版最早的规则中，已经收录“太空欧克掠袭者”。他们比现代设计更矮小，却同样绿皮、佝偻，长着满口獠牙。极端暴力的天性、屁精奴隶阶层，以及原始却有效的技术等大多数基本设定，都已在第一版确立。不过，彼时他们的暴力似乎更源于对一切非欧克生命的仇恨，而非单纯享受打仗。')
p(232,'1990—1991年出版的《Waaargh: Orks》《’Ere We Go》与《Freebooterz》，确立了多数现代欧克背景：热爱战斗、真菌本质、搞哥与毛哥、天生的技术能力与不同文化倾向，例如怪怪小子、飙速教派和各大氏族，以及神秘的聪明小子。按本篇记载，1998年推出《Gorkamorka》后，欧克的外观变得更凶悍，也更具破烂拼装的风格。')
n.update({'A0574-B0124':'Nobz采用官方强蛮人；原老大作为别称保留，不与Warboss战争头目混同。','A0574-B0126':'Mega Nobz与Meganobz为拼写差异，采用重甲强蛮人；Flash Gitz怪枪小子，来自GW09第30/GW10第29页。','A0574-B0130':'Painboy为痛苦小子，原痛苦老大混入另一职衔；Cyborks类别不限于此处一句所列地位，因此表述“本处指”保留列表语境。','A0574-B0141':'Kommandoz／Kommandos对应特种兵；Burna Boyz喷火小子、Tankbustas坦克破坏者、Lootaz／Lootas蛮人拾荒者为官方单位名。','A0574-B0159':'fight on their two feet为步行作战，不是用两只脚打架；Beast Snagga Boyz官方完整名豢兽师小子。','A0574-B0166':'装备受群体灵能影响在本篇中仍是机械修会理论，保留未定论，不扩写为欧克想什么就成真的通则。','A0574-B0169':'disembodied brain为脱离身体的大脑，不是无实体的大脑。','A0574-B0217':'GW09中文第30页可见瓦兹达卡·古茨梅克，GW10旧版同栏未列，标官方中文参考，不伪称两版直接对照。','A0574-B0221':'Zodgrod Wortsnagga佐德格罗德·沃茨纳加、Mozrog Skragbad莫兹罗格·斯夸格巴德直接对应GW09第30/GW10第29页；Runtherd沿早期核心牧奴者。','A0574-B0226':'LE1、LE2为限量模型编号；原英文引号残缺，不按一英寸尺寸擅自解读。','A0574-B0232':'三个出版物保留英文正式书名，不将’ Ere We Go、Gorkamorka机械词译成乱码式中文。原文Gorkamorka的1998年日期待出版史核实，保留来源限定。Oddboyz应为怪怪小子，非Weirdboy灵能小子。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
u9='https://assets.warhammer-community.com/chi_06-05_wh40k_core%26key_munitorum_field_manual-5mrlucr2t1-fkybzzzoce.pdf';u10='https://assets.warhammer-community.com/eng_warhammer40000_munitorum_field_manual_march_2025-cims9ya3sg-s8j9m2haae.pdf'
for en,zh in [('Battlewagon','战斗堡垒'),('Beast Snagga Boyz','豢兽师小子'),('Big Mek','蛮人大技师'),('Boss Snikrot','鬼祟鼠头目'),('Boyz','蛮人小子'),('Burna Boyz','喷火小子'),('Flash Gitz','怪枪小子'),('Ghazghkull Thraka','碎骨者·斯拉卡'),('Gretchin','屁精'),('Kommandos','特种兵'),('Lootas','蛮人拾荒者'),('Meganobz','重甲强蛮人'),('Mek','蛮人技师'),('Mozrog Skragbad','莫兹罗格·斯夸格巴德'),('Nobz','强蛮人'),('Painboy','痛苦小子'),('Squighog Boyz','跳跳猪小子'),('Stormboyz','风暴小子'),('Tankbustas','坦克破坏者'),('Warbikers','摩托小子'),('Warboss','战争头目'),('Weirdboy','灵能小子'),('Zodgrod Wortsnagga','佐德格罗德·沃茨纳加')]:
 by[en.casefold()]=dict(zip(cols,[en,zh,'官方已核对',f'GW-09 {u9}；GW-10 {u10}','GW09中文第30页；GW10英文第29页','两版官方单位清单按名称对应；非按行位置或点数匹配。']))
by['wazdakka gutsmek']=dict(zip(cols,['Wazdakka Gutsmek','瓦兹达卡·古茨梅克','官方中文参考·英文对应待复核',f'GW-09 {u9}','中文PDF第30页；英文名见底稿574','较旧GW10对应页未列此人物，未作为双版全称核对。']))
pairs='''Orkoids|欧克类
Brain Boyz|聪明小子
Oddboyz|怪怪小子
Mekboyz|技师小子
Tribe|部落（欧克组织）
Mob|战群（欧克组织）
Bad Moons|恶月
Blood Axes|血斧
Deathskulls|死颅
Evil Sunz|邪日
Goffs|高夫
Snakebites|蛇咬
Speed Freeks|极速怪胎
Freebooterz|流寇
Kult of Speed|飙速教派
Feral Orks|蛮荒欧克
Beast Snaggas|兽霸
Sneaky Gitz|鬼祟小子
Boom Boyz|爆炸小子
Pyromaniacs|纵火狂
Big Krumpaz|轰爪欧克
Trukk Boyz|卡车小子
Gork|搞哥
Mork|毛哥
Great Green|大绿
Makari|马卡利
teef|牙齿（欧克货币）
Warbuggy|战斗越野车
Brewboyz|酿酒小子
Sloppers|做饭小子
Cyborks|赛博欧克
Nob Bikerz|摩托强蛮人
’Ard Boyz|硬皮小子
Flyboyz|飞空小子
Boarboyz|野猪小子
Warboars|战猪
Squighog|史古格战猪
Gargant|加冈特
Charadon|查拉顿
Arch-Arsonist|头号纵火狂
Nazdreg Ug Urdgrub|纳兹德雷格·乌骨·乌德格拉布
The Overfiend of Octarius|奥克塔琉斯暴君
Snagrod|斯纳哥罗德
Grog Ironteef|格罗格·铁牙
Alsanta|阿尔桑塔
Tuska|图斯卡
Grukk Face-Rippa|撕脸者格鲁克
Red Waaagh!|红潮
Garaghak|加拉哈克
Tallarax|塔拉拉克斯
Klawjaw|爪颚
Bork|博克
The Arch-Maniac of Calverna|卡尔维纳的头号疯子
The Beast|野兽
Gharkul Blackfang|伽尔库·黑牙
Mekboss Buzzgob|技师头目巴兹戈布
Kaptin Badrukk|烂赌鬼船长
Kaptin Dedeye|死眼船长
Mad Dok Grotsnik|疯医戈斯尼克
Old Zogwort|老祖格沃特
Zagstruk|祖格斯图卡'''
for line in pairs.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0574','按本篇语境与已有译名；英文单复数、欧克口音拼写见正文，非新种族。'])))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
# Preserve the source's established name for the coven; no unnecessary change of lineage to descendants.
for k,v in e.items():e[k]=v.replace('黑色血裔','黑色血统')
for k,v in n.items():n[k]=v.replace('Black Descent暂作黑色血裔','Black Descent沿黑色血统')
p=P/'terms.tsv';p.write_text(p.read_text().replace('Black Descent\t黑色血裔','Black Descent\t黑色血统'))
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{574};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':574,'read_through_block':232,'complete':True},ensure_ascii=False,indent=2))
print('574 complete')
