import pymorphy3


def preproccess_post(post: str, remove_punctuation=False) -> str:
    if remove_punctuation:
        post = (
            post
            .replace('.', '')
            .replace(',', '')
            .replace('!', '')
            .replace('?', '')
            .replace('/', '')
            .replace('@', '')
            .replace('#', '')
            .replace('$', '')
            .replace('%', '')
            .replace('^', '')
            .replace('&', '')
            .replace('*', '')
            .replace('(', '')
            .replace(')', '')
            .replace('[', '')
            .replace(']', '')
            .replace('{', '')
            .replace('}', '')
            .replace('\'', '')
            .replace('"', '')
            .replace('«', '')
            .replace('»', '')
        )
    return (
        post
        .replace('**', '')
        .replace('--', '')
        .replace('__', '')
        .replace('||', '')
        .replace('```', '')
        .replace('~~', '')
    )


morph = pymorphy3.MorphAnalyzer()


def normalize_keywords(text: list[str] | str) -> list[str]:
    if isinstance(text, str):
        text = preproccess_post(text, True).split()
    return [morph.parse(keyword.lower())[0].normal_form for keyword in text]
