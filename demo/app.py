"""CPU demo for the pinned v02 model; no prompts or predictions are saved."""
import os
from functools import lru_cache
from time import perf_counter

DEVICE = os.environ.get("PII_DEMO_DEVICE", "cpu")
if DEVICE not in ("cpu", "cuda"):
    raise ValueError("PII_DEMO_DEVICE must be cpu or cuda")
if DEVICE == "cuda":
    import spaces

import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "halilneed/turkish-pii-detection"
MODEL_REVISION = "28644718923ae38b0105c9f3d2be57312ad0ced3"
MAX_CHARACTERS = 1500
MAX_INPUT_TOKENS = 1024
POLICIES = {
    "Mask all / Tümünü maskele": "Metindeki tüm kişisel verileri uygun etiketlerle maskele.",
    "Phone only / Yalnızca telefonu maskele": "Metindeki yalnızca telefon numaralarını maskele; diğer tüm bilgileri olduğu gibi koru.",
    "Keep names / İsim hariç tümünü maskele": "Metindeki kişi isimleri hariç tüm kişisel verileri uygun etiketlerle maskele. Kişi isimlerini olduğu gibi koru.",
}
SAMPLE = "müşteri Ayşe Yılmaz tc 12345678901 tel 0532 111 22 33 e-posta demo@example.com."


@lru_cache(maxsize=1)
def load_model():
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    options = {"revision": MODEL_REVISION}
    if os.environ.get("HF_HOME"):
        options["cache_dir"] = os.path.join(os.environ["HF_HOME"], "hub")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, **options)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32, **options
    ).to(DEVICE).eval()
    end_turn = tokenizer.convert_tokens_to_ids("<end_of_turn>")
    if tokenizer.bos_token is None or end_turn is None or end_turn == tokenizer.unk_token_id:
        raise RuntimeError("The pinned tokenizer is missing Gemma turn tokens.")
    return tokenizer, model, end_turn


def mask(text, policy):
    if not isinstance(text, str) or not text.strip():
        raise gr.Error("Enter fictional Turkish text. / Kurgusal bir Türkçe metin girin.")
    if len(text) > MAX_CHARACTERS:
        raise gr.Error(f"Use at most {MAX_CHARACTERS} characters. / En fazla {MAX_CHARACTERS} karakter kullanın.")
    if policy not in POLICIES:
        raise gr.Error("Choose a masking policy. / Bir maskeleme politikası seçin.")
    tokenizer, model, end_turn = load_model()
    prompt = (
        f"{tokenizer.bos_token}<start_of_turn>user\n{POLICIES[policy]}\n\n"
        f"Metin: {text}<end_of_turn>\n<start_of_turn>model\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    input_tokens = inputs["input_ids"].shape[1]
    if input_tokens > MAX_INPUT_TOKENS:
        raise gr.Error("This text is too long for the demo. / Bu metin demo için çok uzun.")
    started = perf_counter()
    with torch.inference_mode():
        sequence = model.generate(
            **inputs, max_new_tokens=512, do_sample=False,
            eos_token_id=end_turn, pad_token_id=tokenizer.eos_token_id,
        )
    elapsed = perf_counter() - started
    generated = sequence[0, input_tokens:]
    output = tokenizer.decode(generated, skip_special_tokens=True).strip()
    truncated = len(generated) >= 512 and int(generated[-1]) != end_turn
    if not output:
        raise gr.Error("The model returned an empty result. / Model boş bir sonuç üretti.")
    if truncated:
        gr.Warning("Output reached the generation limit and may be incomplete. / Çıktı üretim sınırına ulaştı ve eksik olabilir.")
    return output, {
        "policy_instruction": POLICIES[policy],
        "model": MODEL_ID,
        "revision": MODEL_REVISION,
        "input_tokens": int(input_tokens),
        "generated_tokens": int(len(generated)),
        "generation_seconds": round(elapsed, 3),
        "possibly_truncated": truncated,
    }


if DEVICE == "cuda":
    # ZeroGPU requires CUDA placement at module startup, outside the GPU callback.
    load_model()
    mask = spaces.GPU(duration=30)(mask)

with gr.Blocks(title="Turkish PII Detection and Masking — halilneed", analytics_enabled=False) as demo:
    gr.Markdown("""# Turkish PII Detection and Masking
**270M parameters · Turkish text · three masking policies**

Try the same text with full masking, phone-only masking, or masking that preserves names.
The model generates transformed text; it does not return NER spans.

**Türkçe:** Aynı metinde tüm kişisel verileri, yalnızca telefonu veya isim dışındaki bilgileri maskeleyin.
Çıktı maskelenmiş metindir; modelin hata yapabileceğini göz önünde bulundurun.

[Download the model / Modeli indir](https://huggingface.co/halilneed/turkish-pii-detection)
· [Python guide](https://github.com/halilneed/turkish-pii-detection/blob/main/docs/python-turkish-pii-masking.md)

Use fictional data while evaluating the model. For sensitive documents, run it locally.
Kurgusal veri kullanın. Hassas belgeler için modeli yerel çalıştırın.
""")
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(value=SAMPLE, lines=5, label="Turkish input / Türkçe girdi", info="Up to 1,500 characters / En fazla 1.500 karakter")
            policy = gr.Radio(choices=list(POLICIES), value=next(iter(POLICIES)), label="Masking policy / Maskeleme politikası")
            run = gr.Button("Mask text / Metni maskele", variant="primary")
        with gr.Column():
            output = gr.Textbox(lines=7, label="Model output / Model çıktısı", interactive=False)
            with gr.Accordion("Run details / Çalıştırma ayrıntıları", open=False):
                details = gr.JSON(label="Instruction and recorded model revision")
    gr.Examples(examples=[[SAMPLE, choice] for choice in POLICIES], inputs=[text, policy], cache_examples=False)
    run.click(fn=mask, inputs=[text, policy], outputs=[output, details], api_name="mask", concurrency_limit=1)
    gr.Markdown("""Outputs may miss personal data or change unrelated content. Review every result.
Masking alone does not guarantee anonymization or legal compliance.

Çıktı kişisel verileri kaçırabilir veya ilgisiz içeriği değiştirebilir. Her sonucu kontrol edin.

[Model card, weights and limitations](https://huggingface.co/halilneed/turkish-pii-detection)
· [Source code](https://github.com/halilneed/turkish-pii-detection/tree/main/demo)
· [Model overview](https://halilneed.agency/models/turkish-pii-detection/)
""")

demo.queue(max_size=8, default_concurrency_limit=1)

if __name__ == "__main__":
    demo.launch()
