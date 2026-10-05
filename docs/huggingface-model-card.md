---
language:
- tr
license: gemma
base_model: cagrigungor/pii-guard-turkish-270m
pipeline_tag: text-generation
library_name: transformers
tags:
- pii
- pii-detection
- turkish-nlp
- personal-data
- data-redaction
- anonymization
- masking
- kvkk
- gdpr
- turkish
- privacy
- on-device
model-index:
- name: turkish-pii-detection
  results:
  - task:
      type: text-generation
      name: Instruction-conditional PII masking
    dataset:
      name: Turkish PII Masking Benchmark (1,000 rows)
      type: cagrigungor/turkish-pii-masking-benchmark
      split: test
    metrics:
    - type: exact_match
      name: Row-level exact match (all 1,000 rows)
      value: 0.944
    - type: exact_match
      name: Row-level exact match, schema-neutral (903 rows)
      value: 0.951
---

# Turkish PII Detection and Masking — Türkçe Kişisel Veri Maskeleme (v02)

**By [halilneed](https://halilneed.github.io/).** A 270M instruction-conditioned model for Turkish PII detection and masking. It generates transformed text according to a masking policy: full masking, selected fields, or everything except specified fields. It does not return NER spans or entity offsets. Local inference is supported; validate outputs on representative data before use.

[Model overview / Türkçe özet](https://halilneed.github.io/models/turkish-pii-detection/) · [Python examples and evaluation guide](https://github.com/halilneed/turkish-pii-detection) · [v02 release notes](https://github.com/halilneed/turkish-pii-detection/blob/main/docs/v02-release.md)


Türkçe metindeki kişisel verileri, metin bir LLM'e, log deposuna ya da üçüncü tarafa gitmeden önce maskeleyen 270M parametrelik model. Maskeleme politikasını talimat olarak okur: tümünü maskele, yalnızca şu alanları, şunlar hariç hepsini.

Bu repo daha önce `turkish-pii-detection-v01` adıyla yayındaydı; eski adres buraya yönlendirir. **v01** `revision="v01"` ile aynen erişilebilir. v02, v01'in devamıdır; aynı benchmark'ta **0.880'den 0.944'e** çıktı ve tüm dilimlerde iyileşti; en büyük kazanç uzun metinde (0.656 → 0.844) ve tuzaklarda (0.865 → 0.950).

```
Girdi : MÜŞTERİ SELİM ÖNAL TC 28459163012 TEL 05357213344, İŞYERİ ARÇELİK
Çıktı : MÜŞTERİ [AD] TC [TCKN] TEL [TEL], İŞYERİ [ISYERI]
```

Kullanım örnekleri ve değerlendirme aracı: [github.com/halilneed/turkish-pii-detection](https://github.com/halilneed/turkish-pii-detection)

v01'in nasıl eğitildiği ve hangi dilimlerin gerilediği: [Daha büyük model eğitmedim, zayıf dilimleri eğittim](https://halilneed.medium.com/daha-b%C3%BCy%C3%BCk-model-e%C4%9Fitmedim-zay%C4%B1f-dilimleri-e%C4%9Fittim-f4dcc4afaf5d) (Medium)

Maskeleme öncesi kategori tespiti: [halilneed/turkish-kvkk-classifier](https://huggingface.co/halilneed/turkish-kvkk-classifier) · değerlendirme seti: [halilneed/turkish-kvkk-classification-benchmark](https://huggingface.co/datasets/halilneed/turkish-kvkk-classification-benchmark)

Bankacılık veri sınıfı (hassas veri, müşteri sırrı, banka sırrı — BSEBY): [halilneed/turkish-bseby-classifier](https://huggingface.co/halilneed/turkish-bseby-classifier)

## Sonuçlar

Benchmark: [cagrigungor/turkish-pii-masking-benchmark](https://huggingface.co/datasets/cagrigungor/turkish-pii-masking-benchmark) — 1.000 sentetik test örneği, satır düzeyi tam eşleşme.

Bu veri seti değerlendirme benchmark’ıdır; eğitim verisi olarak listelenmez. Eğitimde kullanılan sentetik veri ve benchmark’ın geliştirme sırasında nasıl kullanıldığı aşağıdaki bölümlerde ayrı açıklanır. Tam eşleşme, varlık düzeyinde recall ya da gerçek belgelerin paylaşılmasının güvenli olduğu anlamına gelmez.

| | v01 | **v02** |
|---|---|---|
| **Tam eşleşme (1.000)** | 0.880 | **0.944** |
| **Şema-nötr (903)** | 0.900 | **0.951** |
| Benchmark'ın B yarısı (531, seçimde hiç kullanılmadı) | 0.885 | **0.945** |
| Tam maskeleme | 0.851 | 0.917 |
| Beyaz liste | 0.895 | 0.940 |
| Kara liste | 0.893 | 0.967 |
| Kapsam dışı | 0.960 | 1.000 |
| PII içermeyen tuzaklar | 0.865 | 0.950 |
| Uzun metin | 0.656 | **0.844** |
| BÜYÜK HARF | 0.775 | 0.838 |
| Ek almış PII ("Cem Aslan'ın") | 0.758 | 0.803 |
| Çok kişili metin | 0.600 | 0.750 |
| Sözle yazılmış sayılar | 0.946 | 1.000 |
| Çok alanlı kayıt | 0.968 | 0.980 |

v01 sütunu bu makinede, aynı değerlendirme betiğiyle yeniden ölçüldü (kartındaki 0.882 / 0.902'den bf16 toplu çıkarım farkıyla 2 satır aşağı).

Aynı benchmark'ta diğer modellerin **kendi kartlarında yayınladıkları** skorlar (yeniden koşulmadı): cagrigungor/pii-guard-turkish-0.8b 0.876 / 0.889 · melikegks/turkish-pii-guard-0.8b şema-nötr 0.922.

### Benchmark nasıl kullanıldı

Eğitim verisi benchmark satırlarına bakılmadan yazıldı ve otomatik kirlilik süzgecinden geçti (benchmark girdisiyle 8 kelimelik ortak dizi ya da birebir aynı talimat içeren satır atıldı). Geliştirme sırasında benchmark'tan toplu geri bildirim alındı: dilim skorları ve bir kez etiket grubu bazında toplu doğruluk. Bu yüzden benchmark id'ye göre ikiye bölündü; interpolasyon oranı A yarısı (469 satır), üreteç dev seti ve kendi yoklama cümlelerimize göre seçildi. **B yarısı (531 satır) seçimde kullanılmadı; temiz karşılaştırma 0.885 → 0.945'tir.** Satır içerikleri hiçbir aşamada eğitim ya da şablon için kullanılmadı.

## Nasıl eğitildi

1. **Sentetik veri üreteci:** 53 etiket, ~1.500 elle yazılmış şablon (bankacılık, İK, sağlık, telekom, e-ticaret, araç, BT logları, uzun e-posta/çağrı dökümü, çok kişili metin, çok alanlı kayıt, ~800 tuzak), ünlü uyumlu ek motoru, Türkçe BÜYÜK HARF / ASCII dönüşümü, sözle yazım ve ~600 farklı politika talimatı. 40.000 örnek.
2. **Öğretmen hizalaması:** Etiket sınırları v01'in sınırlarına hizalandı. v01'in çıktısı girdinin geçerli bir maskelemesiyse ve etiket kümesi aynıysa v01'in sınırları alındı. Anlamsal etiketlerde (sağlık, aile, biyometrik…) v01 ile çelişen 7.136 örnek atıldı. Kalan: 32.864 örnek.
3. **Devam eğitimi:** v01'den full fine-tune, 1 epoch, lr 2e-5, efektif batch 32, loss yalnızca çıktıda.
4. **Ağırlık interpolasyonu (WiSE-FT):** θ = 0.5·θ_fine-tune + 0.5·θ_v01. Tek başına fine-tune benchmark'ta 0.844'e geriledi (üreteç dağılımına kaydı); interpolasyon iki modelin güçlü yanlarını birleştirdi.

## Kullanım

Prompt biçimi v01 ile aynı; başta BOS token gerekir.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "halilneed/turkish-pii-detection"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="auto").eval()
# v01'i birebir kullanmak için: from_pretrained(MODEL, revision="v01")

def maskele(metin, talimat="Metindeki tüm kişisel verileri uygun etiketlerle maskele."):
    prompt = (f"{tokenizer.bos_token}<start_of_turn>user\n{talimat}\n\n"
              f"Metin: {metin}<end_of_turn>\n<start_of_turn>model\n")
    girdi = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(model.device)
    with torch.inference_mode():
        cikti = model.generate(**girdi, max_new_tokens=512, do_sample=False,
                               eos_token_id=tokenizer.convert_tokens_to_ids("<end_of_turn>"),
                               pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(cikti[0, girdi["input_ids"].shape[1]:], skip_special_tokens=True).strip()

print(maskele("müşteri Ayşe Yılmaz tc 12345678901 tel 0532 111 22 33"))
# -> müşteri [AD] tc [TCKN] tel [TEL]
```

CPU'da: `dtype=torch.float32` kullan, `device_map`'i kaldır. Ölçüm: Intel i5-12400F, fp32, 8 iş parçacığı, batch 1 → ~600 ms / cümle (ortalama 50 karakter), ~1.6 GB RAM.

Politikalar ve 53 etiketlik şema v01 ile aynıdır (tam, beyaz liste, kara liste, kategori, kapsam dışı).

## Sınırlar

- Sentetik veriyle değerlendirildi; üretime almadan önce kendi metninde ölç.
- **Bağlamsız kısa parçalarda temkinli:** "vergi numarası 4810271935" tek başına maskelenmeyebilir; kişi bağlamı olan cümlede ("müşterinin vergi numarası …") maskelenir. Tek alanlı kayıtları bağlamla birlikte ver.
- En zayıf dilimler: çok kişili metin (0.750), ek almış PII (0.803), BÜYÜK HARF (0.838).
- Şema dışı etiket üretebilir; çıktıyı etiket listesine karşı doğrula.
- KVKK/GDPR uyumu kullananın sorumluluğundadır. Lisans: [Gemma Terms of Use](https://ai.google.dev/gemma/terms).

## Frequently asked questions / Sık sorulan sorular

**Is this a Turkish NER model?** It generates masked text; it does not return token labels or entity offsets. For structured spans, use a span-based detector instead.

**Can it run locally?** Yes. Download the weights and dependencies first; the usage section includes CPU settings. Published latency measurements apply to the stated hardware and input length.

**How is it different from KVKK classification?** This model transforms text. The separate [Turkish KVKK classifier](https://huggingface.co/halilneed/turkish-kvkk-classifier) predicts data categories, which can inform a masking policy.

**Which version do I get?** The canonical repository serves v02 on `main`. Select `revision="v01"` for the older release or pin a commit SHA to reproduce a specific snapshot. The companion repository's inference example retains its historical v01 default; its quick-start command explicitly selects v02.

**KVKK uyumluluğu sağlar mı?** Maskeleme çıktısı tek başına hukuki uyumluluk veya geri döndürülemez anonimleştirme garantisi vermez. Çıktıyı ve kullanım bağlamını değerlendirin.

## Changelog

- **v02 — 2026-09-30:** 0.944 / 0.951. Yeni üreteç, öğretmen hizalaması, WiSE-FT. Repo `turkish-pii-detection-v01` → `turkish-pii-detection` olarak yeniden adlandırıldı. **Davranış değişikliği:** sürüm sabitlemeden indirenler artık v02'yi alır; v01 için `revision="v01"`.
- **v01 — 2026-09-17:** 0.882 / 0.902 (`revision="v01"`).
