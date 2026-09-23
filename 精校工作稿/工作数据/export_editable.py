from pathlib import Path
from collections import Counter,defaultdict
from lxml import etree
import json,csv,re,hashlib,zipfile,io
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'工作数据'
corpus=json.loads((DATA/'全书分段底稿.json').read_text())
candidates=json.loads((DATA/'双语术语候选.json').read_text())
by_candidate={r['english'].casefold():r for r in candidates}
edits={}
for p in sorted(DATA.glob('人工精校译文*.json'), key=lambda p: (0 if p.stem=='人工精校译文' else int(p.stem.rsplit('-',1)[1]))):edits.update(json.loads(p.read_text()))
notes=json.loads((DATA/'编辑疑点与说明.json').read_text())
title_file=DATA/'精校篇名.json'
titles=json.loads(title_file.read_text()) if title_file.exists() else {}
addition_file=DATA/'补充译文.json'
additions=json.loads(addition_file.read_text()) if addition_file.exists() else {}
reviewed_articles={1,2,3,4,5,8}
if (DATA/'语言精校篇目.json').exists():reviewed_articles.update(json.loads((DATA/'语言精校篇目.json').read_text()))
core=list(csv.DictReader((DATA/'核心术语定译.tsv').read_text().splitlines(),delimiter='\t'))
lookup={r['英文标准词'].casefold():r for r in core}
term_patterns={term:re.compile(r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])',re.I) for term in lookup}
# Cheap conservative prefilter; exact matches and counts still use the original regex.
def search_fold(text):return text.translate(str.maketrans({'İ':'i','ı':'i','ſ':'s','K':'k'})).casefold()
term_probes={term:(max(re.findall(r'[a-z]{3,}',term),key=len,default='')) for term in lookup}
decision_file=DATA/'用户术语决定.json'
decisions=json.loads(decision_file.read_text()) if decision_file.exists() else {}
sources={r['id']:r for r in json.loads((ROOT/'参考资料/来源清单.json').read_text())}
sources.update({
 'GW-07':{'id':'GW-07','title':'索引卡片勘误','url':'https://assets.warhammer-community.com/chi_wh40k_faq%26errata_index_card_errata_dec2024-lleenckupk-zmmg0thexd.pdf'},
 'GW-08':{'id':'GW-08','title':'土星战役与荷鲁斯之乱新版问答','url':'https://www.warhammer-community.com/en-gb/articles/m11ujimg/tu-xing-zhan-yi-yi-yi-jie-da-you-guan-he-lu-si-zhi-luan-xin-ban-ben-de-wen-ti/'}
})
manifest_path=DATA/'导出文件校验值.json'
prior=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
manifest=dict(prior)
for key,digest in prior.items():
    path=ROOT/key
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise RuntimeError(f'发现手工编辑，拒绝覆盖：{path}')
def save(path,text,bom=False):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    encoded=(('\ufeff' if bom else '')+text).encode('utf-8');key=str(path.relative_to(ROOT))
    if path.exists() and key in prior and hashlib.sha256(path.read_bytes()).hexdigest()!=prior[key]:
        raise RuntimeError(f'发现手工编辑，拒绝覆盖：{path}')
    if path.exists() and key not in prior:raise RuntimeError(f'已有非导出器创建的文件，拒绝覆盖：{path}')
    path.write_bytes(encoded);manifest[key]=hashlib.sha256(encoded).hexdigest()
def save_csv(path,headers,rows):
    f=io.StringIO();w=csv.writer(f);w.writerow(headers);w.writerows(rows);save(path,f.getvalue(),True)
def esc(s):return s.replace('\\','\\\\').replace('*','\\*').replace('`','\\`').replace('[','\\[').replace(']','\\]').replace('<','\\<').replace('>','\\>')
def split_pair(s):
    m=re.match(r'^([^\u3400-\u9fff]*[A-Za-z][^\u3400-\u9fff]*)\s*([\u3400-\u9fff].*)$',s)
    return (m.group(1).strip(),m.group(2).strip()) if m else None

