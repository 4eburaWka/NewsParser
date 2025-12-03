import pymorphy3


def preproccess_post(post: str, remove_punctuation=False) -> str:
    if remove_punctuation:
        post = (
            post.replace(".", "")
            .replace(",", "")
            .replace("!", "")
            .replace("?", "")
            .replace("/", "")
            .replace("@", "")
            .replace("#", "")
            .replace("$", "")
            .replace("%", "")
            .replace("^", "")
            .replace("&", "")
            .replace("*", "")
            .replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace("{", "")
            .replace("}", "")
            .replace("'", "")
            .replace('"', "")
            .replace("«", "")
            .replace("»", "")
        )
    return (
        post.replace("**", "")
        .replace("--", "")
        .replace("__", "")
        .replace("||", "")
        .replace("```", "")
        .replace("~~", "")
        .lower()
    )


morph = pymorphy3.MorphAnalyzer()


def normalize_keywords(
    text: list[str] | str
) -> list[str]:
    if exceptions is None:
        exceptions = []

    if isinstance(text, str):
        text = preproccess_post(text, True).split()
    return [
        (
            morph.parse(keyword.lower())[0].normal_form
        )
        for keyword in text
    ]


def normalize_keyphrases(phrases: list[str] | str):
    if isinstance(phrases, str):
        phrases = phrases.split(",")
    return [" ".join(normalize_keywords(phrase.split())) for phrase in phrases]


def is_subsequence(phrase: list[str], text: list[str]) -> bool:
    if not phrase:
        return True

    phrase_len = len(phrase)
    text_len = len(text)
    if phrase_len > text_len:
        return False

    for i in range(text_len - phrase_len + 1):
        if text[i : i + phrase_len] == phrase:
            return True
    return False
