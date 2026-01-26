from deep_translator import GoogleTranslator
import re

def detect_language(text: str) -> str:
    return 'ru' if any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in text) else 'en'


def translate_query_to_english(query: str) -> str:
    language = detect_language(query)
    if language == 'ru':
        translator = GoogleTranslator(source='ru', target='en')
        return translator.translate(query)
    return query


def translate_response_to_russian(response: str) -> str:
    card_pattern = r'(The [A-Z][a-z]+(?:\s+of\s+[A-Z][a-z]+)?)'
    cards_found = re.findall(card_pattern, response)
    
    temp_response = response
    card_placeholders = {}
    for i, card in enumerate(cards_found):
        placeholder = f"__CARD_{i}__"
        card_placeholders[placeholder] = card
        temp_response = temp_response.replace(card, placeholder, 1)
    
    translator = GoogleTranslator(source='en', target='ru')
    
    # Разбиваем на части если текст большой (Google Translate ограничение)
    max_length = 4500
    if len(temp_response) > max_length:
        parts = temp_response.split('\n\n')
        translated_parts = []
        current_chunk = ""
        
        for part in parts:
            if len(current_chunk) + len(part) < max_length:
                current_chunk += part + '\n\n'
            else:
                if current_chunk:
                    translated_parts.append(translator.translate(current_chunk))
                current_chunk = part + '\n\n'
        
        if current_chunk:
            translated_parts.append(translator.translate(current_chunk))
        
        translated = '\n\n'.join(translated_parts)
    else:
        translated = translator.translate(temp_response)
    

    for placeholder, card in card_placeholders.items():
        translated = translated.replace(placeholder, card)

    return translated
