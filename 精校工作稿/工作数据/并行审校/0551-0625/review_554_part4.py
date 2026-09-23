from pathlib import Path
import json,csv,io
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(k,t):e[f'A0554-B{k:04d}']=t
p(283,'第二十七连——原文使用罗马数字，写作 XXVII 连。')
p(292,'Known post-Heresy warbands 荷鲁斯之乱后已知战帮')
p(297,'True Sons 真子')
p(311,'理性凯旋号——副将级战列舰，原为巨口港舰队旗舰，被荷鲁斯之子俘获后改名鞭笞号。')
p(315,'噬王者号——战斗驳船。')
p(317,'冥界王座号——战斗驳船。')
p(327,'祂的选中之子号——战列巡洋舰。')
p(331,'卢佩卡尔之矛号——日蚀级战列巡洋舰。')
p(343,'卢佩卡尔传令官号——巡洋舰。')
p(347,'四重之狼号——巡洋舰。')
p(354,'安特穆拉安魂曲号——志留亚级轻型巡洋舰。')
p(366,'科索尼亚之血号——浩劫级驱逐舰。')
p(368,'科索尼亚之裔号——猎手级驱逐舰。')
p(373,'科索尼亚之狼——犀牛战车。')
p(397,'科索尼亚之名，很可能取自希腊语 Chthonia。这个词含义复杂，关联地底的亡者领域与冥界精灵。冥界精灵既可带来丰饶，也可造成毁灭：从正面看，它们属于重生的意象，象征滋养万物的大地；从负面看，则如重返人间的亡灵，为冥府索取更多灵魂。可以将这种双重寓意，与影月苍狼母星被采掘殆尽、死气沉沉的状态，以及它孕育混沌星际战士的作用相对照。')
p(399,'影月苍狼及后来的荷鲁斯之子，一直被描述为规模较大的星际战士军团，大远征期间某一阶段至少拥有二十五个连。当时资料虽未给出军团总人数上限，但在63-19星球的低语之首行动中，全员出动的第十连约有六百名战士。若二十五个连规模相同，军团当时便可能约有一万五千人。这里需要留意，出版物对军团规模的设定，多年来曾有变动。一度由《阿斯塔特索引》文章确立的“小军团”概念占据主流，《荷鲁斯之乱》系列早期小说也以此为基础；后来，系列逐步修订设定，转向《背景图录》等作品提出的“大军团”概念。以一万人为军团基准时，一万五千人的影月苍狼确属较大的军团，也能与系列后续提供的数字相符，例如小说《福格瑞姆》所述登陆点大屠杀的参战人数。但基准改为十万人后，依此推算，影月苍狼应有十万至十五万人；十五万是此处所举第二大军团怀言者的人数。于是，洛肯连队的六百人只能作为个别描写，不能再据此估算军团总兵力。')
n.update({'A0554-B0311':'Triumph of Reason 原译胜利之因把 Reason 的理性义误作原因，暂修正理性凯旋号；舰级 Legatus 沿现稿副将级待核。','A0554-B0315':'King Eater 为吞噬王者者，原译吞噬之王颠倒修饰关系，暂修正噬王者号。','A0554-B0343':'Pursuivant 此处暂按传令职衔翻译；Lupercal 与本篇人物及其他舰名统一为卢佩卡尔。','A0554-B0397':'本段是词源推测，保留 presumably 的不确定性；不将词源解读标为官方确认设定。','A0554-B0399':'本段为所给原文关于不同出版时期兵力设定的分析，不是独立核实后的定论；其十万至十五万推算与篇首十三万至十七万并不一致，保留两处并说明。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));by={r['英文标准词'].casefold():r for r in rows};cols=list(rows[0])
termtext='''Horus Lupercal|荷鲁斯·卢佩卡尔
Lupercal|卢佩卡尔
Maeleum|玛勒姆
Maleum|玛勒姆
Mournival|四王议会
Justaerin|加斯塔林
Catulan Reaver Squad|卡图兰掠夺者小队
Reaver Attack Squad|掠夺者攻击小队
Luperci|狼之兄弟
Luna Wolves|影月苍狼
Thrice-Cursed Traitors|三重诅咒叛徒
Sons of the Eye|眼之子
Wolves of Horus|荷鲁斯之狼
True Sons|真子
True Sons of Cthonia|科索尼亚真子
Order of the Serpent|蛇之结社
Serpent Lodge|蛇之结社
Speartip|矛尖
Long War|漫长战争
Vengeful Spirit|复仇之魂号
Magna Tyranis|大暴君号
Triumph of Reason|理性凯旋号
Lash|鞭笞号
King Eater|噬王者号
Throne of the Underworld|冥界王座号
War Oath|战争誓言号
Warmaster's Mercy|战帅慈悲号
Conqueror's Pride|征服者之傲号
Tomb of Gold|黄金之墓号
His Chosen Son|祂的选中之子号
Ikon|伊康号
Lupercal's Spear|卢佩卡尔之矛号
Bone Jackal|骨豺号
Gore Prow|血首号
Chariot of the Gods|众神战车号
Baleful Eye|恶意之眼号
Lupercal Pursuivant|卢佩卡尔传令官号
Horus Triumphant|荷鲁斯胜利号
Fourfold Wolf|四重之狼号
Cthonia Rising|科索尼亚崛起号
Cthonic Blood|科索尼亚鲜血号
Requiem of Antmura|安特穆拉安魂曲号
Raksha|拉克萨号
Rise of the Three Suns|三日同辉号
Son of Victory|胜利之子号
Blood of Cthonia|科索尼亚之血号
Cthonian Scion|科索尼亚之裔号
Akhaten|艾卡坦
Cthonian Wolf|科索尼亚之狼
Falkus Kibre|法库斯·凯博
Kalus Ekaddon|卡鲁斯·埃卡顿
Horus Aximand|荷鲁斯·阿西曼德
Tarik Torgaddon|塔里克·托加顿
Garviel Loken|加维尔·洛肯
Maloghurst|马洛赫斯特
Maral Lupus|马拉尔·卢普斯
Vheren Ashurhaddon|维伦·阿舒哈顿
Iacton Qruze|亚克顿·克鲁兹
Tybalt Marr|提伯特·玛尔
Shadrak Meduson|沙德拉克·梅杜森
Urlakk Urg|乌尔拉克·乌尔格
Eugen Temba|欧根·坦巴
Duraga Kal Esmejhak|杜拉加·卡尔·埃斯梅哈克
Vaithan Reaver Squad|韦特罕掠夺者小队
Skyrar's Dark Wolves|斯卡拉的暗狼
Interex|英特雷斯
Davin|戴文
Molech|摩洛
Gorro|戈罗
Ullanor|乌兰诺
Xenobia|芝诺比亚
Auretian Technocracy|奥瑞提亚科技联盟
Xibana Reaches|希巴纳边域
Saturnine Gate|土星之门'''
for line in termtext.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0554','统一本篇名称；舰名、部队及人名不因同形词而跨语境替换。'])))
# Remove an unattested expansion: only the actual supplied English form is catalogued.
by.pop('order of the serpent',None)
with (P/'terms.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=json.loads((P/'reviewed.json').read_text());rv=sorted(set(rv)|{554});(P/'reviewed.json').write_text(json.dumps(rv))
(P/'partial_progress.json').write_text(json.dumps({'article':554,'read_through_block':399,'complete':True},ensure_ascii=False,indent=2))
print('554 complete',len(e),'edits total')
