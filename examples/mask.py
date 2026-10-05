"""Local inference example; not executed during repository preparation.

Prompt format follows the published model card. Use fictional input.
"""
import argparse
import json

MODEL_ID = "halilneed/turkish-pii-detection"
DEFAULT_REVISION = "37f0c06270486017b8498cacbb09658f3eacf150"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True)
    parser.add_argument("--instruction", default="Metindeki tüm kişisel verileri uygun etiketlerle maskele.")
    parser.add_argument("--revision", default=DEFAULT_REVISION)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    args = parser.parse_args()
    if args.max_new_tokens < 1:
        parser.error("--max-new-tokens must be positive")

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, revision=args.revision, dtype="auto", device_map="auto"
    ).eval()
    end_turn = tokenizer.convert_tokens_to_ids("<end_of_turn>")
    if end_turn is None or end_turn == tokenizer.unk_token_id or tokenizer.bos_token is None:
        raise RuntimeError("Expected Gemma turn tokens are missing; inspect tokenizer revision")
    prompt = (
        f"{tokenizer.bos_token}<start_of_turn>user\n{args.instruction}\n\n"
        f"Metin: {args.text}<end_of_turn>\n<start_of_turn>model\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.inference_mode():
        sequence = model.generate(
            **inputs, max_new_tokens=args.max_new_tokens, do_sample=False,
            eos_token_id=end_turn, pad_token_id=tokenizer.eos_token_id,
        )
    generated = sequence[0, inputs["input_ids"].shape[1]:]
    print(json.dumps({
        "model": MODEL_ID,
        "revision": args.revision,
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "output": tokenizer.decode(generated, skip_special_tokens=True).strip(),
        "generated_tokens": int(generated.shape[0]),
        "reached_token_limit": int(generated.shape[0]) >= args.max_new_tokens,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
