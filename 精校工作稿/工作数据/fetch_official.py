from pathlib import Path
import urllib.request, concurrent.futures, json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'参考资料'
def get(row):
    row=dict(row)
    try:
        r=urllib.request.urlopen(row['url'],timeout=25)
        data=r.read();ext='pdf' if data[:4]==b'%PDF' else 'html'
        file=P/f'{row["id"]}-{row["title"]}.{ext}';file.write_bytes(data)
        row.update(file=str(file),bytes=len(data),ok=True)
        row.pop('error',None)
    except Exception as e:row.update(ok=False,error=str(e))
    return row
rows=json.loads((P/'来源清单.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    result=list(pool.map(get,rows))
(P/'来源清单.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
