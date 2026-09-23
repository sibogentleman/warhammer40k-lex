from save_review import save
save(1279,{2:'地狱火手枪是工匠以古老而高度专门化的技术制造的手枪型热熔武器，几乎无法仿制，使用也极少：一个星区中可能总共只有寥寥数把。',4:'Inferno Pistol 地狱火手枪',7:'拥有地狱火手枪是地位的象征，通常只有权势显赫的人才有资格持有。异端审判庭和修女会中地位最特殊的成员，可以获准使用这种珍贵武器。',9:'Inferno Pistol of Inquisitor Malich, hand-crafted by Master Artificer Ernst Heckler in M38 审判官马里奇的地狱火手枪，由工匠大师恩斯特·赫克勒于M38手工打造',11:'圣血天使使用一种名为炼狱手枪的改型，是战团珍藏的遗物，可追溯至黑暗科技时代。著名使用者包括圣血天使指挥官但丁，他的佩枪名为“毁灭手枪”。',13:'Blood Angels Inferno Pistol 圣血天使地狱火手枪',17:'Mars-pattern Inferno Pistol 火星型地狱火手枪',18:'Notable Inferno Pistols 著名地狱火手枪'},notes={2:'Inferno Pistol沿1276地狱火手枪统一，本篇原题炼狱手枪保留对照；Infernus Pistol在本文作为圣血天使改型另译炼狱手枪。',11:'本段古老改型的年代照英文保留，不与正文其他工匠制造说法强行合并。'},terms=[('Inferno Pistol','地狱火手枪'),('Infernus Pistol','炼狱手枪'),('Inquisitor Malich','审判官马里奇'),('Ernst Heckler','恩斯特·赫克勒'),('Conflagration Infernus Pistol','爆燃炼狱手枪'),('Fyrestorm','火焰风暴'),('Ignis Judicium','烈焰审判')],title='地狱火手枪 Inferno Pistol')
save(1280,{2:'多管热熔是带有多根发射管的重型热熔枪。',7:'多管热熔是威力凶猛的帝国反坦克武器，射程长于单兵热熔枪，但仍短于其他重型武器。不同资料对其开火表现的描述有所不同：有的称它伴随炫目闪光射出光束，有的则说它只投射出近乎不可见的强烈热流。目标会被直接熔毁，生物化为灰烬，载具变成扭曲的熔浆。单兵护甲甚至无法提供丝毫防护。',11:'由于体积庞大，多管热熔通常安装在载具上。黎曼鲁斯破坏者可在侧炮座安装，十字军型兰德掠袭者则在车体上安装，均契合两者近距离作战的火力配置。献祭者可配用双联多管热熔，兰德速攻艇及其改型、攻击摩托、豪猪战车和无畏机甲也会使用。',15:'一些配备动力装甲的部队，尤其是星际战士和战斗修女，会携行使用多管热熔；他们同时还必须携带武器所需的燃料和能源。',22:'太阳军型——星际战士在大远征和荷鲁斯之乱期间使用。规格记为“23-20 Mega-thule”，用于攻城突击及死亡区域作战。',26:'普罗透斯型——大远征和荷鲁斯之乱期间使用。',30:'Mk.XI 热能长矛型——涅克罗蒙达凡萨尔家族使用。',32:'Thermic Lance Mk.XI Pattern Mk.XI 热能长矛型'},notes={22:'原文没有说明Mega-thule参数的量纲，原译擅加“弹匣容量”已删除；23-20照录，不擅改顺序。Zone Mortalis暂译死亡区域，指作战环境术语，非据此认定某个地名。'},terms=[('Multi-melta','多管热熔'),('Firestorm Multi-melta','火焰风暴多管热熔'),('Thermic Lance Mk.XI Pattern','Mk.XI 热能长矛型'),('Zone Mortalis','死亡区域')])
save(1281,{2:'热熔爆破炮是安装在星际战士奎托斯重型坦克上的重型热熔武器，专门用于摧毁敌方载具。'},terms=[('Melta Blast-Gun','热熔爆破炮')])
save(1282,{2:'热熔毁灭炮是安装于星际战士锤击型风暴速攻艇的重型三管热熔武器。',4:'Melta Destroyer 热熔毁灭炮'},terms=[('Melta Destroyer','热熔毁灭炮')],title='热熔毁灭炮 Melta Destroyer')
save(1283,{2:'巨型热熔是帝国使用的重型热熔武器，反装甲威力极强。它最初用于太空战中的登舰突击，后来也被装到其他平台上，尤其是火卫二型炼狱掠食者和拳套突击撞击艇。',4:'Magna-Melta on a Deimos Pattern Predator Infernus 火卫二型炼狱掠食者上的巨型热熔'},terms=[('Magna-Melta','巨型热熔')])
from pathlib import Path
import csv,json
p=Path(__file__).parent;f=p/'terms.tsv';r=list(csv.DictReader(f.open(),delimiter='\t'))
for x in r:
 if x['英文标准词']=='Melta Blast-Gun':x['采用中文']='热熔爆破炮';x['编辑说明']='1281明确重型车载武器，与本篇标题统一；1276列表热熔爆破枪回改。'
with f.open('w',newline='') as o:w=csv.DictWriter(o,fieldnames=list(r[0]),delimiter='\t');w.writeheader();w.writerows(r)
f=p/'edits.json';d=json.loads(f.read_text());d['A1276-B0027']='Melta Blast-Gun 热熔爆破炮';f.write_text(json.dumps(d,ensure_ascii=False,indent=2))
