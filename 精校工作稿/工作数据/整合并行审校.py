from pathlib import Path
import csv,json,re,io
D=Path(__file__).resolve().parent
corpus=json.loads((D/'全书分段底稿.json').read_text());blocks={b['id']:b for a in corpus for b in a['blocks']}
core=list(csv.DictReader((D/'核心术语定译.tsv').open(),delimiter='\t'));keycol='英文标准词';cols=list(core[0]);terms={r[keycol].casefold():r for r in core}
choices={
 'imperial army':('帝国军','暂定·官方待核','沿最早18/25篇及原核心表，原稿别名帝国陆军；旧制包括后来拆出的海军，不与普通陆军及帝国卫队混同。'),
 'chapter serfs':('战团农奴','暂定·官方待核','与第9篇Chapter Serf单数统一，区别一般侍从。'),
 'sabbat worlds':('萨巴特诸世界','暂定·官方待核','与Saint Sabbat及Sabbat Crusade沿专名统一词根；原安息日诸世界。'),
 'sabbat worlds crusade':('萨巴特诸世界远征','暂定·官方待核','沿Sabbat Worlds统一，首次附原稿别名。'),
 'sabbat crusade':('萨巴特远征','暂定·官方待核','Sabbat Worlds Crusade的简称，统一专名词根。'),
 'saint sabbat':('圣萨巴特','暂定·官方待核','与萨巴特诸世界及相关远征统一专名词根。'),
 'armour of antilochus':('安提洛克斯战甲','官方词根参考·装备全称待核','GW09第32页中文完整单位名身穿安提洛克斯战甲的马涅乌斯·卡尔加证实装备词根；旧英版无同一完整条目。'),
 'thunderstrike las-talon':('雷霆激光爪','官方词根参考·全称待核','GW09第33页/GW10第32页雷霆型风暴速攻艇；武器沿同型号词根，完整武器名称待核。'),
 'glaive encarmine':('赤红战刃','暂定·官方待核','沿403复数Glaives Encarmine统一；Black Library官方FAQ区分剑型与斧型，非所有该类武器都为剑。'),
 'glaive':('长刀号（舰船）／飞刃（坦克）','语境定译·官方待核','448的舰船与1318的坦克不同实体；坦克亦称Fellglaive，参见https://wh40k.lexicanum.com/wiki/Glaive。'),
 'fellglaive':('飞刃坦克','暂定·官方待核','与Glaive坦克同一型号，沿1318统一，原残暴刃；https://wh40k.lexicanum.com/wiki/Glaive仅核英文异名，中文未认定官方。'),
 'spectral nine':('幽影九号', '暂定·官方待核', '沿323既有型号名，1461统一。'),
 'gloriam':('荣耀号', '暂定·官方待核', '沿449既有犀牛名称，1465—1466原辉煌号保留别名。'),
 'deliverance of vulgate':('沃尔盖特救援之战', '暂定·官方待核', '沿845地名和战役名，1475同一事件。'),
 'eyslk-tan':('艾斯利可坦', '暂定·官方待核', '沿571已校人物名，850回改。'),
 'book of mournful night':('哀夜之书', '暂定·官方待核', '术语表不含书名号，正文作《哀夜之书》。'),
 'saim-hann eldar & wraith constructs':('塞姆罕灵族与幽冥构造体', '暂定·官方待核', '沿已校塞姆罕词根，规范组名标点。'),
 'cognis heavy stubber':('智能重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'diabolus heavy stubber':('恶魔重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'questoris heavy stubber':('巡游重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'ironhail heavy stubber':('铁雹重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'ironhead heavy stubber':('铁首重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'tempest heavy stubber':('暴风重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'volg vi “crank cannon” heavy stubber':('伏尔格 VI“曲柄炮”重机枪', '官方词根参考·全称待核', 'GW04/GW11第13页Heavy stubber重机枪；完整型号名称暂定。'),
 'bionics':('仿生改造／仿生部件（依语境）','语境定译·官方待核','分别指改造过程及替代器官的机械部件。'),
 'elucidan schism':('埃卢西丹分裂','暂定·官方待核','沿124、158既有事件名称，统一1046同一事件。'),
 'nuncio-vox':('通讯引导阵列','暂定·官方待核','沿251定译，统一1349；原大使音阵保留在原译栏。'),
 'omni-scrambler':('全频扰频器','暂定·官方待核','沿298定译，单复数同一设备。'),
 'omni-scramblers':('全频扰频器','暂定·官方待核','与Omni-scrambler同一设备，统一223。'),
 'tra':('特拉（第三大连）','暂定·官方待核','芬里斯语大连名保留特拉；叙事语境可用第三大连。'),
 'oruskh dynasty':('奥鲁斯赫王朝','暂定·官方待核','沿既有王朝名；区别Oruscar奥鲁斯卡王朝。'),
 'apds-6a defender':('APDS-6a 防御者','暂定·官方待核','型号与中文名称间统一加空格。'),
 'psyk-out torpedo':('反灵鱼雷','暂定·官方待核','沿反灵武器及反灵手榴弹统一词根，原灭灵鱼雷。'),
 'plasma eradicator':('等离子根除炮','暂定·官方待核','按1303完整武器条目统一1292目录名称。'),
 'the phoenician':('紫庭凤凰','暂定·官方待核','沿640福格瑞姆称号及词源解释，首次保留原稿别名腓尼基人。'),
 'tyndaris':('廷达里斯号（舰船）／廷达里斯（采矿聚落）','语境定译·官方待核','721的打击巡洋舰与1109采矿聚落不同实体，正文依各自语境。'),
 'the lathes':('拉特诸世界','暂定·官方待核','与Lathe Worlds同一地区，统一864原车床诸世界，地名不按普通机械名词直译。'),
 'torquemada coteaz':('托尔克马达·克提兹','官方词根参考·全名待核','GW09/GW10第24页克提兹官译统一姓氏，全名仍待核。'),
 'plasma projector':('等离子投射炮','暂定·官方待核','沿230舰载武器及后续重型版本统一称呼。'),
 'kill team excis':('埃克西斯杀戮小队','暂定·官方待核','沿393已定专名，统一其他同队条目；原切除杀戮小队为异译。'),
 'adamant rifles':('坚定步枪兵','暂定·官方待核','沿834原稿坚定，Adamant不直接视作Adamantium精金。'),
 'winged grail':('带翼圣杯','暂定·官方待核','沿834原稿航空中队名称；补足Grail圣杯词义。'),
 'aegida company':('神盾连','暂定·官方待核','沿450较早已校名称，统一585和1029同一部队；原艾吉达连。'),
 'aegida platform':('神盾轨道站','暂定·官方待核','沿450同一轨道站，原艾吉达平台。'),
 'oberdeii':('奥伯德伊','暂定·官方待核','沿450已校人名，统一585和1029。'),
 'armiger autocannon':('侍从自动炮','官方词根参考·全称待核','依护卫侍从等官方单位名统一Armiger词根，武器全称待核。'),
 'theldrite moonsilver':('塞尔德赖特月银','暂定·官方待核','沿421 Theldrite词根；月银为本处材料全称的一部分。'),
 'deimos-lux pattern psycannon':('迪莫斯—勒克斯型灵能炮','暂定·官方待核','Deimos沿864迪莫斯，亦称火卫二；武器型号保持同一词根。'),
 'plasma burner':('等离子燃烧枪','暂定·官方待核','沿1298完整武器条目，统一1292目录原灼烧者。'),
 'boreas (dark angels)':('波瑞亚斯（黑暗天使）','暂定·官方待核','与660同名人物及北风导弹区分；黑暗天使按官方名称统一。'),
 'legio tritonis':('三辰军团','暂定·官方待核','沿774现稿及其三天体命名解释，864原特里托尼斯统一。'),
 'belisarian furnace':('贝利萨留斯熔炉','官方词根参考·全称待核','与贝利萨留斯·考尔统一人物词根，器官全称暂定；原贝利撒留熔炉。'),
 'mondus occulam':('蒙杜斯·奥库勒姆','暂定·官方待核','同386的Mondus Occulum铸造城，612及773统一中文，保留英文异拼。'),
 'warlord battle titan':('战将级战斗泰坦','官方词根参考·全称待核','沿官方Warlord Titan战将级泰坦统一，英文Battle的全称仍待核。'),
 'death of innocence':('纯真之死','暂定·官方待核','按773事件语义修正614原无罪之死；首次保留旧别名。'),
 'mercury-exultant kill-zone':('水星—欢欣杀戮区','暂定·官方待核','沿659同一防区，统一700及805。'),
 'trisolian a4':('特里索兰 A4','暂定·官方待核','与610的Trisolian-A4同一基地，沿Trisolian特里索兰统一词根。'),
 'vanaheim':('瓦纳海姆','暂定·官方待核','沿181战役名统一864世界名及1219武器产地词根，首次保留原稿异译。'),
 'krakstorm grenade launcher':('穿甲风暴榴弹发射器','暂定·官方待核','统一1221与1229，Krak词根沿穿甲榴弹。'),
 'lakrimae':('泪滴（动力镰刀）','暂定·官方待核','696与1151同一动力镰刀，与舰船Lachrymae泪痕号分开。'),
 'black staff of ahriman':('阿里曼的黑杖','暂定·官方待核','与The Black Staff of Ahriman同一武器，沿549核心定译。'),
 'hidden one':('隐者','暂定·官方待核','与Hidden Ones同一千子身份，沿58篇统一；646与769回修。'),
 'iron blood':('铁血（芬里斯部落）／铁血号（舰船）','语境定译·官方待核','647篇部落与755篇佩图拉博旗舰为不同实体，分义保留。'),
 'saint basillius':('圣巴西利乌斯','暂定·官方待核','统一747、817同一圣人。'),
 'black reach':('黑域','暂定·官方待核','明确行星名，原黑色河段误取水文词义；首次保留原稿别名。'),
 'mpandex':("姆'潘德克斯",'暂定·官方待核',"与M'Pandex同一铸造世界，原文拼写无撇号时保留英文变体，中文统一。"),
 "hesiod's wake":('赫西奥德的觉醒','暂定·官方待核','与Hesiod姓名词根统一；地名暂定，非本人。'),
 'fidus kryptman':('菲杜斯·克瑞普特曼','暂定·官方待核','与18、98、828篇的Kryptman同一人物，姓名词根统一。'),
 'kryptman census':('克瑞普特曼统计','暂定·官方待核','与人物Kryptman克瑞普特曼统一词根。'),
 'sacristan':('圣物保管者（骑士职务）／萨克里斯坦（世界）','语境定译·官方待核','骑士世界的技术礼仪人员与826篇的世界专名分义。'),
 "drach'nyen's host":('德拉科尼恩的宿主','暂定·语义及官方待核','733与805保留host语义待核；可能另指军势，不指认任何特定宿主。'),
 'piscina':('皮希纳','暂定·官方待核','按已定Piscina IV皮希纳四号统一星系词根。'),
 'naysmith':('谏官','暂定·官方待核','依249与729所述审视命令和提出异议的职责定译；首次保留原稿别名否决铁匠，不按smith字面误解为工匠。'),
 'lord high admiral':('海军至高上将','暂定·官方待核','811与859同一海军高级职衔；不同于Lord High Admiral of the Imperial Navy全称时的具体席位描述。'),
 'daughter of torment':('折磨之女号','暂定·官方待核','668与805同一掠夺者级泰坦，统一具名机体名称。'),
 'irthu haemotalion':('伊图·哈默塔利昂','暂定·官方待核','沿80姓名，统一624和730同一内政部之主。'),
 'prefectia campaign':('总督星战役','暂定·官方待核','依Prefectia行星总督星统一456与713篇战役名称。'),
 'gauntlet of the forge':('铸炉臂铠','暂定·官方待核','统一452、708、709同一遗物；非锻造之手。'),
 'manushya-rakshsasi':('玛努沙·拉克莎希', '暂定·官方待核', '沿第0643篇守密者专名，第0800篇原别名罗刹女保留校注。'),
 'cardinal gate':('枢机之门','暂定·官方待核','沿第0322篇地名；一般职衔Cardinal仍为红衣主教。'),
 'firebrand':('火焰烙印号（舰船）／纵火者（福格瑞姆的枪械）','语境定译·官方待核','第0558篇舰船与第0640篇爆燃突击铳为不同对象，不能混同。'),
 'vesalius':('维萨里号','暂定·官方待核','沿第0567篇舰名；第0641篇维萨留斯号为同舰异译。'),
 'tarnhelm':('塔恩海姆号','暂定·官方待核','沿第0183与0703篇，统一0793篇同一潜行舰。'),
 'heliosa-78':('赫丽奥萨-78','暂定·官方待核','沿第0701篇姓名，统一第0798篇。'),
 'dalia cythera':('达莉亚·库忒拉','暂定·官方待核','沿第0022篇；统一第0614篇姓名。'),

 'visions of heresy':('荷鲁斯叛乱编年史','暂定·官方待核','沿179最新校稿，书名未核官网。'),
 'legions of the horus heresy':('荷鲁斯叛乱诸军团','暂定·官方待核','沿179最新校稿，书名未核官网。'),
 'bror tyrfingr':('布罗尔·蒂尔芬格','暂定·官方待核','沿183已定人名。'),
 'dark sentry':('黑暗哨兵号（打击巡洋舰）／黑暗哨兵（游荡行星）','语境定译·官方待核','448舰船与779进入星系后被交战双方登陆的行星为不同实体。'),
 'canticle city':('颂歌城','暂定·官方待核','沿529已定地名。'),
 'siridor vhen':('希瑞多·维恩','暂定·官方待核','沿561已定人名。'),
 'alajos':('阿拉霍斯','暂定·官方待核','沿633已校人名。'),
 'first master':('首席舰务官（舰员职务）／第一大师（极限战士职衔）','语境定译·官方待核','82舰员职务与盖奇在军团中的称号不混同。'),
 'triarch':('三圣（太空死灵统治议会）／三叉戟成员（钢铁勇士职衔）','语境定译·官方待核','不同阵营相同英文分义，三圣禁卫完整单位官译不扩至钢铁勇士。'),
 'excindio battle-automata':('灭绝者自动机兵','暂定·官方待核','沿2单名Excindio灭绝者，全称同一自动机兵，原毁灭者统一。'),
 'chirurgeon-general':('总医官','暂定·官方待核','沿80既定官职，非军衔。'),
 'garran crowe':('加兰·克罗','官方词根参考·全名待核','GW09/GW10第23页克罗堡主，完整个人姓名仍待核。'),
 'triton class aegis cruiser':('海卫一级神盾巡洋舰','暂定·官方待核','舰型中Aegis采用神盾，非现代军舰宙斯盾系统；不推定与灰骑士神盾关联。'),
 'chalnath expanse':('查尔纳斯广域','暂定·官方待核','沿18同一地区名。'),
 'wych cults':('巫灵教团','官方词根参考·组织全称待核','GW09/GW10第20页Wyches巫灵，组织名沿572—573。'),
 'sul kontep':('苏尔·孔泰普','暂定·官方待核','沿96/549既有人名。'),
 'triumph of reason':('理性凯旋号','暂定·官方待核','沿554现稿舰名。'),
 'kronus':('克洛诺斯','暂定·官方待核','沿核心现稿行星名；区别虫巢舰队Kronos克罗诺斯。'),
 'reanimation protocols':('复生协议','暂定·官方待核','沿已有核心名称。'),
 'gladiator group 138':('第 138 角斗士群','暂定·官方待核','Group与Cadre331编制形式区分；沿540正文。'),
 'cadre':('骨干连（寂静修女）／核心队（钛族）','语境定译·钛族词根参考','不同阵营编制分译；钛族参考GW09第35/GW10第34页Retaliation/Auxiliary Cadre。'),
 'arkhas fal':('阿尔卡斯·法尔','暂定·官方待核','沿先前军团长人物定译。'),
 'deathsworn':('死誓者','语境定译·官方待核','太空野狼军团兵种与钛军莫拉里安辅助兵种同名，不能合并身份。'),
 'auric auxilia':('黄金辅助军','暂定·官方待核','沿240山阵号常备卫队名称。'),
 'genestealer magus':('基因窃取者占星师','官方词根参考·全称待核','GW09/GW10第22页Magus占星师，原书另加种族限定。'),
 'cult benefictus':('教派赐灵者','官方词根参考·全称待核','GW09/GW10第22页Benefictus赐灵者，原书另加教派限定。'),
 'neurothrope':('神经脑虫','暂定·官方待核','区别已核Neurogaunts神经虫；原神经虫同译易混淆。'),
 'master of rites':('祭仪大师','暂定·官方待核','同Master of the Rites，职衔冠词有无不构成两种职务。'),
 'master of the rites':('祭仪大师','暂定·官方待核','同Master of Rites。'),
 'wyrd':('灵能异人（灵能者类别）／命数（芬里斯观念）','语境定译·官方待核','芬里斯命运观念不套用涅克罗蒙达灵能者名称。'),
 'helix adept':('螺旋医疗员','暂定·官方待核','按266明确尚未完成药剂师训练的资格区分命名；其他篇英文资格差异仍保留原文并注。'),
 'vanguard helix adept':('先锋螺旋医疗员','暂定·官方待核','同Helix Adept，避免名称使人误以为已是正式药剂师。'),
 'maleum':('玛勒姆','暂定·官方待核','与Maeleum指同一恐惧之眼行星，沿554统一玛勒姆，非人物名。'),
 'prognosticator':('预言者（银色颅骨职衔）／预言器（跃迁设备）','语境定译·官方待核','人物职衔与导航计算设备分义。'),
 'tormentors':('折磨者（星际战士战团）／施虐者（帝皇之子单位）','语境定译·单位官译已核','GW09/GW10第21页施虐者仅核帝皇之子单位，不套用于225篇同名战团。'),
 'the redacted':('抹除者','暂定·官方待核','原编辑者、修订者均误读redacted；指被删隐抹除的组织，非从事编辑工作的人。'),
 'caster of runes':('符文祭司','暂定·官方待核','太空野狼军团时期职衔；后世Rune Priest称符文牧师，保留时代称谓区别。'),
 'venerable dreadnought':('神圣无畏机甲','官方词根参考·通称待核','GW09第34/GW10第33的太空野狼完整单位词根；不混并各阵营规则身份。'),
 'war of beasts':('野兽之战','暂定·官方待核','警戒星战争，区别M32的War of the Beast野兽战争。'),
 'mindwitch':('心灵巫师','暂定·官方待核','灵能专长类型不限定性别；原心灵女巫保留对照。'),
 'teef':('牙币','暂定·官方待核','欧克以牙齿作货币；正文直接数几颗牙符合语境。'),
 'executioners':('处刑者','语境定译·官方待核','星际战士战团与灵族海盗团同译，所属对象须按语境区分。'),
 'reborn':('复生者（战团）／重生者（死神军自称）','语境定译·官方待核','分指不同组织，不混合历史。'),
 'steel confessors':('钢铁神父','暂定·官方待核','沿225现稿战团名，原钢铁告解者为别名。'),
 'stormspeaking':('风语学派','暂定·官方待核','沿早期核心定译，白疤灵能学派。'),
 'asdrubael vect':('阿斯杜巴尔·维克特','暂定·官方待核','沿第9篇人名，后续各章统一。'),
 'breacher siege':('攻坚者','暂定·官方待核','军团攻坚兵种；区别 Devastator 破坏者，非沿用其他阵营同名单元认证。'),
 'praetorian breacher squad':('禁卫军攻坚小队','暂定·官方待核','按军团兵种语境分译。'),
 'haakonath':('哈科内斯','暂定·官方待核','沿233已校名称；Haakoneth 为同一星球异拼。'),
 'belis corona':('贝利斯·卡罗纳','暂定·官方待核','沿18已校行星专名。'),
 'sensei-emperor':('导师—帝皇','暂定·官方待核','沿23现稿复合称号。'),
 'anathame':('诅咒之刃','暂定·官方待核','特指从英特雷斯盗取的基尼布拉赫母刃；通称 athame 则为仪式之刃，首次保留原稿别名。'),
 'h-grade combat servitor':('H 级战斗机仆','暂定·官方待核','保留英文等级 H，统一中英文空格。'),
 'tech adept':('技术专家','暂定·官方待核','按第0155篇火星祭司体系职衔及第0069篇原译统一。'),
 'imperialis armada':('帝国无敌舰队','暂定·官方待核','沿第0081篇专名，为帝国海军前身，不泛替换帝国舰队。'),
 'master':('导师（审判庭职衔）／舰务官（舰员职务）','语境定译·官方待核','只适用于对应职衔；普通名词及复合专名另按上下文处理。'),
 'ark reach secundus':('方舟疆域塞昆杜斯','暂定·官方待核','Reach 此处为星际疆域，不是河段；Secundus 保留专名音译。'),
 'cordon impenetra':('绝对封锁','暂定·官方待核','沿第0099篇专名；按句可称绝对封锁防线，非一份封锁令。'),
 'electro-priesthood':('驭电祭司团','暂定·官方待核','由已核官方单位驭电祭司统一组织名，组织全称仍标待核。'),
 'acolytum':('侍僧（智库学徒）／技术侍僧（机械教派）','语境定译·官方待核','同形词在星际战士智库与机械教派中分别对应不同学徒职衔。'),
 'order elucidatum':('阐释修会','暂定·官方待核','沿第0478篇精校；马卡多的秘密组织，非审判庭分支。'),
 'archmagos dominus':('统御大贤者','暂定·官方待核','沿机械修会职衔；区别完整官方兵种技术祭司主宰者。'),
 'vigil':('警戒团（静默修女编制）／警戒堡（红蝎空间站）／守夜星（行星）','语境定译·官方待核','编制、空间站与行星专名分译，不套用于其他含 Vigil 的名称。'),
 'helot':('农奴；希洛人（古希腊语境）','语境定译·官方待核','战锤劳役制度中按农奴理解；词源段落用希洛人。'),
 'master of the arsenal':('军械大师','暂定·官方待核','与第0271篇职衔标题一致。'),
 'master of the fleet':('舰队大师','暂定·官方待核','与第0272篇职衔标题一致。'),
 'master of the forge':('铸造大师','暂定·官方待核','与第0262篇职衔标题一致。'),
 'master of the watch':('守望大师','暂定·官方待核','与第0270篇职衔标题一致。'),
 'master of relics':('遗物大师','暂定·官方待核','与第0276篇职衔标题一致。'),
 'master of reconnaissance':('侦察大师','暂定·官方待核','与第0278篇职衔一致，侦查规范为侦察。'),
 'occulus bolt carbine':('全知者爆矢卡宾枪','暂定·官方待核','沿较早现稿与第0304篇，原目镜异译存对照。'),
 'acheron':('黄泉星','暂定·官方待核','沿第0018篇战争世界列表，同一地名不另改阿刻戎。'),
 'long war':('万古长战','暂定·官方待核','沿第0526篇专名，与普通描述的漫长战争区分。'),
 'ollanius pius':('欧良尼乌斯·庇乌斯','官方词根参考·全名待核','GW-09 与 GW-10 第9页死亡面具确认名字词根；人物全名未作官方全称认证。'),
 'ollanius persson':('欧良尼乌斯·佩松','官方词根参考·全名待核','GW-09 与 GW-10 第9页死亡面具确认名字词根；不因与Pius同名而合并人物，Oll简称仍作欧尔。'),
 'diamor':('迪亚莫尔','暂定·官方待核','与第0018篇和第0558篇战役名统一，不能与Cryptus冥府混同。'),
 'orders militant':('战斗修会（战斗修女）／武装骑士团（黑暗天使）','语境定译·官方待核','两个组织使用相同英文通称，按时代与所属组织分译。'),
 'fabricator-general':('铸造将军','暂定·官方待核','沿用机械修会现稿职衔，不视作普通军衔。'),
 'adept':('帝国任职者（广义）／文吏（行政语境）','语境定译·官方待核','第0069篇使用广义头衔；普通能力形容词按句翻译。'),
 'epistolary':('星语官','暂定·官方待核','沿用第0254篇职衔，与 Astropath 星语者分开。'),
 'lectitio divinitatus':('神性论','暂定·官方待核','书名《神性论》；同名信仰称神性论信仰。'),
 'departmento exacta':('计校部','暂定·官方待核','按第0470篇标题统一，原先记校部为异写。'),
 'apocrypha of skaros':('斯卡罗斯次经','暂定·官方待核','与第0232篇标题统一。'),
 'librarius':('智库（机构）／智库学派（灵能学派）','语境定译·官方待核','机构与灵能学派分别翻译，禁止不分语境替换。')}
variant_choices=D/'全书统一复核/术语变体决定.json'
if variant_choices.exists():choices.update(json.loads(variant_choices.read_text()))
# Apply confirmed choices even when the current snapshot has no new proposal for a term.
for key,(zh,status,note) in choices.items():
 if key in terms:
  terms[key]=dict(terms[key]);terms[key].update({'采用中文':zh,'译名状态':status,'编辑说明':note})
  if key in {'ollanius pius','ollanius persson'}:
   terms[key]['依据']='GW-09；GW-10';terms[key]['定位']='两版PDF第9页，Death Mask of Ollanius，姓名词根参考'
notes=json.loads((D/'编辑疑点与说明.json').read_text());titles=json.loads((D/'精校篇名.json').read_text()) if (D/'精校篇名.json').exists() else {};adds=json.loads((D/'补充译文.json').read_text()) if (D/'补充译文.json').exists() else {}
reviewed=set(range(1,25));registry_path=D/'并行稿件映射.json';registry=json.loads(registry_path.read_text()) if registry_path.exists() else {};snapshots=[];proposals={}
for folder in sorted((D/'并行审校').iterdir()):
 if not (folder/'reviewed.json').exists():continue
 rv=set(json.loads((folder/'reviewed.json').read_text()));ed=json.loads((folder/'edits.json').read_text());lo,hi=map(int,folder.name.split('-'))
 assert all(lo<=n<=hi for n in rv),folder
 assert not (reviewed&rv),(folder,'重复篇号')
 ed={k:v for k,v in ed.items() if int(k[1:5]) in rv}
 for k,v in ed.items():
  assert k in blocks and blocks[k]['language']!='en' and blocks[k]['kind']!='image',(folder,k)
  assert isinstance(v,str) and v.strip(),(folder,k)
 reviewed|=rv
 idx=registry.setdefault(folder.name,1001+len(registry))
 snapshots.append((D/f'人工精校译文-{idx}.json',ed))
 for k in list(notes):
  if k in blocks and int(k[1:5]) in rv:del notes[k]
 for fn,target,articlekeys in [('notes.json',notes,False),('additions.json',adds,False),('titles.json',titles,True)]:
  f=folder/fn
  if not f.exists():continue
  obj=json.loads(f.read_text())
  for k,v in obj.items():
   if (int(k) if articlekeys else int(k[1:5])) in rv:
    if fn=='additions.json':assert blocks[k]['language']=='en',k
    target[k]=v
 tf=folder/'terms.tsv'
 if tf.exists():
  for r in csv.DictReader(tf.open(encoding='utf-8-sig'),delimiter='\t'):proposals.setdefault(r[keycol].casefold(),[]).append(r)
conflicts=[]
for key,rows in proposals.items():
 allrows=([terms[key]] if key in terms else [])+rows
 official=[r for r in allrows if r['译名状态'].startswith('官方已')]
 if key in choices:
  chosen=dict(official[-1] if official else allrows[-1]);chosen['采用中文'],chosen['译名状态'],chosen['编辑说明']=choices[key];terms[key]=chosen
 elif official:
  if len({r['采用中文'] for r in official})>1:conflicts.append([key,'官方内部译名差异',[r['采用中文'] for r in official]])
  else:terms[key]=dict(official[-1])
 elif len({r['采用中文'] for r in allrows})==1:terms[key]=dict(allrows[-1])
 elif key not in terms and len({r['采用中文'] for r in rows})==1:terms[key]=dict(rows[-1])
 else:conflicts.append([key,'暂定译名冲突',[r['采用中文'] for r in allrows]])
if conflicts:
 (D/'并行整合阻断项.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2));print(json.dumps(conflicts,ensure_ascii=False,indent=2));raise SystemExit('先处理词义冲突；未改主稿数据')
# Existing user decisions remain authoritative.
decisions=json.loads((D/'用户术语决定.json').read_text())
for key,r in decisions.items():assert terms[key]['采用中文']==r['采用中文'],key
for path,obj in snapshots+[(D/'编辑疑点与说明.json',notes),(D/'精校篇名.json',titles),(D/'补充译文.json',adds),(D/'语言精校篇目.json',sorted(reviewed)),(registry_path,registry),(D/'校对整合决策.json',choices)]:
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2));tmp.replace(path)
with (D/'核心术语定译.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows({c:r.get(c,'') for c in cols} for r in terms.values())
print(json.dumps({'reviewed_articles':len(reviewed),'core_terms':len(terms),'edits_in_parallel_files':sum(len(o) for p,o in snapshots),'mapped_files':registry},ensure_ascii=False))
