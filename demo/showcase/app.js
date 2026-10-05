import { POLICIES, SAMPLE, MAX_CHARACTERS } from './inference.js';

const input = document.getElementById('input-text');
const output = document.getElementById('output');
const instruction = document.getElementById('instruction');
const run = document.getElementById('run');
const stop = document.getElementById('stop');
const reset = document.getElementById('sample');
const status = document.getElementById('status');
const progress = document.getElementById('download-progress');
const counter = document.getElementById('counter');
let worker;
let busy = false;
let requestInput;
let requestPolicy;
let loading = false;

function selectedPolicy() { return Number(document.querySelector('input[name="policy"]:checked').value); }
function clearOutput() { output.textContent = 'Your result will appear here. / Sonuç burada görünecek.'; }
function syncInput() { counter.textContent = `${input.value.length} / ${MAX_CHARACTERS}`; }
function setBusy(value) {
  busy = value;
  run.disabled = value;
  reset.disabled = value;
  stop.hidden = !value;
  input.disabled = value;
  document.querySelectorAll('input[name="policy"]').forEach(radio => { radio.disabled = value; });
  output.setAttribute('aria-busy', String(value));
}
function fail(message) {
  setBusy(false);
  progress.hidden = true;
  status.textContent = message;
  status.dataset.state = 'error';
  output.textContent = 'No complete result. Retry or run the Python demo. / Tam bir sonuç yok. Tekrar deneyin veya Python demosunu çalıştırın.';
}
function createWorker() {
  worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' });
  worker.onerror = () => {
    worker.terminate(); worker = null;
    fail('The browser could not load the demo. Reload the page or use a current browser. / Demo yüklenemedi. Sayfayı yenileyin veya güncel bir tarayıcı kullanın.');
  };
  worker.onmessage = ({ data }) => {
    if (data.type === 'status') {
      loading = data.phase === 'loading';
      progress.hidden = !loading;
      stop.textContent = loading ? 'Cancel download / İndirmeyi iptal et' : 'Stop / Durdur';
      status.textContent = loading ? 'Downloading and preparing the model… / Model indiriliyor ve hazırlanıyor…' : 'Masking your text… / Metniniz maskeleniyor…';
    } else if (data.type === 'progress') {
      const loaded = (data.loaded / 1e6).toFixed(1);
      const total = (data.total / 1e6).toFixed(1);
      if (data.total > 0) { progress.value = data.loaded / data.total; status.textContent = `Downloading / İndiriliyor: ${loaded} / ${total} MB`; }
    } else if (data.type === 'text') {
      output.textContent = data.text;
    } else if (data.type === 'done') {
      setBusy(false);
      progress.hidden = true;
      output.textContent = data.output;
      status.textContent = data.complete ? 'Done. Review the result. / Tamamlandı. Sonucu kontrol edin.' : 'Stopped or reached the output limit. This result is incomplete. / İşlem durduruldu veya çıktı sınırına ulaşıldı. Sonuç eksik.';
      status.dataset.state = data.complete ? 'success' : 'error';
    } else if (data.type === 'error') { fail(data.message); }
  };
}

input.value = SAMPLE;
input.maxLength = MAX_CHARACTERS;
syncInput();
instruction.textContent = POLICIES[selectedPolicy()];
input.addEventListener('input', () => { syncInput(); clearOutput(); status.textContent = ''; });
document.querySelectorAll('input[name="policy"]').forEach(radio => radio.addEventListener('change', () => {
  instruction.textContent = POLICIES[selectedPolicy()]; clearOutput(); status.textContent = '';
}));
reset.addEventListener('click', () => { input.value = SAMPLE; syncInput(); clearOutput(); status.textContent = ''; });
run.addEventListener('click', () => {
  if (busy) return;
  if (!input.value.trim()) { status.textContent = 'Enter Turkish text. / Türkçe metin girin.'; input.focus(); return; }
  if (input.value.length > MAX_CHARACTERS) { status.textContent = `Use at most ${MAX_CHARACTERS} characters. / En fazla ${MAX_CHARACTERS} karakter kullanın.`; return; }
  output.textContent = '';
  status.dataset.state = '';
  setBusy(true);
  requestInput = input.value;
  requestPolicy = selectedPolicy();
  try { if (!worker) createWorker(); worker.postMessage({ type: 'run', text: requestInput, policy: requestPolicy }); }
  catch { fail('This browser cannot run the demo. / Bu tarayıcı demoyu çalıştıramıyor.'); }
});
stop.addEventListener('click', () => {
  worker?.terminate(); worker = null;
  setBusy(false); progress.hidden = true;
  if (loading) {
    output.textContent = 'Download cancelled. / İndirme iptal edildi.';
    status.textContent = 'Cancelled. / İptal edildi.';
  } else {
    if (!output.textContent) output.textContent = 'Stopped before output. / Çıktı üretilmeden durduruldu.';
    status.textContent = 'Stopped. Any partial output is incomplete. / Durduruldu. Kısmi çıktı eksiktir.';
    status.dataset.state = 'error';
  }
});
window.addEventListener('pagehide', () => { worker?.terminate(); worker = null; });
