from translate import Translator


def split_text(input_text, max_length=480):
    parts = []
    for i in range(0, len(input_text), max_length):
        part = input_text[i:i + max_length]
        parts.append(part)
    return parts


def translate(text) :

    translator = Translator(to_lang='tg', from_lang='ru')
    translated_text = ''

    if len(text) > 490 :
        parts = split_text(text)
        for passage in parts :
            tr = translator.translate(passage)
            translated_text += tr
    else :
        translated_text = translator.translate(text)

    return translated_text
