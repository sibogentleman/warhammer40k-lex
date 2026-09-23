from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from PIL import Image
import hashlib, json, time, io

ROOT = Path(__file__).resolve().parent
URLS = json.loads((ROOT / 'image-urls.json').read_text())
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    path = ASSETS / (key + '.img')
    for attempt in range(4):
        try:
            if path.exists():
                data = path.read_bytes()
            else:
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.bilibili.com/'})
                with urlopen(req, timeout=40) as response:
                    data = response.read()
            with Image.open(io.BytesIO(data)) as im:
                width, height, fmt = im.width, im.height, im.format
                im.verify()
            path.write_bytes(data)
            return {'url': url, 'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(),
                    'width': width, 'height': height, 'format': fmt, 'bytes': len(data)}
        except Exception as e:
            err = str(e)
            if attempt < 3:
                time.sleep(1 + attempt * 2)
    return {'url': url, 'error': err}

results = []
started = time.time()
with ThreadPoolExecutor(max_workers=12) as pool:
    futures = [pool.submit(fetch, url) for url in URLS]
    for future in as_completed(futures):
        results.append(future.result())
        if len(results) % 100 == 0 or len(results) == len(URLS):
            print(json.dumps({'done': len(results), 'total': len(URLS), 'errors': sum('error' in x for x in results),
                              'megabytes': round(sum(x.get('bytes',0) for x in results)/1048576,1),
                              'seconds': round(time.time()-started)}, ensure_ascii=False), flush=True)
            (ROOT / 'image-downloads.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))

(ROOT / 'image-downloads.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
assert all('error' not in x for x in results), 'Some images failed; see image-downloads.json'
