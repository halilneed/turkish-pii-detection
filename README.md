# Turkish PII Detection and Masking — Türkçe Kişisel Veri Maskeleme

Usage examples, evaluation utilities, and development notes for [halilneed/turkish-pii-detection](https://huggingface.co/halilneed/turkish-pii-detection), a 270M model for instruction-conditioned Turkish PII detection and masking by [halilneed](https://halilneed.agency/). The current release is v02; this repository also preserves historical v01 notes and its pinned inference default.

**Start here:** [Turkish PII detection model and weights](https://huggingface.co/halilneed/turkish-pii-detection) · [interactive browser demo](https://huggingface.co/spaces/halilneed/turkish-pii-detection-demo) · [Python tutorial with recorded examples](docs/python-turkish-pii-masking.md) · [model overview](https://halilneed.agency/models/turkish-pii-detection/) · [v02 results and version selection](docs/v02-release.md) · [how the model was built](docs/how-it-was-built.md) · [evaluation guide](docs/evaluation.md) · [report a synthetic failure case](https://github.com/halilneed/turkish-pii-detection/issues/new?template=masking-failure.md)

Türkçe: Model, verilen talimata göre Türkçe metindeki kişisel veri ifadelerini maskeler. Bu depo kullanım örneği, değerlendirme aracı ve geliştirme notlarını bir araya getirir.

## What is included

- A local inference example adapted to the prompt format in the published model card.
- A bilingual CPU [Gradio demo](demo/README.md) and a [Python masking tutorial](docs/python-turkish-pii-masking.md) that compare three policies using actual model outputs.
- An [interactive browser demo](demo/browser/README.md) with editable input and client-side ONNX inference; original weights and historical defaults are preserved.
- A dependency-free evaluator for supplied outputs, with deliberately handwritten fixtures.
- An article explaining the documented training recipe and its evaluation limitations.
- A scoped roadmap for the next masking release.

This is a companion repository. The original training pipeline, synthetic-data generator, complete 53-label dictionary, and 1,000-example benchmark are not included. The utilities here do not reproduce the published benchmark.

## What the model does

The release generates transformed text. Its card describes 53 PII labels and full, whitelist, blacklist, and out-of-scope instructions. It does not return entity offsets or document-classification labels.

Illustrative task, not a recorded model prediction:

```text
Instruction: Metindeki e-posta adreslerini maskele; diğer içeriği koru.
Input:       E-posta demo@example.com; durum açık.
Target:      E-posta [EMAIL]; durum açık.
```

Check the released label policy before building strict expected-output tests.

## Try local inference

Use a fresh environment with a Python version supported by the installed PyTorch and Transformers releases:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install torch transformers accelerate
python examples/mask.py --revision 28644718923ae38b0105c9f3d2be57312ad0ced3 --text 'E-posta demo@example.com; durum açık.' --instruction 'Metindeki e-posta adreslerini maskele; diğer içeriği koru.'
```

The first run downloads model files. The command above selects a recorded v02 revision. Without `--revision`, the script retains its historical pinned v01 default (`37f0c06270486017b8498cacbb09658f3eacf150`). Decoding is deterministic. The example was syntax-checked, but model inference has not been executed as part of this repository preparation. No runtime, memory, output, or package-version compatibility result is claimed. The model card's usage example is the source for its prompt format. Record your installed versions and hardware when reporting a run.

## Run the evaluator without downloading a model

Python 3.9+; standard library only:

```bash
cd evaluation
python -m unittest -v
python evaluate.py --cases smoke-cases.jsonl --predictions handwritten-outputs.jsonl
```

These fixtures are deliberately written to demonstrate leakage and unnecessary masking. Their scores are software checks, **not model performance**. See the [evaluation guide](docs/evaluation.md) before supplying model predictions.

## Reported release results

The current model card, read on 5 October 2026, reports the following synthetic-data results. They have **not been rerun in this repository**.

| Metric | v01 rerun reported in current card | v02 |
| --- | ---: | ---: |
| Whole-row exact match, 1,000 examples | 0.880 | 0.944 |
| Schema-neutral exact match, 903 examples | 0.900 | 0.951 |
| B partition, 531 examples not used for model selection | 0.885 | 0.945 |

The historical v01 card reported 0.882 / 0.902. The current card attributes the rerun difference to bf16 batched inference. Benchmark aggregate feedback influenced development; read [the v02 release note](docs/v02-release.md) for the training and selection boundary. Exact match is not entity recall or a privacy guarantee.

## Limitations and feedback

Generative masking can miss data, change unrelated text, or generate unexpected labels. Synthetic evaluation does not establish performance on real documents. Restricted instructions may intentionally leave some data visible. Review outputs; masking alone does not establish anonymization or legal compliance.

Use fictional examples in public issues. Include the instruction, expected and actual outputs, model revision, package versions, and whether the failure is leakage, over-masking, or instruction following. Do not upload customer documents or real personal data.

## Development notes

Read [Building a Small Turkish PII Masking Model](docs/how-it-was-built.md) for the documented recipe and next evaluation priorities. The historical v01 article is included here. A [published Medium article](https://halilneed.medium.com/daha-b%C3%BCy%C3%BCk-model-e%C4%9Fitmedim-zay%C4%B1f-dilimleri-e%C4%9Fittim-f4dcc4afaf5d) is also linked from the model card. Author: [halilneed portfolio](https://halilneed.agency/) · [GitHub](https://github.com/halilneed) · [Medium](https://halilneed.medium.com/).

See the [roadmap](docs/roadmap.md). Documentation improvements do not constitute a new model version.

## Licenses

Original code, documentation, and newly authored synthetic smoke fixtures in this repository are provided under the [MIT license](LICENSE). Model weights and their use remain subject to the model's **Gemma** terms; this repository's MIT license does not relicense the model or any third-party training data. No original training dataset is distributed here.
