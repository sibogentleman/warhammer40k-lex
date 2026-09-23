from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent;e=json.loads((P/'edits.json').read_text());n=json.loads((P/'notes.json').read_text())
def p(a,k,t):e[f'A{a:04d}-B{k:04d}']=t
p(577,2,'奥克塔琉斯欧克帝国位于极限星域，覆盖几乎与奥特拉玛同样广阔的奥克塔琉斯星区，以同名欧克世界为中心。其统治者采用“奥克塔琉斯暴君”的头衔。')
p(577,6,'旧都：奥克塔琉斯')
p(577,10,'最高统治者：奥克塔琉斯暴君')
p(577,12,'统治阶层：战争头目')
p(577,14,'主要信仰：搞哥与毛哥')
p(577,23,'奥克塔瑞亚——帝国的核心世界；虫群领主杀死暴君后，由利维坦虫巢舰队攻陷')
p(577,25,'奥罗克／奥鲁克——遭利维坦虫巢舰队吞噬')
p(577,27,'乌尔穆克——废料港，遭利维坦虫巢舰队吞噬')
p(577,29,'哒咔佐特——大部分已遭利维坦吞噬')
p(577,31,'坏史古格——大部分已遭利维坦吞噬')
p(577,33,'戈拉勒——遭利维坦吞噬')
p(577,35,'德拉贡——利维坦吞噬戈拉勒后，又将其吞噬')
p(577,37,'凯尔托——利维坦吞噬戈拉勒后，又将其吞噬')
p(577,38,"Janding's Reach 詹丁疆域")
p(577,39,'Gryga XIII 格里加十三号')
p(577,47,'古贝利亚——曾遭基因窃取者侵染')
p(577,50,'克莱达克——遭利维坦虫巢舰队入侵')
p(577,54,'第41千年末，审判官克里普特曼将利维坦虫巢舰队的一部分，引向奥克塔琉斯欧克帝国。由此爆发的战争，让泰伦与欧克都付出惨重代价。在这段早期记述中，胜负尚未分晓。')
p(577,56,'大裂隙形成后，恐虐军队侵入奥克塔琉斯星区，战事演变为三方混战。虫群领主随后全面进攻，将矛头直指首都奥克塔瑞亚。经过长期战役，它亲自杀死暴君，整个首都世界随之遭吞噬。此后，欧克帝国分崩离析，多位军阀争夺新暴君之位。')
p(578,2,'战争头目居于大型欧克 Waaagh!的顶端，通常是所属群体中块头最大、力量最强、最狡猾的个体，享用最好的护甲、武器与装备。')
p(578,6,'战争头目作风专横，身高常超过九英尺（约2.7米），在同族中十分醒目。通常，战绩越辉煌，体型也越庞大。')
p(578,9,'战争头目常亲率部落作战，自身也是不可小觑的战力。身旁通常跟着一群强蛮人保镖、搬运弹药的屁精，以及作为战宠的攻击史古格，令他更加难以对付。')
p(578,11,'头目战死后，部落中最大的强蛮人通常会接替，但须先以暴力镇服同族、恢复秩序，才能坐稳位置。非战斗时期，潜在继承者有时间通过决斗与挑战分出胜负，这套方式还算有效；可若在战场上爆发争位内斗，原头目维系的部落联军便可能顷刻失去凝聚力。杀死头目后迅速反击，确曾击退许多欧克入侵，但绝非百试百灵的制胜手段。')
p(578,14,'战争头目依其在欧克社会中的身份，可能采用不同称号：')
p(578,16,'极速怪胎的首领称“极速头目”')
p(578,18,'技师小子的首领称“技师头目”')
p(578,26,'野猪头目——骑战猪作战的蛮荒野猪小子首领')
p(578,28,'兽霸的战争头目称为“野兽头目”，以最辉煌猎杀留下的战利品装饰自己。他们身先士卒，专挑最大、最凶暴的猎物，以利爪将其撕倒。这些壮硕头目肌肉虬结、伤疤累累，脾气恶劣，或奔跑冲锋，或骑着跳跳恐龙投入战场。')
p(578,31,'格外强悍、战绩显赫的战争头目，被称为“军阀”或“大头目”。一个个部落归附其麾下，集成庞大联军。其中最著名的是碎骨者·斯拉卡，几乎所有欧克都敬畏他——至少够聪明的都知道应该如此。')
p(578,33,'Mega Armored Warboss 超重型护甲战争头目')
p(578,35,'最强大的战争头目，也可能自取独一无二、足够威风的称号，例如查拉顿的“头号纵火狂”。')
p(578,38,'战争头目能使用种类繁多的装备，常见搭配却大致相近。无论如何，武器必须足够强悍，才能在小子们面前稳固地位。作为块头最大、最凶狠的欧克，他总能分得最好的战利品，获得技师小子能造出的最佳装备。上前线时，头目常乘战斗堡垒或骑战斗摩托。')
p(578,44,'嵌合武器——通常将大枪与火箭发射器或喷火器组合')
p(578,45,'Kustom Shoota 改装大枪')
p(578,53,'Mega Armour 超重型护甲')
p(578,57,'Ghazghkull Mag Uruk Thraka 碎骨者·斯拉卡')
p(578,74,'莫兹罗格·斯夸格巴德——兽霸中的野兽头目')
p(578,77,'Notable Past Warbosses 著名前代战争头目')
p(578,83,'野兽——险些征服银河')
n.update({'A0577-B0002':'takes the title为采用头衔，不是头衔被夺走；本篇首段/首都表用Octarius，世界列表与后段用Octaria，保留英文差别及对应译名。','A0577-B0014':'Gork和Mork为神祇，不是宗教组织，原表头religious body不合实际所列内容，按主要信仰表述。','A0577-B0038':'Reach在星际地名语境不是河段，暂定疆域。','A0577-B0054':'尚未分出胜负是旧段落的资料时点；后段已记首都覆灭，用早期记述衔接，避免同页现在时自相矛盾。','A0578-B0006':'九英尺约2.743米；原括注3米粗略，现规范为约2.7米，不改变英文阈值。','A0578-B0011':'统一Warboss战争头目，原战斗头目为混写；Nobz采用强蛮人。','A0578-B0028':'meanest指凶悍，不是道德卑鄙；Squigosaur词根取GW09第30/GW10第29“骑跳跳恐龙的野兽头目”对应，通称标参考。','A0578-B0038':'原英文wide array与little variation表面矛盾，按装备种类多而常见组合近似理解；没有额外补出全新的装备限制。','A0578-B0045':'Kustom只是改装，不含原译重型；Kombi组合武器暂沿本稿嵌合武器，等待专项武器条目统核。','A0578-B0074':'英文Mozgrod与已核Mozrog为同篇上下文中的异拼，采用同一官译，不另造新人物。','A0578-B0083':'conquer为征服，非实现政治统一。'})
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));cols=list(rows[0]);by={r[cols[0]].casefold():r for r in rows}
pairs='''Ork Empire of Octarius|奥克塔琉斯欧克帝国
Orrok|奥罗克
Orruk|奥鲁克
Urmuk|乌尔穆克
Junka-Port|废料港
Dakkazot|哒咔佐特
Badsquig|坏史古格
Ghorala|戈拉勒
Derragon|德拉贡
Keltor|凯尔托
Janding’s Reach|詹丁疆域
Gryga XIII|格里加十三号
Deffspin|死旋星
Rujikar|鲁吉卡尔
Thedna VII|瑟德纳七号
Darkmont|达克蒙特
Phundil|方迪尔
Derenden II|德兰登二号
Ghubelia|古贝利亚
Fendatha|芬达塔
Kraidak|克莱达克
Veloria|维洛里亚
Speedboss|极速头目
Mekboss|技师头目
Flyboss|飞空头目
Kaptin|船长（欧克称号）
Boarboss|野猪头目
Attack Squig|攻击史古格
Kombi-Weapon|嵌合武器
Kustom Shoota|改装大枪
Twin-linked Shoota|双联大枪
Slugga|欧克手枪
Stikkbombz|棍子炸弹
Choppa|砍刀
Big Choppa|大砍刀
Power Klaw|动力爪
Mega Armour|超重型护甲
Cybork Body|赛博躯体
Bosspole|头目之旗
Forsarr|弗萨尔'''
for line in pairs.splitlines():
 en,zh=line.split('|');by.setdefault(en.casefold(),dict(zip(cols,[en,zh,'暂定·官方待核','所给英文底稿','篇0577—0578','所给英文专名，欧克方言拼写与普通英语区分，原文矛盾见校注。'])))
