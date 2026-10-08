# Turkish PII masking v02: reported results and version selection

Source: the [current model card](https://huggingface.co/halilneed/turkish-pii-detection), read on 5 October 2026, revision `28644718923ae38b0105c9f3d2be57312ad0ced3`. This note documents the publisher's reported results. No model was trained or benchmark rerun while updating this repository.

## What changed

The canonical model ID is now `halilneed/turkish-pii-detection`. The former `turkish-pii-detection-v01` address redirects to it. Unpinned downloads now use v02; use `revision="v01"` for the older release. The companion script retains its existing pinned v01 default so documentation updates do not silently change predictions.

The task remains instruction-conditioned text generation: transform Turkish text according to a masking policy, using the 53-label schema. It does not return NER spans, entity offsets, or KVKK document-classification labels.

## Reported comparison

| Metric / slice | v01 rerun reported in current card | v02 |
| --- | ---: | ---: |
| Whole-row exact match, 1,000 synthetic examples | 0.880 | 0.944 |
| Schema-neutral exact match, 903 examples | 0.900 | 0.951 |
| B partition, 531 examples not used for model selection | 0.885 | 0.945 |
| Long text | 0.656 | 0.844 |
| Multiple people | 0.600 | 0.750 |
| Suffixed personal data | 0.758 | 0.803 |

The historical v01 card reported 0.882 / 0.902. The current card attributes its 0.880 / 0.900 rerun to bf16 batched inference differences. Keep the measurement context when comparing these numbers. Exact match is not entity recall or a guarantee that a real document is safe to share.

## Training and evaluation boundary

The card describes 40,000 generated examples, with 32,864 retained after teacher alignment. Continued full fine-tuning from v01 used one epoch, learning rate 2e-5, and effective batch 32. A 0.5 / 0.5 weight interpolation with v01 was selected after standalone fine-tuning regressed on the benchmark.

Benchmark aggregate feedback influenced development. The interpolation ratio was selected using the A partition (469 rows), the generator's development set and internal probes. The card says the B partition (531 rows) was not used for selection, and benchmark row contents were not used for training or templates. This is a publisher-reported boundary, not an independently verified contamination audit. Training data and evaluation benchmark must be described separately.

## Use a recorded v02 revision

```bash
python examples/mask.py \
  --revision 28644718923ae38b0105c9f3d2be57312ad0ced3 \
  --text 'E-posta demo@example.com; durum açık.' \
  --instruction 'Metindeki e-posta adreslerini maskele; diğer içeriği koru.'
```

The command selects the recorded v02 snapshot, rather than the script's historical default. This inference command was not executed during the documentation update; benchmark, speed, memory and package compatibility were not verified here.

## Resources

- [Model overview and Turkish summary](https://halilneed.agency/models/turkish-pii-detection/)
- [Weights, policy and current model card](https://huggingface.co/halilneed/turkish-pii-detection)
- [Evaluation guide](evaluation.md)
- [Historical v01 training article](how-it-was-built.md)
- [Published Medium article](https://halilneed.medium.com/daha-b%C3%BCy%C3%BCk-model-e%C4%9Fitmedim-zay%C4%B1f-dilimleri-e%C4%9Fittim-f4dcc4afaf5d)
