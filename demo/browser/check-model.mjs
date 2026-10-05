import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import * as runtime from '@huggingface/transformers';
import { createEngine } from './inference.js';

const root = path.resolve(import.meta.dirname, '../../..');
runtime.env.allowRemoteModels = false;
runtime.env.allowLocalModels = true;
runtime.env.useFSCache = false;
const modelPath = path.join(root, '.browser-artifact').replaceAll('\\', '/');
const engine = await createEngine(runtime, modelPath, { device: 'cpu' });
const original = JSON.parse(await fs.readFile(path.join(root, 'seo-geo-update/demo-recorded-runs.json'), 'utf8'));
const checks = [];
try {
  await assert.rejects(engine.mask('', 0), /Enter Turkish text/);
  for (let policy = 0; policy < 3; policy++) {
    const started = performance.now();
    const result = await engine.mask(original.runs[policy].input, policy);
    console.log(JSON.stringify({ policy, ...result, seconds: (performance.now() - started) / 1000 }));
    assert.equal(result.output, original.runs[policy].output);
    assert.ok(result.complete);
    checks.push({ policy, input: original.runs[policy].input, ...result });
  }
  const input = 'iletişim telefonu 0544 222 33 44, e-posta deneme@example.org.';
  const result = await engine.mask(input, 1);
  assert.ok(result.output.includes('[TEL]'));
  assert.ok(result.output.includes('deneme@example.org'));
  assert.ok(!result.output.includes('0544'));
  assert.ok(result.complete);
  checks.push({ policy: 1, input, ...result });
  await fs.writeFile(path.join(root, 'seo-geo-update/browser-inference-checks.json'), JSON.stringify({ runtime: runtime.env.version, checks, benchmarkRerun: false }, null, 2));
  console.log('All browser-model functional checks passed.');
} finally { await engine.dispose(); }
