// Compatibility entry point. Rebuild the reviewed Hindi pack and all-subject guide.
const {spawnSync} = require('node:child_process');
const result = spawnSync('python', ['-X', 'utf8', 'build_icse_2027.py'], {cwd:__dirname, stdio:'inherit'});
if (result.error) { console.error(result.error.message); process.exit(1); }
process.exit(result.status ?? 1);
