import re

def del_extra_space(text: str) -> str:
    text = text.strip()
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\{\.mark\}', '', text)
    return text