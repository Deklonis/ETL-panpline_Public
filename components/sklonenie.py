import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def morph_analize(text: str) -> list:
    parses = morph.parse(text)
    if not parses:
        return []
    
    p = next((parse for parse in parses if parse.tag.POS in ('NOUN', 'ADJF', 'NPRO', 'PRTF', 'PRTS')), None)
    
    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']

    result = []
    if p:
        for tag in cases:
            form = p.inflect({tag})
            result.append(form.word if form else None)
        
        return result
    else:
        return []
