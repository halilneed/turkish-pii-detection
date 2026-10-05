---
title: Turkish PII Detection and Masking
short_description: Mask your own Turkish text locally in your browser
emoji: 🔎
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
license: gemma
models:
- halilneed/turkish-pii-detection
tags:
- turkish
- pii-detection
- masking
---

# Turkish PII Detection: interactive browser demo

Enter your own Turkish text and run [halilneed/turkish-pii-detection](https://huggingface.co/halilneed/turkish-pii-detection) directly in your browser. Compare full masking, phone-only masking, and masking that preserves names. This is real inference on your input, using a separate dynamic uint8 ONNX conversion of the original v02 weights.

Türkçe: Kendi metninizi yazın, maskeleme politikasını seçin ve **Metni maskele** düğmesine basın. Model tarayıcınızda çalışır; uygulama girdiyi sunucuya göndermez. İlk kullanımda yaklaşık **472 MB** model dosyası ve çalıştırma bileşenleri indirilir. Dosyalar tarayıcınızın önbelleğine alınabilir.

The UI remains responsive while a Web Worker runs WebAssembly inference. Model loading is lazy and can be cancelled; generation can be stopped. The demo uses at most 800 input characters / 512 prompt tokens and 256 generated tokens. Short texts work best. It does not save inputs or predictions. Model/runtime downloads make network requests, but inference does not send the input to a backend.

Quantization can change outputs. Original Python benchmark scores have not been revalidated for this browser conversion. Review every result; the model can miss personal data or alter unrelated text. Low-memory devices may not be able to load the model; use the Python demo in that case.

- [Turkish PII detection model on Hugging Face](https://huggingface.co/halilneed/turkish-pii-detection)
- [Run the local interactive demo](https://github.com/halilneed/turkish-pii-detection/tree/main/demo)
- [Python tutorial with instructions and recorded results](https://github.com/halilneed/turkish-pii-detection/blob/main/docs/python-turkish-pii-masking.md)

Original weight revision: `28644718923ae38b0105c9f3d2be57312ad0ced3`. Converted with PyTorch 2.8.0+cpu, Transformers 4.56.1 and Optimum ONNX 0.1.0; dynamic uint8 MatMul/Gather quantization with ONNX Runtime 1.23.2. Browser runtime: Transformers.js 4.3.0. Three policy examples and a different input were checked with the actual converted model in Node and a browser; these functional checks are not a benchmark rerun.

The browser model files in `browser-model/` are modified derivatives of the original model. They remain subject to the [Gemma Terms of Use](https://ai.google.dev/gemma/terms), including the use restrictions in Section 3.2 and the [Gemma Prohibited Use Policy](https://ai.google.dev/gemma/prohibited_use_policy). A copy of the terms and a Notice accompany the model files. The original demo UI/source is MIT licensed; bundled libraries retain their licenses in `transformers-runtime.js.LEGAL.txt`. The original HF model repository and its weights are unchanged by this deployment.
