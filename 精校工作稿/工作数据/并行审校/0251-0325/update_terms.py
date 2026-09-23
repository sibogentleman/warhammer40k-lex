from pathlib import Path
import csv,json,io
P=Path(__file__).resolve().parent
h=['英文标准词','采用中文','译名状态','依据','定位','编辑说明']
rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t')) if (P/'terms.tsv').exists() else []
r={x[h[0]].casefold():x for x in rows}
def add(en,zh,status='暂定·官方待核',src='所给英文底稿',loc='篇 0251—0297',note='按已逐段核读的具体语境统一；同形普通词不自动替换。'):
 r[en.casefold()]=dict(zip(h,[en,zh,status,src,loc,note]))
for line in '''Chief Librarian|首席智库员
Librarium|智库馆
Librarius|智库
Host of Pentacles|五芒天军
Librarius Discipline|智库学派
Technomancy|科技学派
Fulmination|雷霆学派
Geokinesis|控地学派
Vanguard Librarian|先锋智库员
Epistolary|星语官
Codicier|典记员
Lexicanium|编修员
Acolytum|侍僧
Master of Sanctity|圣洁导师
High Chaplain|至高教士
Reclusiarch|隐修长
Reclusiam|隐修圣殿
Lord Speaker of the Dead|亡者代言人领主
Albanactus|阿尔巴纳克托斯
Watch Fortress Furor Shield|狂热之盾守望堡垒
Ivanus Enkomi|伊万努斯·恩科米
Minotaurs|米诺陶
Raneil|雷内尔
Thulsa Kane|塔尔萨·凯恩
Xavier|泽维尔
Rosarius|玫瑰念珠
Crozius Arcanum|教士权杖
Imperial Heralds|帝国先驱
Voices of Fire|火之声
Interrogator-Chaplain|审讯教士
Druids|德鲁伊
Death Speakers|亡者代言人
Iron Father|钢铁圣父
Death Company Chaplain|死亡连队教士
Paternis Sanguis|圣血之父
Absolvor Bolt Pistol|赦免者爆矢手枪
executioner relic blade|处刑圣物大剑
tempormortis|时殁装置
Master of the Forge|铸造大师
Techno-mats|技术工役
Mentors|导师战团
Master of the Rock|巨石之主
Alcoves of Honor|荣誉壁龛
Conversion Beamer|转化光束炮
Mortis Machina|机械之死
Night Swords|夜剑
Machina Opus|机械之作
Cyber-familiars|智控魔宠
lesser haemonculites|小型人造生物
Forge Bolter|铸炉爆矢枪
Omnissian Power Axe|欧姆尼赛亚动力斧
Techmarine Novitiate|见习科技战士
Signum|目标指示器
Chief Apothecary|首席药剂师
Master of the Apothecarion|药剂大师
Apothecarion|药剂部
Aslon Marr|阿斯隆·玛尔
Corbulo|科布罗
Corpus Helix|科尔珀斯·赫利克斯
Dyserna|戴瑟纳
Harath Shen|赫拉斯·沈
Razaek|拉扎克
Narthecium|医疗套件
Carnifex|刽子手
Progenoid glands|基因存收腺
Prime Helix|至高螺旋
Primus Medicae|首席药剂师
Helix Adept|先锋药剂师
Helix Gauntlet|医疗臂铠
Chapter Champion|战团冠军
Company Champion|连队冠军
Curadh|库拉德
Company Ancient|连队旗手
Chapter Ancient|战团旗手
Master of the Watch|守望大师
Master of the Arsenal|军械大师
Master of the Fleet|舰队大师
Master of the Marches|行军大师
Master of the Rites|祭仪大师
Lord Executioner|处刑者领主
Master of Relics|遗物大师
Master of the Recruits|新兵大师
Master of Reconnaissance|侦察大师
Tractoris Servitor|训练机仆
Tractoris Dummies|训练假人
transplasteks|塑胶材料
Command Squad|指挥小队
Nuncio-vox|通讯引导阵列
Pyre Wardens|火葬守卫
Foeseekers|寻敌者
Reclusiam Command Squad|隐修圣殿指挥小队
Reclusiaries|隐修卫士
Tyranthikos|提兰提科斯卫队
Chosen of the Tetrarchy|四方领主的受选者
Unforgiven|戴罪者
Nemesis Force Weapon|复仇女神灵能武器
Terminator Titanhammer Squad|终结者泰坦之锤小队
Dragonfire Bolts|龙火爆矢
Hellfire Rounds|地狱火弹
Kraken Pattern Penetrator Rounds|克拉肯型穿甲弹
Metal Storm Shells|金属风暴弹
Tempest Bolts|暴风爆矢
Vengeance Rounds|复仇弹
Apocrypha of Skaros|斯卡罗斯外典
Gravis Pattern Power Armour|重装型动力甲
Plasma Incinerator|等离子焚化枪
Battlewagon|战斗货车
Vengor Launcher|威格尔发射器
Castellan Launcher|堡主发射器'''.splitlines():
 en,zh=line.split('|');add(en,zh)
