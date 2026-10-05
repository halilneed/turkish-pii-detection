---
title: Turkish PII Detection and Masking
short_description: Compare three recorded policies; run Python locally
emoji: 🔎
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
license: mit
models:
- halilneed/turkish-pii-detection
tags:
- turkish
- pii-detection
- masking
---

# Turkish PII Detection: recorded policy examples

Compare three real v02 outputs for the same fictional input: mask all, phone only, and keep names. This static page shows recorded model outputs; it does not perform inference on new text.

Türkçe: Aynı kurgusal metinde üç politikanın gerçek model çıktılarını karşılaştırın. Bu sayfa kaydedilmiş çıktıları gösterir; yeni metin işlemek için yerel Python demosunu çalıştırın.

- [Turkish PII detection model on Hugging Face](https://huggingface.co/halilneed/turkish-pii-detection)
- [Run the local interactive demo](https://github.com/halilneed/turkish-pii-detection/tree/main/demo)
- [Python tutorial with instructions and recorded results](https://github.com/halilneed/turkish-pii-detection/blob/main/docs/python-turkish-pii-masking.md)

Examples recorded on CPU using revision `28644718923ae38b0105c9f3d2be57312ad0ced3`, PyTorch 2.8.0+cpu and Transformers 4.56.1. These three examples are not a benchmark rerun. See the model card for reported benchmark results and limitations.
