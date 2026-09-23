# coding: utf-8
from save import save,replacements,P
import json
save({
'A0362-B0551':'以星际战士战团的标准衡量，太空野狼舰队规模异常庞大，拥有一百余艘舰船。某一时期的记录列出以下兵力：',
'A0362-B0553':'八艘战斗驳船。',
'A0362-B0555':'三十余艘打击巡洋舰。',
'A0362-B0557':'二十余个猎手级驱逐舰中队。',
'A0362-B0559':'二十余个短剑级与新星级护卫舰中队。',
'A0362-B0561':'两座拉米雷斯级星堡：血腥贵族与雷神之锤。',
'A0362-B0565':'Heresy Era 荷鲁斯之乱时期',
'A0362-B0567':'赫拉芬克尔号——荣光女王级战列舰，黎曼·鲁斯的旗舰。',
'A0362-B0570':'全父荣光号——战斗驳船，战团现任旗舰。',
'A0362-B0573':'除通常的星际战士载具外，太空野狼军械库还保有一些黎曼鲁斯灭绝者坦克，以纪念原体。他们很少动用这些战车，但每逢出战都会造成毁灭性打击；星际战士乘员精湛的技艺，更使战车原本就可怕的武装发挥出惊人威力。',
'A0362-B0576':'芬里斯之火号——救赎者型兰德掠袭者战车，曾参加阿伦海姆的七倍之城争夺战，以及芬里斯星系围攻战。',
'A0362-B0578':'血腥匕首号——拳套突击艇。',
'A0362-B0580':'赫尔姆加特号——风暴鸟。',
'A0362-B0582':'莫凯号——战团的第四架飞行器，曾参加米堤亚 841 之战。',
'A0362-B0584':'沃尔特号——兰德掠袭者战车。',
'A0362-B0586':'Heresy Era 荷鲁斯之乱时期',
'A0362-B0598':'乔林·血嚎——第十三大连（Dekk-Tra）首领。',
'A0362-B0600':'布拉维耶——第十三大连（Dekk-Tra）首领，曾任乔林·血嚎麾下的王室护卫。',
'A0362-B0616':'凯加尔·冷血——狼主。',
'A0362-B0629':'阿贾克·石拳——人形巨山、芬里斯之砧，野狼卫队成员。成为太空野狼前，他是熊爪部落的铁匠，后来升为洛根·格里姆纳尔的贴身冠军。',
'A0362-B0633':'阿斯格·战拳——野兽之战时期的狼主。',
'A0362-B0644':'Leifvar Twice-Slain — Wolf Guard.',
'A0362-B0645':'莱夫瓦尔·二逝——野狼卫队成员。',
'A0362-B0651':'不屈的莫基尔——头狼大连的神圣无畏机甲。',
'A0362-B0653':'风暴召唤者纳吉奥——符文牧师。',
'A0362-B0655':'杀戮牙——无畏机甲。',
'A0362-B0663':'杀戮者乌尔里克——狼牧师。',
'A0362-B0665':'哈尔·灰色编织者——死亡守望钢铁牧师及铸造大师。'
},notes={'A0362-B0561':'Goremenjarl、Mjalnar 是星堡专名，“血腥贵族”“雷神之锤”沿用现稿，未查得官方汉译；后者不因词形相近便宣称与现实神话 Mjölnir 完全同名。','A0362-B0573':'Leman Russ Exterminator 对应官方“黎曼鲁斯灭绝者”；原“根除者”实际对应另一型号 Eradicator。','A0362-B0600':'previously Huscarl to Jorin Bloodhowl 表示曾为乔林麾下护卫，而不是乔林的前任首领，原译颠倒了从属关系。','A0362-B0602':'Geigor Fell-Hand 暂沿用“戈果·邪手”；Fell-Hand 与 Bjorn the Fell-Handed 为不同人物称号，不直接借用断手比约恩的官译合并二人。','A0362-B0651':'Venerable Dreadnought 泛称统一“神圣无畏机甲”，参考完整单位 Space Wolves Venerable Dreadnought 的官方词根；通称仍标待核，避免同书出现神圣/尊者两套。'})
# An English block must remain untouched: discard the redundant preservation entry above.
e=json.loads((P/'edits.json').read_text());e.pop('A0362-B0644',None);(P/'edits.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
replacements([362],{'罗根·格里姆纳尔':'洛根·格里姆纳尔','罗伯特·基里曼':'罗保特·基里曼','尼加尔·风暴呼唤者':'风暴召唤者纳吉奥','荷鲁斯叛乱':'荷鲁斯之乱','普罗斯佩罗':'普洛斯佩罗','普罗斯彼罗':'普洛斯佩罗','灰猎':'灰色猎手','阿米吉多顿':'阿玛吉多顿','野狼侦察兵':'狼侦查','野狼侦查摩托':'狼侦查摩托','约林·血嚎':'乔林·血嚎','莱昂·艾尔庄森':'莱昂·艾尔’庄森'})
save({},[362])
base='https://assets.warhammer-community.com/'
url=base+'chi_06-05_wh40k_core%26key_munitorum_field_manual-5mrlucr2t1-fkybzzzoce.pdf ; '+base+'eng_warhammer40000_munitorum_field_manual_march_2025-cims9ya3sg-s8j9m2haae.pdf'
with (P/'terms.tsv').open('a') as f:
 for en,zh,page,note in [('Blood Claws','血爪','GW09第34页／GW10第33页','同名单位对照'),('Fenrisian Wolves','芬里斯狼','GW09第34页／GW10第33页','同名单位对照'),('Thunderwolf Cavalry','雷狼骑兵','GW09第34页／GW10第33页','同名单位对照'),('Murderfang','杀戮牙','GW09第34页／GW10第33页','同名单位对照；原弑牙'),('Wulfen','狼人','GW09第34页／GW10第33页','同名单位对照'),('Wulfen Dreadnought','狼人无畏机甲','GW09第34页／GW10第33页','同名单位对照'),('Wolf Guard Terminators','野狼守卫终结者','GW09第34页／GW10第33页','同名单位对照；不凭此宣称所有Wolf Guard职衔已有同样直接官译'),('Wolf Scouts','狼侦查','GW09第34页／GW10第33页','保留官方“侦查”写法，不擅改“侦察”'),('Space Wolves Venerable Dreadnought','神圣无畏机甲','GW09第34页／GW10第33页','中文位于太空野狼专页且省去阵营前缀，完整单位对应；其他阵营不自动视作同规则单位'),('Leman Russ Exterminator','黎曼鲁斯灭绝者','GW09／GW10均第8页','与Eradicator根除者严格区分'),('Land Raider Redeemer','救赎者型兰德掠袭者战车','GW09第32页／GW10第31页','同名单位对照'),('Repulsor Executioner','处决者型反重力战车','GW09第33页／GW10第32页','同名单位对照')]: f.write('\t'.join([en,zh,'官方已核对',url,page,note])+'\n')
 f.write('\t'.join(['Venerable Dreadnought','神圣无畏机甲','官方词根参考·通称待核',url,'GW09第34页／GW10第33页；362 B0650','依据太空野狼完整单位词根统一通称；不把不同阵营单位规则合并'])+'\n')
 for en,zh,loc,note in [('Vlka Fenryka','芬里斯之狼','362 B0001','芬里斯语自称，不是芬里斯之子或芬里斯人'),('Masaanore-Core','马萨诺尔核心城','362 B0058','原正教核心城无依据'),('Watch Pack','监视小队','362 B0086','马卡多派往原体身边监督的小队'),("Faith’s Anchorage",'信仰锚地','362 B0183','地名；原信仰安克雷奇'),('War of Beasts','群兽之战','362 B0187','警戒星战事，区别War of the Beast野兽之战'),('Bloodslinker','血潜者','362 B0238','泰伦利卡特个体名；原链血者'),('Reductor','基因提取器','362 B0547','药剂师器械，原还原者'),('The Bloodmaws','血喉','362 B0338','大连名，区别Bran Redmaw伯恩·红喉'),('Gore Dagger','血腥匕首号','362 B0577','载具专名，原戈尔匕首')]:f.write('\t'.join([en,zh,'暂定·官方待核','所给英文底稿',loc,note])+'\n')
