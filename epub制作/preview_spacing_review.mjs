import fs from 'node:fs';
import { chromium } from '/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
const root = '/Users/bytedance/Documents/ChatGPT/战锤 40k/epub制作/reports/英文二次校对';
const samples = [
  [9, 'Imperial Nobility'], [68, 'each other'], [282, 'Occult Bodyguards'],
  [545, 'Home World'], [835, 'Night Guard'], [864, 'Helios Hellgrace'],
  [1252, 'Ultima pattern storm'], [1433, 'on road N/A'],
];
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const reports = [];
for (const width of [430, 960]) {
  const page = await browser.newPage({ viewport: { width, height: 932 }, deviceScaleFactor: 1 });
  await page.route(/^https?:/, route => route.abort());
  for (const [number, term] of samples) {
    const name = `article-${String(number).padStart(4, '0')}`;
    await page.goto(`file://${root}/preview/EPUB/text/${name}.xhtml`);
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
    });
    const result = await page.evaluate(term => {
      const matches = [...document.querySelectorAll('p,li,h2,h3,h6')].filter(e => e.textContent.includes(term));
      const target = matches.sort((a, b) => a.textContent.length - b.textContent.length)[0];
      if (target) window.scrollTo(0, window.scrollY + target.getBoundingClientRect().top - 100);
      return {
        title: document.title, width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        images: document.images.length,
        brokenImages: [...document.images].filter(image => !image.complete || !image.naturalWidth).length,
        term, foundTerm: !!target, renderedExcerpt: target?.textContent.slice(0, 600),
      };
    }, term);
    reports.push({ number, ...result });
    if ([9, 68, 835, 1252].includes(number)) await page.screenshot({ path: `${root}/${name}-${width}.png` });
  }
  await page.close();
}
await browser.close();
fs.writeFileSync(`${root}/离线渲染检查.json`, JSON.stringify(reports, null, 2));
const errors = reports.filter(r => r.brokenImages || r.scrollWidth > r.width || !r.foundTerm);
console.log(JSON.stringify({ checks: reports.length, errors, imagesAcrossChecks: reports.reduce((n, r) => n + r.images, 0) }));
if (errors.length) process.exitCode = 1;
