# Interactive Turkish PII browser demo

The [HF Space](https://huggingface.co/spaces/halilneed/turkish-pii-detection-demo) accepts editable text and runs the actual model on the visitor's device using WebAssembly. It needs no inference server or HF compute subscription. The model and its tokenizer download on the first request (approximately 472 MB, plus the runtime); browser caching is supported. The UI does not send the input to a backend or save input/output. Short texts work best; memory and speed depend on the device.

Türkçe: Metninizi yazın, politikayı seçin ve **Metni maskele** düğmesine basın. Model cihazınızda çalışır. İlk kullanımda model dosyaları indirilir; daha sonra tarayıcı önbelleği kullanılabilir. Durdurma düğmesi çalışan işçiyi sonlandırır; sonraki çalıştırma modeli önbellekten yeniden yükleyebilir.

## Source layout

- `inference.js`: exact Gemma prompt, three instructions, input validation, deterministic generation and completeness detection. Shared by Node checks and the browser worker.
- `../showcase/app.js`: input, progress, output and stop controls.
- `../showcase/worker.js`: loads the local browser model and runs inference off the UI thread.
- `build.mjs`: bundles the pinned Transformers.js runtime into the Space's public files.
- `check-model.mjs`: three recorded policies plus a different phone/email input against the real converted model. These are functional checks, not benchmark results.

## Rebuild runtime

```bash
cd demo/browser
npm ci
node build.mjs
```

The Space needs `index.html`, `app.js`, `worker.js`, the generated runtime and its license notices from `demo/showcase/`, plus `inference.js` from this directory at the Space root. Generated library bundles are ignored by Git and are recreated with `node build.mjs`. Model files are served under `browser-model/`. They are stored in the Space, rather than in this GitHub repository. Do not include `node_modules` or binary weights in a GitHub source commit.

## Model conversion

The separate browser artifact is derived from original model revision `28644718923ae38b0105c9f3d2be57312ad0ced3`. The original model repository and its `.safetensors` file are unchanged. Export used PyTorch 2.8.0+cpu, Transformers 4.56.1, Optimum ONNX 0.1.0 and ONNX opset 21; dynamic uint8 quantization of MatMul and Gather used ONNX Runtime 1.23.2. Optimum's float export reported a maximum logits difference of approximately 0.000248 relative to PyTorch on its validation input. This is not a guarantee of equivalence on all inputs.

The browser conversion reproduced the three recorded outputs and correctly masked a new phone/email example in Node and WebAssembly browser checks. Quantization may still change outputs. The original benchmark scores have not been revalidated for this conversion. Inputs are limited to 800 characters / 512 prompt tokens and 256 generated tokens; interrupted or truncated outputs are marked incomplete.

The browser model's `config.json` adds `transformers.js_config.use_external_data_format=false` and source/quantization provenance; no training was performed. The ONNX file carries a modification notice. Gemma weights remain under the [Gemma Terms of Use](https://ai.google.dev/gemma/terms), including Section 3.2 use restrictions. A copy of the terms and a Notice are included with the Space's model files. The demo source is MIT licensed; bundled dependencies retain their license notices.
