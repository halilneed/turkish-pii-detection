---
title: Turkish PII Detection and Masking
short_description: Full, phone-only and keep-names masking in Turkish
emoji: 🔎
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
python_version: '3.10.13'
app_file: app.py
pinned: false
license: mit
models:
- halilneed/turkish-pii-detection
tags:
- turkish
- pii-detection
- masking
- privacy
---

# Turkish PII Detection and Masking — Türkçe Kişisel Veri Maskeleme

A demo for [halilneed/turkish-pii-detection](https://huggingface.co/halilneed/turkish-pii-detection), a 270M instruction-conditioned Turkish PII masking model. Compare full masking, phone-only masking, and masking that keeps names. This Python application defaults to CPU. The [online Space](https://huggingface.co/spaces/halilneed/turkish-pii-detection-demo) now accepts your own input and runs a separate quantized ONNX conversion in the browser; see [browser source and build notes](browser/README.md). The optional Python ZeroGPU hosting code is prepared for eligible accounts.

Türkçe: Aynı metin üzerinde tüm kişisel verileri, yalnızca telefon numaralarını veya isim dışındaki verileri maskeleyen üç politikayı deneyin. Türkçe tanıtım ve kullanım açıklamaları model kartında korunur.

The output is generated text, not NER spans or offsets. Use fictional inputs in the public demo. The local application does not save or log prompts or predictions. If you deploy an inference server, inputs are sent to that server. Download the model for sensitive local use. Hosting infrastructure may collect its own service logs.

The model is pinned to v02 weights revision `28644718923ae38b0105c9f3d2be57312ad0ced3`. Local CPU execution loads the model on the first request. ZeroGPU loads it at startup and allocates a shared GPU for each call, subject to HF daily quotas. Requests are processed one at a time, with a queue of eight, at most 1,500 input characters / 1,024 input tokens and 512 generated tokens. Review empty, incomplete and incorrectly masked outputs.

## Run locally

```bash
git clone https://github.com/halilneed/turkish-pii-detection.git
cd turkish-pii-detection/demo
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

- [Download the model and read its limits](https://huggingface.co/halilneed/turkish-pii-detection)
- [Python masking guide and recorded examples](https://github.com/halilneed/turkish-pii-detection/blob/main/docs/python-turkish-pii-masking.md)
- [Source code](https://github.com/halilneed/turkish-pii-detection/tree/main/demo)

For ZeroGPU hosting, use `requirements-space.txt` as the Space's `requirements.txt`, set `PII_DEMO_DEVICE=cuda`, select ZeroGPU hardware and preserve the README metadata. The `spaces.GPU` callback releases the GPU after each request. CPU Basic hosting currently requires HF PRO, even though its hardware has no hourly charge.

The original demo code is MIT licensed; model weights remain subject to [Gemma Terms of Use](https://ai.google.dev/gemma/terms).
