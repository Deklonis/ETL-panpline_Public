import re
import pandas as pd


def phone_finder(newstr: str) -> str:
    '''Ищет почту в строке'''
    pattern = r'(\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    if not isinstance(newstr, str):
        return None
    clean = re.sub(r'[^\d \+]', '', newstr)
    phone = re.search(pattern, clean, re.IGNORECASE)
    return re.sub(r'[\s]', '', phone.group(0)) if phone else None