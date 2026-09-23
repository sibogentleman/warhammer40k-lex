import json,pathlib
P=pathlib.Path(__file__).parent
def save(edits,notes=None,reviewed=None):
 for f,d in [('edits.json',edits),('notes.json',notes or {})]:
  p=P/f;o=json.loads(p.read_text());o.update(d);p.write_text(json.dumps(o,ensure_ascii=False,indent=2))
 if reviewed:
  p=P/'reviewed.json';o=json.loads(p.read_text());p.write_text(json.dumps(sorted(set(o+reviewed)),ensure_ascii=False,indent=2))
def terms(rows):
 p=P/'terms.tsv'
 if not p.exists():p.write_text('英文标准词\t采用中文\t译名状态\t依据\t定位\t编辑说明\n')
 with p.open('a') as f:
  for en,zh,loc,note in rows:f.write('\t'.join([en,zh,'暂定·官方待核','所给英文底稿',loc,note])+'\n')