groups=list(dict.fromkeys(a['major'] for a in corpus));groupdirs={g:f'{i+1:02d}-{g}' for i,g in enumerate(groups)}
article_index=[];changes=[];term_matches=Counter();term_articles=defaultdict(set)
for article in corpus:
    n=article['number'];major=article['major'];directory=groupdirs[major]
    filename=f'{n:04d}.md';title=titles.get(str(n),article['title'])
    if n==8:title='深度打击 Deep Strike'
    state='中文行文已逐段精校，部分术语仍为暂定' if n in reviewed_articles else '待逐段精校'
    lines=[f'# {n:04d} {title}','',f'精校状态：{state}','',f'分类：{major}'+(' / '+' / '.join(article['subpath']) if article['subpath'] else ''),'',f'原文来源：{article["url"]}','',f'原作者：{article["metadata"].get("作者","")}','',f'原文时间：{article["metadata"].get("发布时间","")}','', '[返回分类目录](目录.md) · [全书目录](../../目录.md)','']
    if title!=article['title']:lines += ['原篇名：'+esc(article['title']),'']
    for b in article['blocks']:
        bid=b['id'];original=b['text'];revised=edits.get(bid)
        if b['kind']=='image':
            src=Path(b['src']).name
            lines += [f'<!-- {bid} 图片 -->',f'![{esc(b.get("alt", ""))}](../../图片/{src})','']
            continue
        lines += [f'<!-- {bid} -->']
        # Safe term changes are limited to exact bilingual labels/headings.
        # Narrative Chinese is revised by GPT only, never by broad replacement.
        if revised is None and b['kind'] in ('heading','list','caption'):
            pair=split_pair(original)
            if pair and pair[0].casefold() in lookup:
                chosen=lookup[pair[0].casefold()]
                if chosen['译名状态'].startswith(('官方已核对','编辑用语已统一')):
                    revised=pair[0]+' '+chosen['采用中文']
                    if revised==original:revised=None
        if bid=='A0001-B0070' and revised:revised=revised.replace('比拉克便','比拉克尔便')
        if revised is not None and revised!=original:
            changes.append([bid,n,original,revised,notes.get(bid,'对照英文校顺中文；术语依核心术语表，未核官方者保留暂定状态。')])
        if b['kind']=='heading':
            h=etree.fromstring(b['html']).tag.rsplit('}',1)[-1]
            level=min(max(int(h[1:]),2),6)
            lines += ['#'*level+' '+esc(revised or original),'']
            if revised and revised!=original:lines += ['原题：'+esc(original),'']
        elif b['language']=='en':
            lines += ['**英文原文**','',esc(original),'']
        else:
            lines += ['<details>','<summary>原译文</summary>','',esc(original),'','</details>','']
            label='校订译文' if n in reviewed_articles or revised is not None else '校订译文（待精校，当前保留原译）'
            lines += [f'**{label}**','',esc(revised if revised is not None else original),'']
        if bid in additions:
            assert b['language']=='en',(bid,'补译必须对应英文原文')
            lines += ['**补译**','',esc(additions[bid]),'']
            changes.append([bid,n,'',additions[bid],notes.get(bid,'原稿缺少中文，依据英文补译。')])
        if bid in notes:lines += ['**校注：** '+notes[bid],'']
        lines += [f'<!-- /{bid} -->','']
    article_index.append([n,title,major,state,str(Path('正文')/directory/filename),article['url']])
    english='\n'.join(b['text'] for b in article['blocks'] if b['language']=='en')
    found_terms=[]
    folded_english=search_fold(english)
    for term in lookup:
        if term_probes[term] not in folded_english:continue
        count=len(term_patterns[term].findall(english))
        if count:term_matches[term]+=count;term_articles[term].add(n)
        if count:found_terms.append(lookup[term])
    if found_terms:
        lines += ['<details>','<summary>本篇核心术语与暂定项</summary>','','以下列出本篇出现的英文原形及核心术语表用词。同形词可能指不同对象，具体词义以本篇正文和校注为准；单复数、别名和仅见于图注的名称可能尚未列入。完整候选见[术语表](../../术语表/双语术语候选.csv)。','','| 英文 | 采用中文 | 状态 |','| --- | --- | --- |']
        lines += [f'| {esc(r["英文标准词"])} | {esc(r["采用中文"])} | {r["译名状态"]} |' for r in found_terms]
        lines += ['','</details>','']
    save(Path('正文')/directory/filename,'\n'.join(lines))

