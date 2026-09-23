from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;D=P.parents[1];a=json.loads((D/'全书分段底稿.json').read_text());B={b['id']:b for x in a for b in x['blocks']}
e=json.loads((P/'edits.json').read_text());notes=json.loads((P/'notes.json').read_text());titles=json.loads((P/'titles.json').read_text());review=json.loads((P/'reviewed.json').read_text())
def p(n,k,t):e[f'A{n:04d}-B{k:04d}']=t
def m(n,k,t):
 bid=f'A{n:04d}-B{k:04d}';s=B[bid]['text'];hit=re.search('[\u3400-\u9fff]',s);e[bid]=s[:hit.start()]+t
p(253,2,'先锋智库员是原铸星际战士中的灵能者，精于遮蔽踪迹与隐秘行动，使战斗兄弟能够趁敌人最不防备之时发动攻击。他们有时也亲自率领先锋星际战士突击部队作战。')
m(253,4,'先锋智库员')
p(253,6,'被选入先锋部队的智库员，掌握独特的战斗灵能技巧，能够掩藏战友的行踪，并以幻象与幻觉误导对手。他们把灵能塑成暗影斗篷般的屏障，环绕自身，引导战斗兄弟穿过敌境抵达目标，让警惕的敌人也生不出一丝疑心。他们还穿着带兜帽的迷彩斗篷，隐藏自己的身份，以及所能施展的强大灵能力量。')
p(254,2,'星语官是星际战士智库员的第三级职衔，主要担任战场内外的首席通信官。他们能够把心智投射到亚空间中，其方式类似星语庭的星语者，却不必接受后者必须经历的痛苦魂缚仪式。更常见的用途，是在较短距离内传递信息，协调进攻与作战命令。')
p(254,31,'格劳西斯·泰洛迈恩——灰骑士。')
p(255,2,'典记员是星际战士智库员的第二级职衔。')
p(255,4,'他们负责审核编修员撰写的报告，将其定稿后收入智库档案，并提供战役的战略综述。随着灵能力量和驾驭能力提升，典记员可晋升为星语官。')
p(256,2,'编修员是星际战士智库员的最低一级职衔，授予刚刚加入智库的成员。他们负责撰写战报，提交战团存档。这些概要记录构成战团历史的一部分，其内容与风格会因编修员的信念、思想或战役本身而有所不同。')
p(256,6,'编修员通常没有灵能兜帽，有时甚至不戴头盔；除了智库员特有的蓝色动力甲，他们的外表与其他战斗兄弟颇为相似。')
p(257,2,'侍僧是星际战士战团中具有灵能天赋的候选人，正在接受成为智库员的训练。')
p(257,4,'他们不仅要熬过成为星际战士所必需的艰苦试炼与植入程序，还必须学会掌控自己的灵能天赋。若不能保护心智、抵御亚空间的恐怖威胁，等待他们的便是落入恶魔魔爪、比死亡更加可怕的命运。')
p(258,2,'圣洁导师又称至高牧师，是阿斯塔特修会战团的牧师首领，也是战团信仰的领袖。作为战团高层之一，他通过向各连指派牧师，维护全团的精神与信仰状态。其下一级是隐修长，负责主管隐修圣殿。')
p(258,12,'贾戈林——风暴之音，白疤。')
p(258,28,'姓名不详——亡者代言人领主，处刑者。')
notes.update({'A0254-B0002':'Epistolary 采用暂定职衔“星语官”，与 Astropath（星语者）区分；third rank 为等级，不是第三梯队编制。','A0258-B0002':'Adeptus Astartes 是阿斯塔特修会，不是《阿斯塔特圣典》；Chapter Cult 指战团信仰体系，Reclusiam 为供奉与仪式场所，此处暂译隐修圣殿。','A0258-B0028':'Lord Speaker of the Dead 是职衔，暂作说明性译名“亡者代言人领主”；原译“代死领主”易误解为代替他人赴死。'})
titles['253']='先锋智库员 Vanguard Librarian'
review=sorted(set(review)|set(range(253,259)))
for name,obj in [('edits.json',e),('notes.json',notes),('titles.json',titles),('reviewed.json',review)]:(P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
print('Reviewed through258',len(e),'cumulative edits')
