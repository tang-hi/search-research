
def whitespace_tokenize(text):
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    for token in tokens:
        yield token