u9='https://assets.warhammer-community.com/chi_06-05_wh40k_core%26key_munitorum_field_manual-5mrlucr2t1-fkybzzzoce.pdf';u10='https://assets.warhammer-community.com/eng_warhammer40000_munitorum_field_manual_march_2025-cims9ya3sg-s8j9m2haae.pdf'
for en,zh in [('Beastboss','野兽头目'),('Beastboss on Squigosaur','骑跳跳恐龙的野兽头目'),('Painboss','痛苦头目'),('Warboss in Mega Armour','超重型护甲战争头目')]:by[en.casefold()]=dict(zip(cols,[en,zh,'官方已核对',f'GW-09 {u9}；GW-10 {u10}','GW09第30页；GW10第29页','直接核对官方完整单位名。']))
by['squigosaur']=dict(zip(cols,['Squigosaur','跳跳恐龙','官方词根参考·通称待核',f'GW-09 {u9}；GW-10 {u10}','GW09第30页；GW10第29页','取Beastboss on Squigosaur完整单位词根，非将所有Squig都改名。']))
by['the swarmlord']=dict(zip(cols,['The Swarmlord','虫群领主','官方已核对',f'GW-09 {u9}；GW-10 {u10}','GW09第37页；GW10第36页','直接核对官方完整单位名。']))
with (P/'terms.tsv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(by.values())
for fn,obj in [('edits.json',e),('notes.json',n)]:(P/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
rv=set(json.loads((P/'reviewed.json').read_text()))|{577,578};(P/'reviewed.json').write_text(json.dumps(sorted(rv)))
(P/'partial_progress.json').write_text(json.dumps({'article':578,'read_through_block':83,'complete':True},ensure_ascii=False,indent=2))
print('551-578 complete')