completion_text=(f'全书共 {len(corpus):,} 篇，中文行文已全部完成逐段精校。' if len(reviewed_articles)==len(corpus) else f'全书共 {len(corpus):,} 篇；中文行文已逐段精校 {len(reviewed_articles)} 篇，其余仍标为待精校。')+'部分专名采用暂定译名，尚未查得官方出处。'
index=['# 战锤 40K 设定汇编精校工作稿','','编辑格式：Markdown 分章正文与 CSV 术语表。正文按原书分类保存，每篇独立成文。','',completion_text,'', '[使用与校订规则](使用说明.md) · [精校说明](本批精校说明.md) · [核心术语表](术语表/核心术语表.csv) · [全量双语候选](术语表/双语术语候选.csv) · [英文正文候选](术语表/英文正文术语候选.csv) · [译名冲突](术语表/译名冲突.csv) · [精校进度](精校进度.csv)','']
for g in groups:
    subset=[a for a in article_index if a[2]==g];gd=groupdirs[g]
    index.append(f'- [{g}](正文/{gd}/目录.md)：{len(subset)} 篇')
    sub=['# '+g,'','[返回全书目录](../../目录.md)','']
    sub.extend(f'- [{r[0]:04d} {r[1]}]({r[0]:04d}.md) — {r[3]}' for r in subset)
    save(Path('正文')/gd/'目录.md','\n'.join(sub)+'\n')
save(Path('目录.md'),'\n'.join(index)+'\n')
save_csv(Path('精校进度.csv'),['篇号','篇名','分类','状态','稿件路径','来源'],article_index)

headers=['术语ID','英文标准词','采用中文','原书译名','译名状态','官方或参考来源','定位','原形在英文段落中的次数','出现篇号','编辑说明','你的定译']
rows=[]
for r in core:
    key=r['英文标准词'].casefold();candidate=by_candidate.get(key,{})
    olds='；'.join(candidate.get('translations',{}))
    ref_parts=[]
    for source_part in r['依据'].split('；'):
        source_ids=['GW-'+n.zfill(2) for n in re.findall(r'GW-?\s*(\d{1,2})',source_part)]
        if source_ids and 'https://' not in source_part:
            ref_parts.extend(sources[k]['url'] for k in source_ids if k in sources)
        else:ref_parts.append(sources.get(source_part,{}).get('url',source_part))
    refs='；'.join(dict.fromkeys(ref_parts))
    tid='T-'+hashlib.sha1(key.encode()).hexdigest()[:10]
    rows.append([tid,r['英文标准词'],r['采用中文'],olds,r['译名状态'],refs,r['定位'],term_matches[key],','.join(f'{i:04d}' for i in sorted(term_articles[key])),r['编辑说明'],decisions.get(key,{}).get('用户决定','')])
save_csv(Path('术语表/核心术语表.csv'),headers,rows)
candidate_rows=[];conflicts=[]
for r in candidates:
    key=r['english'].casefold();adopted=lookup.get(key)
    variants=sorted(r['translations'].items(),key=lambda x:(-x[1],x[0]))
    selected=adopted['采用中文'] if adopted else variants[0][0]
    status=adopted['译名状态'] if adopted else '待筛选·原译候选，不代表定译'
    row=['C-'+hashlib.sha1(key.encode()).hexdigest()[:10],r['english'],selected,'；'.join(f'{k}（{v}）' for k,v in variants),status,r['article_count'],','.join(f'{i:04d}' for i in r['articles']),','.join(r['sources']),r['contexts'][0]['text'],decisions.get(key,{}).get('用户决定','')]
    candidate_rows.append(row)
    if len(variants)>1:conflicts.append(row)
ch=['候选ID','英文词条','建议中文或原译候选','原译及清单频次','状态','清单检出篇数','检出篇号','提取位置','原文样例','你的定译']
save_csv(Path('术语表/双语术语候选.csv'),ch,candidate_rows)
save_csv(Path('术语表/译名冲突.csv'),ch,conflicts)
save_csv(Path('逐段修订记录.csv'),['段落ID','篇号','原译','校订译文','说明'],changes)
save_csv(Path('参考资料/已核对来源.csv'),['来源ID','名称','网址','核对方式'],[[k,v['title'],v['url'],v.get('check_method', 'PDF 已下载并提取核对' if v.get('ok') else '网页工具核对；未保存原文件')] for k,v in sources.items()])

