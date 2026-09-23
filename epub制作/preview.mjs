import fs from 'node:fs';
import {chromium} from '/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const root='/Users/bytedance/Documents/ChatGPT/战锤 40k/epub制作';
const browser=await chromium.launch({headless:true,channel:'chrome'});
const reports=[];
for (const width of [430,960]) {
  const page=await browser.newPage({viewport:{width,height:932},deviceScaleFactor:1});
  await page.route(/^https?:/,route=>route.abort());
  for (const name of ['cover','article-0588','article-0001','article-0176','article-0805','article-1498','category-01']) {
    await page.goto('file://'+root+'/package/EPUB/text/'+name+'.xhtml');
    reports.push(await page.evaluate(()=>({title:document.title,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:document.images.length,broken:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,headings:document.querySelectorAll('h1,h2,h3').length})));
    if (['cover','article-0588','article-0176','category-01'].includes(name)) await page.screenshot({path:root+'/reports/'+name+'-'+width+'.png'});
    if (name==='article-0588'&&width===430) {
      await page.evaluate(()=>window.scrollTo(0,1000));
      await page.screenshot({path:root+'/reports/正文段落-430.png'});
    }
  }
  await page.close();
}
await browser.close();
fs.writeFileSync(root+'/reports/离线渲染检查.json',JSON.stringify(reports,null,2));
console.log(JSON.stringify(reports));
