# Turkish PII detection and masking in Python

This guide runs [halilneed's Turkish PII detection model on Hugging Face](https://huggingface.co/halilneed/turkish-pii-detection) with three masking policies and the same fictional text. It is a 270M instruction-conditioned text-generation model: its output is masked text, rather than NER spans or offsets.

**Türkçe:** Bu rehberde aynı kurgusal metin üzerinde üç politika çalıştırılır: tümünü maskele, yalnızca telefonu maskele ve isim hariç tümünü maskele. Türkçe tanıtım, teknik açıklamalar ve sonuçlar [HF model kartında](https://huggingface.co/halilneed/turkish-pii-detection) korunur.

[Compare recorded outputs](https://huggingface.co/spaces/halilneed/turkish-pii-detection-demo) · [Download the model](https://huggingface.co/halilneed/turkish-pii-detection) · [Demo source](../demo/app.py)

## Install and run locally

Use a fresh Python environment. The demo's dependencies pin the CPU build of PyTorch and the tested Transformers and Gradio versions:

```bash
git clone https://github.com/halilneed/turkish-pii-detection.git
cd turkish-pii-detection
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r demo/requirements.txt
python demo/app.py
```

The local UI prints its address at startup. The online comparison page shows recorded outputs only. The runnable Python demo processes new text locally. Use fictional data while evaluating behavior.

To compare policies from Python without starting the UI, run this from the repository root:

```python
from demo.app import POLICIES, SAMPLE, mask

for policy in POLICIES:
    output, details = mask(SAMPLE, policy)
    print(policy)
    print(output)
    print(details["revision"])
```

The demo pins v02 weights revision `28644718923ae38b0105c9f3d2be57312ad0ced3`. The model ID is `halilneed/turkish-pii-detection`. The older `examples/mask.py` intentionally retains its historical v01 default; pass `--revision` explicitly when using it for v02.

## Actual recorded outputs

Recorded on 5 October 2026, CPU, PyTorch 2.8.0+cpu, Transformers 4.56.1, Gradio 5.49.1.


Input:

```text
müşteri Ayşe Yılmaz tc 12345678901 tel 0532 111 22 33 e-posta demo@example.com.
```


### Mask all / Tümünü maskele

Instruction:

```text
Metindeki tüm kişisel verileri uygun etiketlerle maskele.
```

Actual output:

```text
müşteri [AD] tc [TCKN] tel [TEL] e-posta [EMAIL].
```


### Phone only / Yalnızca telefonu maskele

Instruction:

```text
Metindeki yalnızca telefon numaralarını maskele; diğer tüm bilgileri olduğu gibi koru.
```

Actual output:

```text
müşteri Ayşe Yılmaz tc 12345678901 tel [TEL] e-posta demo@example.com.
```


### Keep names / İsim hariç tümünü maskele

Instruction:

```text
Metindeki kişi isimleri hariç tüm kişisel verileri uygun etiketlerle maskele. Kişi isimlerini olduğu gibi koru.
```

Actual output:

```text
müşteri Ayşe Yılmaz tc [TCKN] tel [TEL] e-posta [EMAIL].
```

These are functional checks on one fictional input, not a rerun of the 1,000-row benchmark or an estimate of real-document reliability. Generation is deterministic (`do_sample=False`), but hardware and library versions can affect results. The local check records its package versions; a hosted inference version was not deployed because HF rejected CPU and ZeroGPU creation for this account.

## How the prompt is constructed

The input begins with the tokenizer's BOS token and uses Gemma turn markers:

```text
<BOS><start_of_turn>user
<Turkish masking instruction>

Metin: <Turkish text><end_of_turn>
<start_of_turn>model
```

The model performs instruction-conditioned Turkish masking. English documentation describes its use; it does not add English detection capability. The tokenizer call uses `add_special_tokens=False` to avoid duplicating the BOS token. The end-of-turn token ends generation; only tokens after the input are decoded.

## Failure cases and output review

- Missing fields: verify that the fields selected by the policy were actually masked.
- Unnecessary masking: check that phone-only masking preserves names and other unselected fields.
- Unexpected edits: compare the surrounding text, punctuation and non-PII content.
- Empty output: the demo reports an error instead of returning a blank success.
- Long output: generation stops at 512 tokens; the demo warns if that limit is reached without the turn-ending token.
- Invalid input: the demo rejects empty input, unknown policies, more than 1,500 characters and more than 1,024 prompt tokens. It does not silently truncate the input.

Known weaker release slices include multiple people, Turkish suffixes and uppercase text. Context-free short fragments may be missed. Restricted policies deliberately preserve some PII, and masking does not by itself establish anonymization or legal compliance.

For a synthetic failure case, [open an issue](https://github.com/halilneed/turkish-pii-detection/issues/new?template=masking-failure.md) with the instruction, fictional input, output, model revision and package versions. Read the [evaluation guide](evaluation.md) before measuring task-specific leakage or preservation.

## Resources

- [Turkish PII detection model, weights, bilingual documentation and reported benchmark](https://huggingface.co/halilneed/turkish-pii-detection)
- [Recorded Turkish PII masking examples](https://huggingface.co/spaces/halilneed/turkish-pii-detection-demo)
- [v02 release and model-selection boundary](v02-release.md)
- [Demo installation and hosting notes](../demo/README.md)

Original guide and demo code: MIT. Model weights: [Gemma Terms of Use](https://ai.google.dev/gemma/terms).
