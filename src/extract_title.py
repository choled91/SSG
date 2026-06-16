def extract_title(markdown):
    for headline in markdown.split("\n"):
        if headline.startswith("# "):
            return headline[2:]
    raise ValueError("No h1 heading found")