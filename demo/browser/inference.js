export const MODEL_REVISION = '28644718923ae38b0105c9f3d2be57312ad0ced3';
export const MAX_CHARACTERS = 800;
export const POLICIES = [
  'Metindeki tüm kişisel verileri uygun etiketlerle maskele.',
  'Metindeki yalnızca telefon numaralarını maskele; diğer tüm bilgileri olduğu gibi koru.',
  'Metindeki kişi isimleri hariç tüm kişisel verileri uygun etiketlerle maskele. Kişi isimlerini olduğu gibi koru.',
];
export const SAMPLE = 'müşteri Ayşe Yılmaz tc 12345678901 tel 0532 111 22 33 e-posta demo@example.com.';

export async function createEngine(runtime, modelPath, options = {}) {
  const { AutoTokenizer, AutoModelForCausalLM, TextStreamer, InterruptableStoppingCriteria } = runtime;
  const tokenizer = await AutoTokenizer.from_pretrained(modelPath, options);
  const model = await AutoModelForCausalLM.from_pretrained(modelPath, {
    ...options, dtype: 'q8',
  });
  const stopper = new InterruptableStoppingCriteria();
  let running = false;
  return {
    interrupt() { stopper.interrupt(); },
    async dispose() { await model.dispose(); },
    async mask(text, policy, onText = () => {}) {
      if (running) throw new Error('A request is already running. / Bir işlem zaten çalışıyor.');
      if (typeof text !== 'string' || !text.trim()) throw new Error('Enter Turkish text. / Türkçe metin girin.');
      if (text.length > MAX_CHARACTERS) throw new Error(`Use at most ${MAX_CHARACTERS} characters. / En fazla ${MAX_CHARACTERS} karakter kullanın.`);
      if (!Number.isInteger(policy) || !POLICIES[policy]) throw new Error('Choose a policy. / Bir politika seçin.');
      const prompt = `<bos><start_of_turn>user\n${POLICIES[policy]}\n\nMetin: ${text}<end_of_turn>\n<start_of_turn>model\n`;
      const inputs = tokenizer(prompt, { add_special_tokens: false });
      const inputLength = inputs.input_ids.dims.at(-1);
      if (inputLength > 512) throw new Error('Shorten this text. / Bu metni kısaltın.');
      stopper.reset();
      running = true;
      let streamed = '';
      const streamer = new TextStreamer(tokenizer, {
        skip_prompt: true, skip_special_tokens: true,
        callback_function: chunk => { streamed += chunk; onText(streamed); },
      });
      try {
        const sequence = await model.generate({
          ...inputs, max_new_tokens: 256, do_sample: false,
          eos_token_id: 106, pad_token_id: 1,
          streamer, stopping_criteria: [stopper],
        });
        const generated = sequence.tolist()[0].slice(inputLength);
        const output = tokenizer.decode(generated, { skip_special_tokens: true }).trim();
        const complete = generated.at(-1) === 106n || generated.at(-1) === 106;
        if (!output) throw new Error('No output was generated. / Çıktı üretilemedi.');
        return { output, complete, generatedTokens: generated.length };
      } finally { running = false; }
    },
  };
}