readme='''# 使用说明

从“目录.md”进入分类和具体文章。每篇都有固定篇号；每个段落都有固定编号，方便追踪修改。

## 手工编辑

直接修改“校订译文”下方的中文即可。折叠的“原译文”和英文原文用于对照，建议保留。尚未完成的段落会标明“待精校”，不能将它们视为完成稿。标题和图片保留在原位置，图片全部位于本目录的“图片”文件夹内。

可用 Typora、Obsidian、VS Code 或其他 Markdown 编辑器打开。移动资料时，请一起移动正文和图片文件夹。CSV 为 UTF-8 编码，可用 Excel、Numbers 或文本编辑器修改。

## 术语规则

核心术语表以英文为索引。官方已核对的译名附有网址、页码或页面位置；暂定译名明确标注。双语候选表来自标题、列表和图注，不是已经全部确认的专名词典；其中也含普通章节用语。不要将“原译候选”自动视为定译。“译名冲突.csv”保留的是原稿历史异译，供追溯比较；它不表示现稿仍在混用这些译名。篇末术语附表按英文原形检索，同形词的具体含义以正文与校注为准。

英文正文候选表补充提取叙述段落中的名称，附英文上下文和相邻原译。它依据英文大写模式初筛，仍可能包含普通短语；相邻段落也不保证逐句对应，均需语义复核。核心表中的频次只统计英文原形，不是合并了全部单复数、别名的实体总频次。

优先级为：与该词具体语境对应的 Games Workshop 官方简体中文资料；官方中文介绍页面；有依据的暂定译名。官方网站内部有异译时，记录两者，并说明本书采用哪一种。不能把授权电子游戏译文直接标成 GW 官网译文。

已确认的本稿用词：Ordo Malleus 采用“恶魔审判庭”，原稿译名“圣锤修会”；Ordo Hereticus 采用“异端审判庭”，原稿译名“讨逆修会”；Ordo Xenos 采用“异形审判庭”，原稿译名“攘外修会”。按全书正文顺序，在各词首次出现时附原稿译名，此后使用本稿定译。相关词条标为“用户确认·官方待核”，与“官方已核对”分别记录。

名称相近但概念不同的词分开登记，例如 Astropath／Astronomican／Adeptus Astronomica，以及 Imperial Army／Imperial Guard／Astra Militarum。英文别名、单复数与拼写变体在确认后才能合并。

可在术语表的“你的定译”栏填写修改意见。修改 CSV 不会自动改动正文；采用前仍需逐段确认英文所指对象，避免把同形词替换错。

## 中文精校规则

以本书英文段落为直接依据，修复错译、漏译、指代不清、句式僵硬和不自然的搭配。保留英文原文及原译，不用通用替换规则冒充逐段语义校对。已经可读且忠实的语句可以保留。

英文自身有拼写、语法或设定疑点时，在校注中指出。未经核实，不擅自增添原文没有的设定，也不以记忆中的设定覆盖英文。

## 当前范围

这是精校工作稿。全书文本和配图已整理为可编辑格式；逐篇完成范围以“精校进度.csv”为准。已完成语言精校的篇目仍可能含待核官方出处的暂定专名。“待逐段精校”的篇目仅完成格式整理及少量有明确依据的标题术语修正。

本次不生成 EPUB。最终完成并确认文字后，再从这套稿件制作电子书。
'''
if len(reviewed_articles)==len(corpus):
    readme=readme.replace('尚未完成的段落会标明“待精校”，不能将它们视为完成稿。','全书中文已完成逐段精校；暂定专名与原文疑点仍在术语表及校注中标明。')
    readme=readme.replace('这是精校工作稿。全书文本和配图已整理为可编辑格式；逐篇完成范围以“精校进度.csv”为准。已完成语言精校的篇目仍可能含待核官方出处的暂定专名。“待逐段精校”的篇目仅完成格式整理及少量有明确依据的标题术语修正。','全书 1,587 篇均已对照英文逐段校读，修订范围与原译对照见“逐段修订记录.csv”，篇目状态见“精校进度.csv”。全书完成语言精校不代表所有专名均已取得官方中文依据；暂定译名继续保留待核标记。')
save(Path('使用说明.md'),readme)
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
summary={'articles':len(corpus),'language_reviewed_articles':sorted(reviewed_articles),'core_terms':len(core),'official_verified_terms':sum(r['译名状态'].startswith('官方已') for r in core),'bilingual_candidates':len(candidates),'translation_conflicts':len(conflicts),'revised_blocks':len(changes),'markdown_files':sum(x.endswith('.md') for x in manifest),'images':3918}
(DATA/'导出统计.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False))
