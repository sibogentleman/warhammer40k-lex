from save import save,P,replacements
import json
raw='''Dregrokk|德雷格罗克|欧克要塞世界，另拼 Dreggrok。
Unhallowed|渎圣号|噩兆方舟。
Legio Vulturum|秃鹫军团|泰坦军团；原秃鹰／秃鹫并存，统一后者。
Torpedo Drone|鱼雷无人机|联络用途无人机沿原稿。
Asmor Bleakverse|阿斯莫尔·荒凉之诗|怀言者人物名沿原稿。
Perplexing Weave|迷乱织网|千子战帮，原困惑编织不自然。
Temporary Air Base Zephyr33|西风 33 临时空军基地|编号原英文保留。
Ob’lotai|奥博’罗泰|沿原稿钛族人物名。
Great Star Dais|巨星平台|阿尔萨斯·摩洛克古代建筑。
Star Dais Exclusion Zone|星台禁入区|围绕平台建立的防御区域。
Haggard Tower|憔悴之塔|沿原稿战场专名，含义待核。
Commander Bravestorm|指挥官勇暴|沿原稿人物名。
Bleak Missive|凄冷信函号|剑级护卫舰，missive 信函，原使命误认 mission。
Tholonius|托洛尼乌斯|死亡守望守望连长。
Cachecis|卡切西斯|镜面领主伪装使用的典记员身份。
Looking Glass|镜子|阿尔法军团叛乱触发暗号，原中文漏译。
The Eight (Farsight)|八人组|远见亲随群体，固定名称不随实际幸存人数变化；区别黄衣之王八人众。
Da Suparig|超级大车号|欧克夺得方舟后的新名，原超大环误认 rig/ring。
Idolatros System|盲信星系|沿原稿地名，非仅宗教概念。
Netherworld Blade|冥界之刃号|噩兆方舟。
Scrilem System|斯克里莱姆星系|外围星系。
Apostra System|阿波斯特拉星系|外围星系。
Redoubtable|可敬号|戴罪者舰船，沿原稿。
Dark Cathedrum|黑暗大教堂|龙林星要塞。
Warpforge Palace|亚空间铸炉宫殿|原文另拼 Warpforged Palace，同一设施。
Paralaxese|帕拉莱克西斯|恶魔王子。
House Bazhkar|巴兹卡尔家族|混沌骑士家族。
Ouroboros (Caliban engine)|衔尾蛇|与图丘查、瘟疫之心并列的引擎；区别567同形专名。
Plagueheart|瘟疫之心|古代引擎，沿原稿。
Dissonance Engine|不协引擎|由三台古代引擎构成的装置。
Golden Host (Blood Angels)|黄金大军|但丁率领的圣血天使部队，非509同名恶魔军势。
Urghab’laxx|乌尔加布’拉克斯|拦阻撤离的大不净者。
Effacers of Medrengard|梅林德加德抹除者|钢铁勇士战帮。
Barbican Lords|碉楼领主|钢铁勇士战帮。
Ferrocratic Creed|铁权信条|钢铁勇士战帮。
Fire Riders|火焰骑士|吞世者战帮，沿原稿。
Riven Reforged|分裂重铸|叛军组织名暂沿现稿。
Legio Krytos|柯伊托斯军团|泰坦军团名沿原稿。
Legio Rorgahl|罗加尔军团|泰坦军团名沿原稿。
House Akumara|阿库马拉家族|混沌骑士家族。
Grymzags Lootas|格里姆扎格的蛮人拾荒者|官译 Lootas 词根参考，完整部队名暂定。'''
known={l.split('\t')[0].casefold() for l in ((P.parent.parent/'核心术语定译.tsv').read_text()+'\n'+(P/'terms.tsv').read_text()).splitlines()}
rows=[]
for l in raw.splitlines():
 en,zh,note=l.split('|')
 if en.casefold() in known:continue
 known.add(en.casefold());rows.append('\t'.join([en,zh,'暂定·官方待核','所给英文底稿；逐段核读并比对核心词根','篇0843',note]))
with (P/'terms.tsv').open('a') as f:f.write('\n'.join(rows)+'\n')
save({},[843]);replacements([805],{'腓尼基人':'紫庭凤凰'})
f=P/'terms.tsv';t=f.read_text().replace('The Phoenician\t腓尼基人','The Phoenician\t紫庭凤凰');f.write_text(t)
f=P/'notes.json';n=json.loads(f.read_text());key='A0805-B0071';n[key]=n.get(key,'')+' 福格瑞姆称号 The Phoenician 按主审第640篇统一紫庭凤凰，原稿别名腓尼基人保留对照。';f.write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
print('843 complete; new terms',len(rows),'; 805 Phoenician aligned')
