"""Small, inspectable summarization engines. No training is performed."""
import re
from threading import Lock

MODEL_ID = 'google/flan-t5-small'
_model = _tokenizer = None
_lock = Lock()

def words(text):
    return re.findall(r"\b[\w'-]+\b", text)

def sentences(text):
    return [s.strip() for s in re.split(r'\n+|(?<=[!?])\s+|(?<=\.)\s+(?=[A-Z0-9])', text) if s.strip()]

def extractive(text, count=3):
    """Rank event sentences, select top N, then restore chronological order."""
    rows = list(dict.fromkeys(sentences(text)))
    def score(s):
        outcome = bool(re.search(r'\b(won|wins|winner|victory|full time|final score)\b', s, re.I))
        event = len(re.findall(r'\b(goal|scores|scored|wicket|six|four|boundary|penalty|equalizer|touchdown)\b', s, re.I))
        return 5 * outcome + 2 * event + bool(re.search(r'\d', s))
    chosen = sorted(sorted(range(len(rows)), key=lambda i: (-score(rows[i]), i))[:count])
    return ' '.join(rows[i] for i in chosen)

def generate(text, max_new_tokens=80, beams=4):
    global _model, _tokenizer
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    # One inference at a time keeps a small CPU demonstration predictable.
    with _lock:
        if _model is None:
            tok = AutoTokenizer.from_pretrained(MODEL_ID)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
            model.eval()
            _tokenizer, _model = tok, model
        prompt = 'Summarize this sports commentary. Preserve the stated result and key events; do not invent facts. Commentary: ' + text
        encoded = _tokenizer(prompt, return_tensors='pt', truncation=False)
        n = encoded['input_ids'].shape[1]
        if n > 512:
            raise ValueError(f'Input uses {n} tokens including instructions; limit is 512. Shorten the commentary.')
        with torch.inference_mode():
            ids = _model.generate(**encoded, max_new_tokens=max_new_tokens, num_beams=beams, do_sample=False)
        return _tokenizer.decode(ids[0], skip_special_tokens=True), n

def summarize(text, engine='extractive', count=3, max_new_tokens=80, beams=4):
    import time
    started = time.perf_counter()
    if not text.strip(): raise ValueError('Enter commentary first.')
    if len(text) > 12000: raise ValueError('Limit: 12000 characters.')
    if engine not in ('extractive', 'flan-t5'): raise ValueError('Unknown engine.')
    tokens = None
    if engine == 'extractive': output = extractive(text, count)
    else: output, tokens = generate(text, max_new_tokens, beams)
    original, final = len(words(text)), len(words(output))
    source_result = next((s for s in reversed(sentences(text)) if re.search(r"\b(won|wins|final score|full time)\b", s, re.I)), "No explicit result sentence detected.")
    return dict(source_result=source_result, summary=output, engine=engine, model=MODEL_ID if engine=='flan-t5' else 'Rule-based baseline (not an LLM)', input_words=original, output_words=final, reduction_percent=round(100*(1-final/original),1) if original else 0, input_tokens=tokens, latency_ms=round((time.perf_counter()-started)*1000,2), warning='Generated summaries may omit or invent facts. Check names and scores.' if engine=='flan-t5' else 'Selected source sentences; important events may still be omitted.')
