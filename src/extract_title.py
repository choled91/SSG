def extract_title(markdown):
    header = ""
    if markdown.startswith("#") and not markdown.startswith("##"):
        header +=markdown[1:].replace(" ", "")
        return header
    else:
        raise Exception("No header found")
    
