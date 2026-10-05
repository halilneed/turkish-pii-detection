# Building a Small Turkish PII Masking Model: Data, Fine-Tuning, and Failure Cases

> Historical v01 article, based on the model card read on 28 September 2026. Statements below about a future v2 describe the plan at that time. v02 was released on 30 September; see [the current release note](v02-release.md) and [model card](https://huggingface.co/halilneed/turkish-pii-detection). The historical comparison below has not been rewritten as a v02 result.

Turkish PII masking is more than replacing an email address with a placeholder. A useful system needs to identify the relevant information, follow the requested masking scope, and preserve the rest of the message.

That is the task behind [turkish-pii-detection-v01](https://huggingface.co/halilneed/turkish-pii-detection-v01), a small instruction-conditioned model for Turkish text. This article explains the recipe documented in its model card, the published comparison, and the work required to make the next version easier to evaluate and use.

## What the model does

The released model takes a masking instruction and a Turkish text, then generates a transformed version of that text. The card describes 53 PII labels and four instruction modes: full masking, whitelist, blacklist, and out-of-scope behavior.

This fictional example illustrates the task contract, rather than a newly measured prediction:

```text
Instruction: Mask the person's name and email address.
Input:      Başvuran Deniz Kaya; e-posta demo@example.com.
Target:     Başvuran [AD]; e-posta [EMAIL].
```

The target is an illustration; the complete released label vocabulary must be checked before using it in a benchmark. In particular, a teaching dataset that uses `[PERSON]` should not silently be treated as equivalent to a model using another label.

## The documented training recipe

The model card identifies Gemma-3-270m-it as the starting point. It describes continued full fine-tuning on 24,000 synthetic examples, for one epoch with a learning rate of 5e-5. The examples are described as Turkish banking and ERP-style text targeting difficult cases.

These details describe the published recipe. They do not establish a complete reproduction environment. A full training release should also identify the base checkpoint revision, data generator and version, label definitions, tokenizer, optimizer settings, batch size, sequence lengths, random seed, and software environment.

Those details matter when adapting a small model. A reader needs to know both what was changed and how to repeat the comparison. Training time, GPU memory, and hardware-specific speed are not reported here because verified run records are not available for this article.

## Synthetic data and the evaluation boundary

The card states that training templates were written independently from benchmark sentence and instruction patterns, and that overlapping rows were removed during generation. This is useful information to document, but exact deduplication alone cannot demonstrate independence.

Two sentences can differ in names and numbers while retaining the same template. For the next release, template families and source scenarios should be separated across training, development, and final evaluation. If difficult benchmark cases influence new training data, that benchmark should be treated as development evidence; a separate final set is needed for the next release claim.

## What the published numbers show

The existing card reports whole-line exact match on a 1,000-example Turkish masking benchmark:

| Model, as described in the card | Reported exact match |
|---|---:|
| 270M baseline | 0.743 |
| Released model | 0.882 |

These are previously reported synthetic-data results, not a benchmark rerun for this article. The precise baseline revision and raw evaluation artifacts should accompany any reproduction claim. The difference is 13.9 percentage points on this reported metric; it does not mean that 88.2% of real documents are safe to share.

The slice results are more useful for planning improvements than the headline alone. The card reports 0.600 exact match on multiple-person examples, 0.656 on long examples, and 0.758 on suffixed examples. Per-slice sample counts and raw outputs are needed to interpret these results properly.

## Two failures that one score can hide

A transformation can leave information visible that should have been removed. It can also remove information that the task requires us to preserve. Whole-output exact match marks both as failures, but does not explain which problem occurred.

There is an even simpler counterexample: an empty output contains none of the original sensitive strings, yet it also destroys the entire message. For this reason, the proposed evaluation report separates target-information leakage, preservation of non-target content, empty outputs, instruction-scope errors, and execution failures.

Literal checks can help diagnose examples, but they are not complete entity-level evaluation. Partial disclosure, spelling changes, and indirect identification require additional annotation and review.

## What v2 should improve

The next candidate should be compared with the released model on a frozen task policy, with special attention to multiple people, Turkish suffixes, long inputs, and negative examples. Improvements need to hold without introducing regressions in ordinary text or instruction following.

The release package should make the result inspectable: a model card, a working inference example, a documented dataset split, an evaluation command, and a small set of synthetic failure cases. No v2 performance result is available yet.

## Masking and classification are different next steps

A masking model changes text. A classification model can instead help identify which data categories are present and which passages require review. A future Turkish data-classification model would be a separate task and release, with its own labels and evaluation.

Neither a masking output nor a category label determines whether processing or sharing a document is legally permitted. That depends on the context and applicable rules beyond the model's text prediction.

## Try the existing release

The current model and its usage example are available on [Hugging Face](https://huggingface.co/halilneed/turkish-pii-detection-v01). Start with fictional text. Useful feedback includes the instruction, expected behavior, model revision, and a synthetic reproduction of the failure—not a customer document.

Which case would be most useful for the next evaluation: long support messages, several people in one document, or instruction-specific masking?


## Companion resources

The [Turkish PII Detection companion repository](https://github.com/halilneed/turkish-pii-detection) groups an inference example, a small evaluator, and these development notes. The evaluator includes handwritten fixtures to demonstrate its behavior; their scores are not model results. The original training pipeline, data generator, and published benchmark are not included in this companion package.

The inference example follows the published model card's prompt format and records its model revision. It has not yet been executed as part of preparing these resources. A verified reproduction needs an actual run and its environment record.

*Source: the [published model card](https://huggingface.co/halilneed/turkish-pii-detection-v01), read on 28 September 2026. The training recipe and benchmark scores above are reported release information; no model was trained or benchmark rerun while preparing this article.*
