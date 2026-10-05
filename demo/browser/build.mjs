import { build } from 'esbuild';
import path from 'node:path';

await build({
  entryPoints: [path.join(import.meta.dirname, 'runtime-entry.js')],
  outfile: path.join(import.meta.dirname, '../showcase/transformers-runtime.js'),
  bundle: true, platform: 'browser', format: 'esm', minify: true,
  legalComments: 'linked',
  target: 'es2022', logLevel: 'info',
});
