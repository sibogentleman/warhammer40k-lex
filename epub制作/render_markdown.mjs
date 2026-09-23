import fs from 'node:fs';
import {marked} from '/Users/bytedance/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';
const rows = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const row of rows) row.html = marked.parse(row.markdown, {gfm:true, breaks:false});
fs.writeFileSync(process.argv[3], JSON.stringify(rows));
