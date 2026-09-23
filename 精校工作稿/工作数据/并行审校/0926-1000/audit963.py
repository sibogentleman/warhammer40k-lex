import json,csv,re
from pathlib import Path
ROOT=Path(__file__).parents[2]
src=json.loads((ROOT/'全书分段底稿.json').read_text());bs={b['id']:b for a in src for b in a['blocks']}
folders=['0101-0175','0316-0400','0776-0850','0926-1000']
# These Chinese expressions were verified against their source contexts in this review.
common={'堡垒修道院':'要塞修道院','战团仆役':'战团农奴','火焰枪':'火焰喷射器','圣若斯曼之希望':'圣约斯曼之希望','阿格里皮纳':'阿格里皮娜','图拉真·瓦洛里斯':'图拉真·瓦洛瑞斯','坦波里亚':'坦珀利亚','赤红之马格努斯':'红魔马格努斯','卡塔昌丛林战士':'卡塔昌丛林斗士','卡西萨特拉':'卡西萨特拉号','尼康城':'尼尔康城','尼康之战':'尼尔康之战'}
targeted={
'A0109-B0026':{'暴风忠嗣部队':'风暴忠嗣军','暴风忠嗣':'风暴忠嗣军'},
'A0119-B0130':{'犀牛装甲车':'犀牛战车'},'A0119-B0149':{'犀牛装甲车':'犀牛战车'},
'A0170-B0058':{'瓦尔基里':'女武神炮艇','犀牛、':'犀牛战车、'},
'A0172-B0021':{'禁军卫士':'禁军卫队'},
'A0326-B0182':{'变化灵':'诡变灵'},
'A0384-B0013':{'重甲欧克老大':'重甲欧克强蛮人'},
'A0817-B0009':{'大灭绝':'大剔除'},
'A0828-B0105':{'瓦尔基里运输机':'女武神炮艇'},
'A0829-B0043':{'违背者':'违背者'},
'A0829-B0094':{'瓦尔基里炮艇':'女武神炮艇'},
'A0833-B0047':{'海军瓦尔基里、仇杀飞行中队':'海军的女武神炮艇与仇杀飞行中队'},
'A0834-B0168':{'瓦尔基里飞行中队':'女武神炮艇飞行中队'},
'A0834-B0583':{'腐烂使者':'腐朽使者'},
'A0835-B0060':{'杜鲁卡里':'黑暗灵族'},
'A0935-B0033':{'至尊巫师':'高阶巫师'},
'A0950-B0027':{'违逆者':'违背者'}
}
full={
'A0317-B0033':'荷鲁斯之乱后的二次建军期间，罗格·多恩创建了饮魂者战团，成员主要来自帝国之拳军团残存的舰基突击部队。建团之初，多恩还赠予他们一件最古老、最受尊崇的圣物——灵魂之矛，以昭示战团的使命，也提醒他们：尽管已经分属不同战团，帝国之拳的子嗣仍以共同的精神和兄弟情谊紧密相连。',
'A0137-B0041':'机兵的双臂和背部均可安装武器，并按任务需要迅速更换组合，形成强大火力。型号名称后的三位代码用于标示装备配置，其中大写字母代表重型武器。例如，“铁骑 LBf”的背部装有激光炮，右臂装有重型爆矢枪，左臂则装有火焰喷射器。'
}
termmap={'The Great Cull':'大剔除','Bringers of Decay':'腐朽使者','Khasisatra':'卡西萨特拉号','Temporia':'坦珀利亚','Nyrcon City':'尼尔康城','Violators':'违背者','Chapter Serf':'战团农奴','Chapter Serfs':'战团农奴','Fortress-monastery':'要塞修道院','Fortress-Monastery':'要塞修道院','Valkyrie':'女武神炮艇','Flamer':'火焰喷射器','Nobz':'强蛮人','Exalted Sorcerer':'高阶巫师','Trajann Valoris':'图拉真·瓦洛瑞斯','Catachan Jungle Fighters':'卡塔昌丛林斗士','Magnus the Red':'红魔马格努斯','Tempestus Scions':'风暴忠嗣军'}
audit=[]
for folder in folders:
 d=ROOT/'并行审校'/folder;ed=json.loads((d/'edits.json').read_text());reviewed=set(json.loads((d/'reviewed.json').read_text()))
 for a in src:
  if a['number'] not in reviewed:continue
  last=''
  for b in a['blocks']:
   if b['language']=='en':last=b['text']
   if b['language']!='zh':continue
   old=ed.get(b['id'],b['text']);s=full.get(b['id'],old)
   for x,y in common.items():
    if x=='卡西萨特拉':s=re.sub(x+'(?!号)',y,s)
    else:s=s.replace(x,y)
   if re.search(r'drop.?pods?',last+' '+b['text'],re.I):s=s.replace('空投舱','空降舱')
   if re.search(r'Imperial Army',last,re.I):s=s.replace('帝国陆军','帝国军')
   for x,y in targeted.get(b['id'],{}).items():s=s.replace(x,y)
   if s!=old:ed[b['id']]=s;audit.append({'id':b['id'],'before':old,'after':s})
 (d/'edits.json').write_text(json.dumps(ed,ensure_ascii=False,indent=2)+'\n')
 rows=list(csv.reader((d/'terms.tsv').open(),delimiter='\t'))
 for r in rows:
  if len(r)!=6:raise ValueError((folder,r))
  for x,y in common.items():
   if x=='卡西萨特拉':r[1]=re.sub(x+'(?!号)',y,r[1])
   else:r[1]=r[1].replace(x,y)
  r[1]=termmap.get(r[0],r[1])
  if r[0]=='Khasisatra':r[5]='具名帝国大厦超重型指挥车；与1518同一攻城引擎，带号。'
 with (d/'terms.tsv').open('w') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerows(rows)
 # Only update Chinese parts of existing corrected titles.
 t=json.loads((d/'titles.json').read_text())
 for k,v in t.items():
  for x,y in common.items():
   if x!='卡西萨特拉':v=v.replace(x,y)
  t[k]=v
 (d/'titles.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
 print(folder,'edits',len(ed),'reviewed',len(reviewed))
(Path(__file__).parent/'audit963_changes.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print('changedblocks',len(audit))
