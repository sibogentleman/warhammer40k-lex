from pathlib import Path
import re, json, hashlib, collections, subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/Users/bytedance/Documents/Codex/2026-09-20/https-www-bilibili-com-opus-1117594376438022184/outputs')
CATALOG = json.loads((SOURCE/'战锤40K_LEX专栏条目清单.json').read_text())
ENTRIES = {r['number']:r for r in CATALOG['entries']}
edits, formatting, structure = [], collections.Counter(), []

# Every replacement below was reviewed in its local sentence. Similar-looking
# but valid repetitions (目的的, 可以以, 所有有, 被被称为) are not changed globally.
candidate_ids = [4,9,12,19,20,22,23,29,32,33,36,37,38,42,47,54,61,66,70,72,73,87,88,91,101,105,109,124,129,138,144]
candidates = json.loads((ROOT/'reports/校对候选.json').read_text())
rules = []
for idx in candidate_ids:
    row = candidates[idx]
    phrase = row['context']
    # A short window avoids source line breaks while retaining local context.
    pos = phrase.index(row['match'])
    old = phrase[max(0,pos-3):pos+len(row['match'])+3]
    new = old.replace(row['match'], row['match'][0], 1)
    rules.append((row['article'], old, new, '删除误重复字'))

rules += [
 (80,'被做为高领主代表','被作为高领主代表','错别字'),
 (172,'还做为皇宫外围的哨兵','还作为皇宫外围的哨兵','错别字'),
 (98,'也不排审判官参与','也不排除审判官参与','补全漏字'),
 (871,'x星际战士新兵','星际战士新兵','删除混入字符'),
 (588,'同时执行着对众多对人类生存至关重要的任务','同时执行着众多对人类生存至关重要的任务','修正语病'),
 (588,'公元前8世纪，帝皇出生在(安纳托利亚)萨卡里亚河岸边的一个原始赫梯村庄','公元前第8个千年，帝皇出生在安纳托利亚萨卡里亚河岸边的一个原始赫梯村庄','依据紧邻英文修正时间单位与括号'),
 (588,'他看到了自己被谋杀的景象','他看到了父亲被谋杀的景象','依据紧邻英文修正指代'),
 (588,'永生者尔达遇到了皇帝，当时她已经是一个试图加速人类进化并将种族引导至优势物种的军阀','永生者尔达遇到了帝皇；当时，帝皇已经是一位试图加速人类进化、将人类引导为更优越物种的军阀','依据紧邻英文修正指代与语序'),
 (588,'人类们-萨满秘会；创造的一个计划的结果','人类——萨满秘会——所策划的结果','修正语法与断句'),
 (588,'在有成记录的历史之前','在有文字记录的历史之前','修正错字与搭配'),
 (588,'并驾驭着他们的一部分力量的出现了','并带着从他们那里获得的一部分力量归来','依据紧邻英文修正语序'),
 (588,'将它们交给他的稳定原体','将这些能量赋予他的原体','依据紧邻英文删除混入词语'),
 (588,'他会通过帝皇塔罗与灵魂绑定的灵能者突然间指引他的种族，与他最重要的侍者保持联系，并指引星炬信标引导太空舰队穿过亚空间。','他同时通过帝皇塔罗指引人类，与灵能者进行灵魂绑定，接见最重要的臣仆，并引导星炬信标，为穿越亚空间的舰船指明航向。','依据紧邻英文修正并列关系'),
 (588,'并增强了他的子嗣，对黄金王座上的帝皇发出了致命一击','并为法杖蓄能，准备对黄金王座上的帝皇施以致命一击','依据紧邻英文修正宾语与时态'),
 (588,'因为它与帝皇一起精神世界中飘荡去发现宇宙知识的极限','因为他的灵魂会与帝皇一起在非物质界中遨游，探索宇宙知识的极限','依据紧邻英文修正语病'),
 (588,'马格努斯可以在为他准备的新军团的带领下回到忠诚派这边','马格努斯可以率领为他准备的新军团回归忠诚派','依据紧邻英文修正主客关系'),
 (588,'沃坎将留下来监督以保证黄金王座上的故障无碍','沃坎将留下来，监督黄金王座的故障保护装置','依据紧邻英文修正语病'),
 (588,'Horus\' mysteriously lowered','Horus mysteriously lowered','英文多余撇号'),
 (588,'confront his father as he donned','confronting his father as he donned','英文语法'),
 (588,'The Emperor reluctant slew','The Emperor reluctantly slew','英文词性'),
 (588,'with a illusion','with an illusion','英文冠词'),
 (588,'guided by an Tarot card','guided by a Tarot card','英文冠词'),
 (588,'his fathers body','his father\'s body','英文所有格'),
 (588,'the Warmasters taunts','the Warmaster\'s taunts','英文所有格'),
 (72,'盖勒立场（也拼写为盖勒力场）','盖勒力场（Gellar Field，也拼写为 Geller Field）','依据紧邻英文修正拼写说明'),
 (72,'这个立场的名字','这个力场的名字','错别字'),
 (72,'专门从事立场技术','专门从事力场技术','错别字'),
]

