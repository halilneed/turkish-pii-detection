# Evaluation guide

## Included software demonstration

`evaluation/evaluate.py` scores supplied output strings. It neither runs a model nor trains one. The three smoke cases and handwritten outputs were authored for software testing, contain fictional data, and are not a benchmark. Two cases share an input intentionally to demonstrate two different failure modes.

Case records require a unique nonempty `id`, `text`, `expected`, nonempty `slice`, and lists of nonempty strings named `must_remove` and `must_keep`. Prediction records require the matching `id` and an `output` string. Case and prediction ID sets must match exactly; missing outputs cannot silently disappear from the report.

The evaluator reports whole-output exact match, case-sensitive literal leakage, and missing required literals. Each rate includes its denominator, with `null` for an absent denominator. It also groups results by slice. Literal checks cannot detect all entity variants, partial disclosure or semantic changes. Empty output is not a successful masking policy merely because no sensitive literal remains.

## Before comparing model versions

1. Publish the exact label vocabulary and scope policy. Do not treat `[PERSON]` and `[AD]` as interchangeable without a declared mapping.
2. Track data provenance and licensing. Keep training, development, and final evaluation separate by source and template family. Exact deduplication alone is insufficient.
3. Record the base and tuned model revisions, prompts, decoding settings, package versions, and hardware.
4. Freeze the final set before selecting the candidate. If benchmark weaknesses shape training examples, use a separate untouched set for the final claim.
5. Save predictions and execution failures for every case. Report sample counts, exact match, task-specific leakage and preservation review, empty/truncated outputs, and slice results. Report entity precision/recall only with suitable span annotations and an explicit matching policy.

The published 1,000-example benchmark and its raw predictions are not bundled here. The current model card reports v02 results; see [the v02 release note](v02-release.md) for the reported metrics and selection boundary. Those results were not rerun in this companion repository. The earlier 20-example teaching exercise is not included as a 53-label benchmark.
