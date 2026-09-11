from petrovich.main import Petrovich
import pymorphy3



def convert_name(n: str):
    morph = pymorphy3.MorphAnalyzer()
    p = Petrovich()

    if len(n.split()) >= 3:
        gen = morph.parse(n.split()[2])[0].tag.gender
        d = {
            'masc': 'male',
            'femn': 'female'
        }
        if gen:
            declined = p.lastname(n.split()[0].lower().title(), case=1, gender=d[gen])
        else:
            declined = p.lastname(n.split()[0].lower().title(), case=1, gender='male')
        return (declined + ' ' + n.split()[1][0].lower().title() + '.' + n.split()[2][0] + '.').title()
    else:
        if len(n.split()) == 1:
            return "ОШИБКА"
        declined = p.lastname(n.split()[0].lower().title(), case=1, gender='male')
        return (declined + ' ' + n.split()[1][0].lower().title() + '.').title()
#95% правильности
