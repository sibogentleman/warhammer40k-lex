from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'战锤40K_全书精校稿_Markdown与CSV.zip'
files=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or p.name.startswith('.'):continue
    rel=p.relative_to(ROOT)
    if rel.parts[0]=='工作数据':continue
    if rel.parts[0]=='参考资料' and p.suffix!='.csv':continue
    files.append(p)
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,Path(ROOT.name)/p.relative_to(ROOT))
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    assert len([n for n in z.namelist() if '/图片/' in n])==3918
    assert len([n for n in z.namelist() if n.endswith('.md')])==1603
r={'zip':str(OUT),'files':len(files),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'crc_checked':True}
(ROOT/'工作数据/打包核验.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print(json.dumps(r,ensure_ascii=False))
