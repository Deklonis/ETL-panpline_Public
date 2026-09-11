import re
from components.find_in_base import normolise


ORG_FORMS = ['ооо', 'оао', 'зао', 'пао', 'ао', 'уп', 'гуп', 'муп', 'фгуп', 'ип', 'нко', 'ано']

def restore_company(text: str) -> str:
    text = normolise(text).strip()
    pattern = '|'.join(sorted(ORG_FORMS, key=len, reverse=True))
    mat = re.match(rf'^({pattern})\s+(.+)$', text, re.IGNORECASE)
    
    if not mat:
        return f'«{text.capitalize()}»'
    
    opf = mat.group(1).upper()
    name = mat.group(2).capitalize()
    return f'{opf} «{name}»'

