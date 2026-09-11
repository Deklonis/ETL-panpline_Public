import re
import pandas as pd


def email_finder(newstr: str) -> str:
    '''Ищет почту в строке'''
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if not isinstance(newstr, str):
        return None
    email = re.search(pattern, newstr, re.IGNORECASE)
    return email.group(0) if email else None