global_rules = [
 ('太辣','泰拉','地名错别字，已核对两处上下文'),
 ('盖勒立场','盖勒力场','Field 对应的错别字'),
 ('静滞立场','静滞力场','Field 对应的错别字'),
 ('开起盖勒','开启盖勒','错别字'),
]
english_spelling = {'againt':'against','seperate':'separate','recieved':'received','thier':'their','varients':'variants'}

def record_sub(s, pattern, repl, number, kind):
    def sub(m):
        after = repl(m) if callable(repl) else m.expand(repl)
        if after != m[0]:
            edits.append({'number':number,'type':kind,'before':m[0],'after':after,
                          'context':s[max(0,m.start()-35):m.end()+35]})
        return after
    return re.sub(pattern,sub,s)

def repair_text(s, number, title=False):
    for n,old,new,why in rules:
        if n == number:
            count=s.count(old)
            if count:
                edits.append({'number':number,'type':why,'before':old,'after':new,'count':count})
                s=s.replace(old,new)
    for old,new,why in global_rules:
        count=s.count(old)
        if count:
            edits.append({'number':number,'type':why,'before':old,'after':new,'count':count})
            s=s.replace(old,new)
    for old,new in english_spelling.items():
        s=record_sub(s,r'\b'+old+r'\b',new,number,'英文拼写')
    return s

prefixes = 'the|The|a|A|an|An|of|Of|for|For|to|To|from|From|with|With|by|By|in|In|and|And|his|His|its|Its|their|Their|into|Into|at|At|as|As|is|Is|was|Was|were|are|during|During|on|On|both|Both|against|Against|under|Under|between|Between|named|called'
glossary = ['Imperium','Emperor','Primarch','Primarchs','Astartes','Marines','Marine','Tyranid','Tyranids','Necrons','Necron','Chaos','Crusade','Heresy','Legion','Legions','Chapter','Chapters','World','Worlds','Guard','Terra','Guilliman','Horus','Fulgrim','Corax','Orks','Ork','Eldar','Mechanicus','Mortarion','Nihilus','Secundus','Segmentum','Obscurus','Navy','Warmaster']
suffixes = 'and|or|of|in|on|at|to|by|as|is|was|were|are|has|had|have|with|that|which|who|when|where|after|before|during|under|from|for|into|against|within|beyond|between|himself|led|signed|deliberately|forces|worlds|world|invasion|threat|creatures|earned|most|well|but'

