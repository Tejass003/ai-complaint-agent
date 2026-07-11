"""
app/translator.py
Handles language detection and translation.

Flow:
  Detect language of complaint
  If not English → translate to English for RAG
  After decision → translate email back to original language
"""

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# Supported languages
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
}


def detect_language(text: str) -> str:
    """
    Detects language of input text.
    Returns ISO language code like 'hi', 'en', 'ta'
    """
    try:
        code = detect(text)
        return code
    except LangDetectException:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """
    Translates any language to English.
    Used before RAG search so policy matching works correctly.
    """
    if source_lang == "en":
        return text

    try:
        translated = GoogleTranslator(
            source=source_lang,
            target="en"
        ).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_email(email_text: str, target_lang: str) -> str:
    """
    Translates the drafted email to customer's language.
    So Hindi customer gets Hindi email back.
    """
    if target_lang == "en":
        return email_text

    try:
        translated = GoogleTranslator(
            source="en",
            target=target_lang
        ).translate(email_text)
        return translated
    except Exception as e:
        print(f"Email translation error: {e}")
        return email_text


def get_language_name(code: str) -> str:
    """Returns full name of language from code."""
    return LANGUAGE_NAMES.get(code, "Unknown")


# ── Test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test 1 — Hindi detection
    hindi_text = "मुझे गलत प्रोडक्ट मिला है, रिफंड चाहिए"
    lang = detect_language(hindi_text)
    print(f"Detected: {lang} ({get_language_name(lang)})")

    # Test 2 — Hindi to English
    english = translate_to_english(hindi_text, lang)
    print(f"Translated: {english}")

    # Test 3 — Tamil detection
    tamil_text = "என் தயாரிப்பு சேதமடைந்தது, மாற்று வேண்டும்"
    lang2 = detect_language(tamil_text)
    print(f"\nDetected: {lang2} ({get_language_name(lang2)})")

    english2 = translate_to_english(tamil_text, lang2)
    print(f"Translated: {english2}")

    # Test 4 — Translate email back to Hindi
    email = "Dear Customer, we will replace your product within 3 days."
    hindi_email = translate_email(email, "hi")
    print(f"\nHindi email: {hindi_email}")