import fs from 'node:fs';
import path from 'node:path';
import { marked } from '/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';
import { chromium } from '/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const root='/Users/bytedance/Documents/ChatGPT/战锤 40k/精校工作稿';
const browser=await chromium.launch({headless:true,channel:'chrome'});
const page=await browser.newPage({viewport:{width:1100,height:1000}});
await page.route(/^https?:/,route=>route.abort());
const reports=[];
for (const n of [263,277,292,304]) {
  const file=fs.readdirSync(path.join(root,'正文')).map(g=>path.join(root,'正文',g,String(n).padStart(4,'0')+'.md')).find(f=>fs.existsSync(f));
  const html='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><base href="file://'+path.dirname(file)+'/">'+
   '<style>body{max-width:780px;margin:40px auto;padding:0 24px;font:17px/1.8 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;color:#26303c}h1{font-size:29px}h2{font-size:24px;margin-top:40px}h3{font-size:21px}img{max-width:100%;max-height:500px;display:block;margin:24px auto}details{border-left:3px solid #bba47a;padding:10px 16px;margin:18px 0;background:#f7f5f0}summary{cursor:pointer;color:#78694d}p{overflow-wrap:anywhere}a{color:#486281}</style><body>'+marked(fs.readFileSync(file,'utf8'))+'</body></html>';
  const out=path.join(root,'工作数据',`预览-${n}.html`);fs.writeFileSync(out,html);
  await page.goto('file://'+out);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
  reports.push(await page.evaluate(()=>({title:document.querySelector('h1')?.textContent,images:document.images.length,broken:[...document.images].filter(i=>!i.naturalWidth).length,overflows:document.documentElement.scrollWidth>innerWidth,originals:document.querySelectorAll('details').length})));
  if(n===263) {
    await page.screenshot({path:path.join(root,'工作数据/样稿预览.png')});
    await page.locator('details').first().locator('summary').click();
    await page.screenshot({path:path.join(root,'工作数据/原译对照预览.png')});
  }
}
await browser.close();
fs.writeFileSync(path.join(root,'工作数据/排版核验.json'),JSON.stringify(reports,null,2));
console.log(JSON.stringify(reports));
if(reports.some(r=>r.broken||r.overflows))process.exitCode=1;