def format_md(s,number):
    formatting['不换行空格改为普通空格'] += s.count('\xa0')
    s=s.replace('\xa0',' ').replace('\u200b','').replace('\ufeff','')
    s=repair_text(s,number)
    # Process only prose, never destinations or source URLs.
    protected=re.compile(r'(!?\[[^\]]*\]\([^\n)]+\)|https?://\S+)')
    chunks=protected.split(s)
    for i in range(0,len(chunks),2):
        t=chunks[i]
        t=record_sub(t,r'\b('+prefixes+r')(?=[A-Z][a-z]{2})',r'\1 ',number,'恢复英文词间空格')
        t=record_sub(t,r'\b('+'|'.join(glossary)+r')('+suffixes+r')\b',r'\1 \2',number,'恢复英文词间空格')
        t=record_sub(t,r'(?<=[a-z])\.([A-Z][a-z])',r'. \1',number,'恢复英文句间空格')
        chunks[i]=t
    s=''.join(chunks)
    literal_markup_fixes={
        176:[('**IV****','**IV** **'),('**XVIII****','**XVIII** **')],
        214:[('unknown**./**927','unknown. / 927')],
        232:[('"**-**Prelude*','" — Prelude*')],
        497:[('****Main Parts of any Hive City**','**Main Parts of any Hive City**'),('**任何巢都城市的主要部分****','**任何巢都城市的主要部分**')],
        659:[('*Bronwin**Abermort*','*Bronwin Abermort*')],
        183:[('court**[ing]**death','court[ing] death')],
    }
    for old,new in literal_markup_fixes.get(number,[]):
        formatting['修复局部强调标记']+=s.count(old);s=s.replace(old,new)
    lines=[]
    for line in s.splitlines():
        line=line.rstrip()
        if number in [290,291,777] and line.startswith('> *') and line.endswith('*'):
            formatting['拆分粘连引文']+=line.count('**');line=line.replace('**','*\n>\n> *')
        if re.fullmatch(r'\*{4}[^*]+\*{4}',line):
            line='**'+line[4:-4]+'**';formatting['消除重复加粗标记']+=1
        if '****' in line and not re.fullmatch(r'\s*\*+\s*',line):
            lead='> ' if line.startswith('> ') else ''
            # Adjacent bilingual bold spans need a block boundary to render.
            inner=line[len(lead):]
            if inner.startswith('**') and inner.endswith('**'):
                line=('\n\n'+lead).join(lead+'**'+part+'**' if j==0 else '**'+part+'**' for j,part in enumerate(inner[2:-2].split('****')))
                formatting['拆开粘连的加粗段落']+=1
        lines.append(line)
    s='\n'.join(lines)
    s,n=re.subn(r'<br> {2,}- +', '\n  - ',s)
    formatting['恢复嵌套列表换行']+=n
    # User text remains content; only the known <br> line-break markup is kept.
    s=re.sub(r'<(?!/?br\s*/?>)', '&lt;',s,flags=re.I)
    # Explicit spans support Chinese/punctuation-adjacent bold delimiters that
    # CommonMark otherwise leaves visible. User-supplied HTML was escaped above.
    def strong_span(m):
        formatting['明确加粗边界']+=1
        return '<strong>'+m[1]+'</strong>'
    s=re.sub(r'(?<!\*)\*\*([^*\n]+)\*\*(?!\*)',strong_span,s)
    s=re.sub(r'\n{3,}','\n\n',s).strip()
    return s

articles=[]
for f in sorted((SOURCE/'chapters').glob('*.md')):
    text=f.read_text()
    matches=list(re.finditer(r'^##### (\d+)\. (.+)$',text,re.M))
    for i,m in enumerate(matches):
        n=int(m[1]); entry=ENTRIES[n]
        raw=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
        lines=raw.splitlines();meta={}
        while lines:
            mm=re.match(r'^- (原页面标题|来源|作者|发布时间|页面编号)：(.*)$',lines[0])
            if not mm:break
            meta[mm[1]]=mm[2];lines.pop(0)
        if '页面编号' in meta: entry['cv']=meta['页面编号']
        # Group headings between entries belong to the next table of contents.
        next_e=ENTRIES[int(matches[i+1][1])] if i+1<len(matches) else None
        group_tokens=set()
        if next_e:
            group_tokens=set(next_e['subpath']+[next_e['group']]) - {''}
        while lines and (not lines[-1].strip() or re.fullmatch(r'---+',lines[-1].strip()) or re.match(r'^#{1,6} ',lines[-1]) or lines[-1].strip('* ') in group_tokens):
            line=lines.pop()
            if line.strip():structure.append({'number':n,'removed':line,'reason':'章节间导航或重复分隔符'})
        body='\n'.join(lines).strip()
        assert body, n
        assert meta.get('来源')==entry['url'],(n,meta)
        assert m[2]==entry['title'],(n,m[2],entry['title'])
        articles.append({**entry,'title':repair_text(entry['title'],n,title=True),'metadata':meta,
                         'source_file':f.name,'raw_chars':len(body),'raw_images':len(re.findall(r'!\[[^\]]*\]\([^)]+\)',body)),
                         'markdown':format_md(body,n)})

assert len(articles)==1587 and {x['number'] for x in articles}==set(range(1,1588))
assert sum(x['raw_images'] for x in articles)==4004
(ROOT/'articles.json').write_text(json.dumps(articles,ensure_ascii=False))
(ROOT/'reports/文字校对明细.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2))
(ROOT/'reports/排版处理统计.json').write_text(json.dumps(dict(formatting),ensure_ascii=False,indent=2))
(ROOT/'reports/章节结构整理.json').write_text(json.dumps(structure,ensure_ascii=False,indent=2))
fingerprints={str(f.relative_to(SOURCE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in SOURCE.rglob('*') if f.suffix in ['.md','.json']}
(ROOT/'reports/原始资料校验值.json').write_text(json.dumps(fingerprints,ensure_ascii=False,indent=2))
print(json.dumps({'articles':len(articles),'images':sum(x['raw_images'] for x in articles),'text_edits':len(edits),'formatting':dict(formatting)},ensure_ascii=False))
subprocess.run(['/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(ROOT/'render_markdown.mjs'),str(ROOT/'articles.json'),str(ROOT/'rendered.json')],check=True)
