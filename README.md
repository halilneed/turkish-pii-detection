# Turkish PII Detection

Usage examples, evaluation utilities, and development notes for [halilneed/turkish-pii-detection-v01](https://huggingface.co/halilneed/turkish-pii-detection-v01), a small model for instruction-conditioned Turkish personal-data masking.

**Start here:** [model and weights](https://huggingface.co/halilneed/turkish-pii-detection-v01) · [how the model was built](docs/how-it-was-built.md) · [evaluation guide](docs/evaluation.md) · [report a synthetic failure case](https://github.com/halilneed/turkish-pii-detection/issues/new?template=masking-failure.md)

Türkçe: Model, verilen talimata göre Türkçe metindeki kişisel veri ifadelerini maskeler. Bu depo kullanım örneği, değerlendirme aracı ve geliştirme notlarını bir araya getirir.

## What is included

- A local inference example adapted to the prompt format in the published model card.
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
python examples/mask.py --text 'E-posta demo@example.com; durum açık.' --instruction 'Metindeki e-posta adreslerini maskele; diğer içeriği koru.'
```

The first run downloads model files. The script defaults to a recorded model revision and deterministic decoding. The example was syntax-checked, but model inference has not been executed as part of this repository preparation. No runtime, memory, output, or package-version compatibility result is claimed. The model card's usage example is the source for its prompt format. Record your installed versions and hardware when reporting a run.

## Run the evaluator without downloading a model

Python 3.9+; standard library only:

```bash
cd evaluation
python -m unittest -v
python evaluate.py --cases smoke-cases.jsonl --predictions handwritten-outputs.jsonl
```

These fixtures are deliberately written to demonstrate leakage and unnecessary masking. Their scores are software checks, **not model performance**. See the [evaluation guide](docs/evaluation.md) before supplying model predictions.

## Reported release results

The model card, read on 28 September 2026, reports whole-line exact match on 1,000 synthetic Turkish examples:

| Comparison described in the card | Exact match | Schema-neutral subset (903 examples) |
| --- | ---: | ---: |
| 270M baseline | 0.743 | 0.773 |
| Released model | 0.882 | 0.902 |

These historical results have not been rerun here. The precise baseline revision, raw predictions, benchmark distribution and training artifacts are still needed for independent reproduction. Exact match is not entity recall or a privacy guarantee.

## Limitations and feedback

Generative masking can miss data, change unrelated text, or generate unexpected labels. Synthetic evaluation does not establish performance on real documents. Restricted instructions may intentionally leave some data visible. Review outputs; masking alone does not establish anonymization or legal compliance.

Use fictional examples in public issues. Include the instruction, expected and actual outputs, model revision, package versions, and whether the failure is leakage, over-masking, or instruction following. Do not upload customer documents or real personal data.

## Development notes

Read [Building a Small Turkish PII Masking Model](docs/how-it-was-built.md) for the documented recipe and next evaluation priorities. The article is included here; a direct Medium article link will be added after publication. Author: [Halil on GitHub](https://github.com/halilneed) · [Medium](https://hailneed.medium.com/).

See the [roadmap](docs/roadmap.md). Documentation improvements do not constitute a new model version.

## Licenses

Original code, documentation, and newly authored synthetic smoke fixtures in this repository are provided under the [MIT license](LICENSE). Model weights and their use remain subject to the model's **Gemma** terms; this repository's MIT license does not relicense the model or any third-party training data. No original training dataset is distributed here.
