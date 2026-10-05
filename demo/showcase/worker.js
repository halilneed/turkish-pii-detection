import { createEngine } from './inference.js';

let engine;
let loading;
let busy = false;

async function load() {
  if (!loading) {
    const path = 'browser-model';
    loading = import('./transformers-runtime.js').then(runtime => {
      runtime.env.allowRemoteModels = false;
      runtime.env.allowLocalModels = true;
      runtime.env.localModelPath = './';
      runtime.env.useBrowserCache = true;
      runtime.env.backends.onnx.wasm.numThreads = 1;
      return createEngine(runtime, path, {
      device: 'wasm',
      progress_callback: progress => {
        if (progress.status === 'progress') self.postMessage({ type: 'progress', loaded: progress.loaded, total: progress.total, file: progress.file });
      },
      });
    }).then(result => { engine = result; return result; }).catch(error => { loading = null; throw error; });
  }
  return loading;
}

self.onmessage = async ({ data }) => {
  if (data.type === 'stop') { engine?.interrupt(); return; }
  if (data.type !== 'run' || busy) return;
  busy = true;
  try {
    self.postMessage({ type: 'status', phase: engine ? 'generating' : 'loading' });
    const model = await load();
    self.postMessage({ type: 'status', phase: 'generating' });
    const result = await model.mask(data.text, data.policy, text => self.postMessage({ type: 'text', text }));
    self.postMessage({ type: 'done', ...result });
  } catch (error) {
    self.postMessage({ type: 'error', message: error.message || 'Could not run the model. / Model çalıştırılamadı.' });
  } finally { busy = false; }
};

self.addEventListener('close', () => { engine?.dispose(); });
