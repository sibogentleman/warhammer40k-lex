from pathlib import Path
import csv
P=Path(__file__).resolve().parent;rows=list(csv.DictReader((P/'terms.tsv').open(),delimiter='\t'));h=list(rows[0]);d={r['英文标准词'].casefold():r for r in rows}
for s in '''Plasma Exterminator|等离子灭绝枪
Phobos Armour|恐惧型护甲
Phobos Strike Team|恐惧打击小队
Omni-Scrambler|全频扰频器
Marksman Bolt Carbine|射手型爆矢卡宾枪
Saboteur|破坏专家
Occulus Bolt Carbine|全知者爆矢卡宾枪
Divinator-class Auspex|占卜师级鸟卜仪
Haywire Mine|紊乱地雷
Executioner rounds|处刑者弹
Omnis Pattern Power Armour|全知型动力甲
Accelerator Autocannon|加速自动炮
Scout Sergeant|侦察兵军士
Scout Heavy Gunner|侦察兵重炮手
Scout Hunter|侦察兵猎手
Scout Sniper|侦察兵狙击手
Scout Tracker|侦察兵追踪者
Scout Warrior|侦察兵战士
Scout Squad Kill Team|侦察兵杀戮小队
Terror Scout|恐怖侦察兵
Scout Armour|侦察护甲
Primaris Outrider|原铸摩托警卫
Centurion Warsuit|百夫长战甲
Devastator Centurion|破坏者百夫长
Suppression Force|压制部队
Jagrvelj Skyhammer|贾格维利·天锤
Storm Ravens|风暴渡鸦
Armoured Spearhead|装甲矛头编队
Line Breaker Squadron|破阵者中队
Automated Defence Force|自动防御部队
Tarantula Sentry Gun|狼蛛哨戒炮
Strike Force Nerva|涅尔瓦打击部队
Taros Intervention Force|塔罗斯干预部队
Deathstorm Strike Force|死亡风暴打击部队
Skyhammer Orbital Strike Force|天锤轨道打击部队'''.splitlines():
 en,zh=s.split('|');d[en.casefold()]=dict(zip(h,[en,zh,'暂定·官方待核','所给英文底稿','篇 0298—0315','按所给英文语境统一，待核官方直接对应。']))
for en,zh,cp,ep in [('Centurion Assault Squad','百夫长突击小队',32,31),('Centurion Devastator Squad','百夫长破坏者小队',32,31),('Vindicator','维护者战车',33,32),('Predator Annihilator','歼灭者型掠食者战车',33,32),('Predator Destructor','破坏者型掠食者战车',33,32),('Whirlwind','旋风战车',33,32)]:
 d[en.casefold()]=dict(zip(h,[en,zh,'官方已核对','GW-09；GW-10',f'GW-09 中文{cp}页；GW-10 英文{ep}页','中英文同名单位对应核对。']))
d['phobos armour']['编辑说明']='采用官方角色装备名中的恐惧型护甲（GW-09中文32页／GW-10英文31页）；不用于同名卫星。'
d['primaris outrider']['编辑说明']='由已核官译 Outrider Squad 摩托警卫小队对应到个体；原稿先遣者，单独个体名仍标暂定。'
d['apocrypha of skaros']['采用中文']='斯卡罗斯次经'
with (P/'terms.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=h,delimiter='\t');w.writeheader();w.writerows(d.values())
print(len(d),'root terms')
