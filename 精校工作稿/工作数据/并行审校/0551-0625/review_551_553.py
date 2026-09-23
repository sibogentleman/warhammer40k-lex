from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent
ed={
'A0551-B0002':'肯特泰密会是大远征与荷鲁斯之乱期间千子军团的一支精锐部队。',
'A0551-B0007':'这些战士隶属豺狼教团，守护普罗斯佩罗的五大学派。肯特泰刀锋战士彼此通过灵能紧密相连；其中的精锐，则得以研习学派内部的秘密与秘术。',
'A0551-B0009':'肯特泰最出众的战士组成一个个刀锋结社，每个结社由一位刀锋大师率领。正如其名，他们的主要武器是成对的灵能剑。',
'A0552-B0002':'阿米塔拉密会是大远征与荷鲁斯之乱期间，千子军团采用的快速攻击部队。',
'A0552-B0004':'Ammitara Occult Symbol 阿米塔拉密会标志',
'A0552-B0006':'这是一个高度隐秘的团体，听命于神秘的盲者教团。阿米塔拉擅长快速突袭、侦察、谍报、刺杀与误导敌人，因此最常配备狙击步枪。最低阶战士称为代祷者，小队指挥官则称为命运者。',
'A0553-B0002':'黑鸦信徒是大远征与荷鲁斯之乱期间，来自千子黑鸦学派的飞行员。他们以神秘的预知感官辅助机载瞄准设备，凭借洞见未来的能力作战。'}
notes={
'A0551-B0009':'Force Swords 为灵能剑，不是 Power Swords 动力剑；cabals 此处指小型结社，不是黑暗灵族的 Kabal 阴谋团，也不是异形组织密教。',
'A0552-B0006':'Intercessor 此处是军团时代阿米塔拉密会的低阶职衔，暂沿用代祷者，不能套用原铸仲裁者单位译名。Fates 暂译命运者；Order of the Blind 暂译盲者教团。',
'A0553-B0002':'eldritch 为神秘的、秘术性的，原译矫正误判词义；并修正大十远征的错字。'}
for name,obj in [('edits.json',ed),('notes.json',notes),('reviewed.json',[551,552,553]),('titles.json',{}),('additions.json',{})]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
with (P/'terms.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['英文标准词','采用中文','译名状态','依据','定位','编辑说明'])
 for en,zh in [('Khenetai Occult','肯特泰密会'),('Order of the Jackal','豺狼教团'),('Ammitara Occult','阿米塔拉密会'),('Order of the Blind','盲者教团'),('Corvidae Initiate','黑鸦信徒'),('Corvidae Cult','黑鸦学派'),('Fates','命运者')]:w.writerow([en,zh,'暂定·官方待核','所给英文底稿','篇 0551—0553','按具体军团语境暂定；同形词不机械替换。'])
print('551-553 complete')