for en,zh,cp,ep in [
 ('Chaplain','教士',32,31),('Techmarine','科技战士',33,32),('Judiciar','裁决者',32,31),
 ('Iron Father Feirros','钢铁圣父费洛斯',32,31),('Chaplain Grimaldus','格里玛度斯教士',10,10),('Lemartes','雷马特斯',11,11),('Asmodai','阿斯莫德',17,17),
 ('Iron Priest','钢铁牧师',34,33),('Apothecary','药剂师',32,31),('Apothecary Biologis','生物药剂师',32,31),('Fabius Bile','法比乌斯·拜尔',15,15),('Ancient','旗手',32,31),('Bladeguard Ancient','剑卫旗手',32,31),('Bladeguard Veteran Squad','剑卫老兵小队',32,31),
 ('Sanguinary Guard','圣血守卫',11,11),('Inner Circle Companions','内环近卫',17,17),('Ravenwing Command Squad','鸦翼指挥小队',17,17),('Rhino','犀牛战车',33,32),('Razorback','豪猪战车',33,32),('Darnath Lysander','达纳斯·莱山德',32,31),
 ('Sternguard Veteran Squad','肃卫老兵小队',33,32),('Terminator Assault Squad','终结者突击小队',33,32),('Terminator Squad','终结者小队',33,32),('Devastator Squad','破坏者小队',32,31),('Tactical Squad','战术小队',33,32),('Intercessor Squad','仲裁者小队',32,31),('Infernus Squad','焚狱者小队',32,31),('Hellblaster Squad','地狱轰击者小队',32,31),('Desolation Squad','寂灭小队',32,31),('Aggressor Squad','侵略者小队',32,31),('Eradicator Squad','根除者小队',32,31),('Inceptor Squad','先驱者小队',32,31),('Infiltrator Squad','渗透者小队',32,31),('Incursor Squad','入侵者小队',32,31),('Reiver Squad','掠夺者小队',33,32),('Eliminator Squad','歼灭者小队',32,31),('Suppressor Squad','压制者小队',33,32),('Scout Squad','侦察小队',33,32),('Outrider Squad','摩托警卫小队',32,31),('Drop Pod','空降舱',32,31),('Heavy Intercessor Squad','重装仲裁者小队',32,31),('Assault Intercessor Squad','突击仲裁者小队',32,31),('Grey Hunters','灰色猎手',34,33)]:
 add(en,zh,'官方已核对','GW-09；GW-10',f'GW-09 中文{cp}页；GW-10 英文{ep}页','按官方中英文同名单位表对应核对；不得扩大到仅名称相近的其他单位。')
add('Aethon Shaan','艾索·沙恩','官方已核对','GW-06；https://www.warhammer-community.com/en-gb/articles/8wocrwoc/aethon-shaan-master-of-shadows/','GW-06 人物卡；官网英文人物页','只统一人物姓名，不用新版现职覆盖本书描述的历史职务。')
r['carnifex']['编辑说明']='此处仅指药剂师实施帝皇安宁的医疗器械；同名泰伦生物须按其条目另译，不作全书同形替换。'
r['librarius']['编辑说明']='机构语境为智库；灵能学派语境为智库学派，按语境分开。'
r['iron father']['编辑说明']='参考官译人物全称 Iron Father Feirros／钢铁圣父费洛斯；独立职衔未查得直接中文证据，仍标暂定。'
r['primus medicae']['编辑说明']='军团时代职衔，暂沿用首席药剂师；不与现代战团的 Chief Apothecary 静默合并。'
r['unforgiven']['编辑说明']='参考官方复合名 Unforgiven Task Force／戴罪者特遣队（GW-09/GW-10第17页）；独立称谓仍标暂定。'
r['chief librarian']['编辑说明']='参考 Chief Librarian Mephiston／首席智库员墨菲斯顿（GW-09/GW-10第11页）；官名首席智库狄格里斯保留固定形式。'
with (P/'terms.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=h,delimiter='\t');w.writeheader();w.writerows(r.values())
print(len(r),'term decisions saved')
