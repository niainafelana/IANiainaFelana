from transformers import pipeline
from utils import detect_language

models = {
    'en': "facebook/bart-large-cnn",
    'fr': "csebuetnlp/mT5_multilingual_XLSum",
}

summarizers = {
    lang: pipeline("summarization", model=mod)
    for lang, mod in models.items()
}

def summarize_text(text, target_lang=None):
    detected_lang = detect_language(text)
    lang = target_lang if target_lang else detected_lang

    summarizer = summarizers.get(lang, summarizers['en'])

    if len(text) > 1000:
        text = text[:1000]  # tronquer si trop long

    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text'], lang
