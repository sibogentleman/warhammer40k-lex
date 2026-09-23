# coding:utf-8
from save import *
rows='''Liber Malefact|《邪恶典籍》|预言文献，沿原稿。
Urkanthos / Urkrathos|乌尔坎托斯|同一恐虐亲选，名单/叙事不同拼写；原正文厄奎索斯，与主审同意统一。
Logistar-General|后勤总监|后勤职衔，General不按普通将军军衔机械译。
Conskavan Raik|康斯卡万·莱克|后勤总监，沿原稿人名。
Marus Porelska|马鲁斯·珀勒斯卡|卡迪亚首席总督。
Audaria Zabine|奥达利亚·扎比内|最高政委。
Kozchokan|科兹乔坎|海军大将。
Quarren|夸伦|海军上将。
Dostov|陀思妥夫|海军上将。
Minzet|明泽特|海军上将。
Venesca Catallia|韦涅斯卡·卡塔莉亚|海军上将。
Attica|阿提卡|领主元帅。
Talia Daverna|塔莉娅·达韦尔纳|审判官。
Katarinya Greyfax|卡塔琳娅·格雷法克斯|沿原稿全名；官方Inquisitor Greyfax核对仅支持姓氏及职衔。
Vardus|瓦杜斯|渡鸦家族女男爵。
Devram Korda|德夫拉姆·科尔达|沿原稿。
Ygethmor the Deceiver|欺诈者伊戈瑟默|角色称号，区别星神欺诈者。
Zagthean the Broken|破灭者札格辛|沿原稿。
Druxus Bale|德鲁克斯·贝尔|沿原稿。
Krom Gat|克罗姆·盖特|钢铁勇士指挥官。
Kossolax the Foresworn|背誓者科索拉克斯|沿核心词根。
Tarraq Darkblood|塔拉克·暗血|午夜领主。
Kranon the Relentless|无情者克拉能|沿核心克拉能词根。
Varan the Undefeatable|无敌者瓦兰|战帅。
Plagueclaw|瘟疫之爪号|舰船。
Urthwart|乌尔斯勒|恶魔世界及星系，原星系另译厄斯里奇，统一同词根。
Frenerax Dust Cloud|弗兰尼莱克斯尘埃云|星际区域。
Plague of Unbelief|无信瘟疫|沿原稿事件名，非一般不信教。
Lelithar|莱利瑟|統一同章莱利萨。
Voice of the Emperor|帝皇之声|此篇邪教首领自称，不当作事实上的帝皇代言。
Kasr Tyrok / Tyrok Fields|提洛克堡／提洛克原野|堡城与外围场地区分。
Volscani Cataphracts|沃斯卡尼铁骑|沿原稿部队名，不据名称假设均为骑兵。
Pulaski|普拉斯基|海军上将，不能替换为同段夸伦。
Ormantep|奥尔曼泰普|星系。
Solar Mariatus|索拉·玛丽亚图斯|卡迪亚星系行星。
St. Josmane’s Hope|圣若斯曼之希望|监狱世界。
Thybault Helican XXIII|蒂博·赫利肯二十三世|领主。
Lord Judiciary|司法领主|法务部职衔；原文Lord Jiudiciary疑误拼，非人名朱迪卡里。
Scelus|斯凯鲁斯|区别Scarus斯卡鲁斯。
Khajog Khan|哈乔格可汗|白疤指挥官。
Green Krusade|绿色远征|欧克战役名。
Cruxis Crusade|克鲁西斯远征|黑色圣堂远征军。
Might of the Faithful|忠实力量号|帝皇级战列舰，沿原稿名。
Will of Eternity|永恒意志号|黑石堡垒。
Eleanor|埃莉诺|殉教圣女修会大修女。
Genevieve|吉纳维芙|殉教圣女修会大修女。
Klarn|克拉恩|机械教贤者。
Artesia|阿特西亚|恶魔魔宠。
Cacadius Siron|卡卡迪乌斯·西隆|阿巴顿情报主管。
Morkath|莫卡斯|阿巴顿的造物及养女称谓，身份限于原文。
Ruis Tracinto|鲁伊斯·特拉辛托|绯红之拳军官。
Jarran Kell|贾兰·凯尔|克里德旗手。
Cerantes|卡兰提斯|荷鲁斯之乱时代极限战士副指挥官。
Extremis Protocols|极端协议|禁止卡迪亚撤离的审判庭协议，沿原稿。
Null-Array|反灵能阵列|卡迪亚方尖碑相关装置，区别虚空盾。
Tesseract Labyrinth|超立方体迷宫|太空死灵囚禁装置，沿原稿。
Shadowlight|暗影之光|佩利亚异形遗物。
Amberley Vail|安伯利·维尔|审判官，沿原稿。
Chaeronia|喀罗尼亚|黑暗机械修会铸造世界。
Xorphas|索法斯|黑色军团巫师。
Battle of Vorlese|沃勒斯之战|沿原稿。
Basilica of St. Lysias|圣莱西亚斯大教堂|沿原稿。
Boros Gate|博罗斯之门|沿原稿。
Mendox Cataclysm|门多克斯大灾变|沿原稿。'''
with (P/'terms.tsv').open('a') as f:
 for row in rows.splitlines():
  eng,zh,why=row.split('|');f.write('\t'.join([eng,zh,'暂定·官方待核','所给英文底稿','篇0829',why])+'\n')
