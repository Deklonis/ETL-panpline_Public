# from petrovich.main import Petrovich <- больше не нужна
import pymorphy3

def name_lastname(namestr: str) -> str:
    morph = pymorphy3.MorphAnalyzer()
    namelist = namestr.split()
    if len(namelist) == 3:
        endfix = namelist[-1][-2:]
        if endfix in ['ич', 'на']:
            d = {
                'ич': 'Уважаемый',
                'на': 'Уважаемая'
            }
            return d[endfix] + ' ' +' '.join(namelist[1:]).lower().title()
        return "ОШИБКА"
    if len(namelist) == 2:
        gen = morph.parse(namelist[1])[0].tag.gender
        if gen in ['masc', 'femn']:
            d = {
                'masc': 'Уважаемый',
                'femn': 'Уважаемая'
            }
            return d[gen] + ' ' +' '.join(namelist).lower().title()
        else:
            return "ОШИБКА"
    return "ОШИБКА"
