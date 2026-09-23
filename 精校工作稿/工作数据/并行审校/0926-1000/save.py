import json,pathlib
P=pathlib.Path(__file__).parent
SOURCE=P.parent.parent/'全书分段底稿.json'
def replacements(numbers,mapping):
    prior=json.loads((P/'edits.json').read_text()); edits={}
    for article in json.loads(SOURCE.read_text()):
        if article['number'] not in numbers: continue
        for b in article['blocks']:
            if b.get('language')!='zh':continue
            s=prior.get(b['id'],b['text'])
            for old,new in mapping.items():s=s.replace(old,new)
            if s!=prior.get(b['id'],b['text']):edits[b['id']]=s
    save(edits)
def save(edits, reviewed=(), notes=None):
    for name, value in [('edits.json',edits),('notes.json',notes or {})]:
        obj=json.loads((P/name).read_text());obj.update(value)
        (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    obj=json.loads((P/'reviewed.json').read_text())
    (P/'reviewed.json').write_text(json.dumps(sorted(set(obj)|set(reviewed)))+'\n')
