import pymorphy3
import re
from functools import cache


morph = pymorphy3.MorphAnalyzer()


@cache
def ban_list_func():
    first_ban_list = ['отдел', 'управление', 'департамент', 'служба', 'бюро', 'центр', 'проект', 'производство', 'производственно']
    all_ban_list = set()
    for i in first_ban_list:
        pred = []
        for j in ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']:
            scl = morph.parse(i)[0].inflect({j})
            if scl:
                pred.append(scl.word)
                all_ban_list.add(scl.word)
        pred2 = pred.copy()
        for j in pred:
            scl = morph.parse(j)[0].inflect({'plur'})
            if scl:
                pred2.append(scl.word)
                all_ban_list.add(scl.word)
        for j in pred2:
            for gend in ['masc', 'femn', 'neut']:
                scl = morph.parse(j)[0].inflect({gend})
                if scl:
                    all_ban_list.add(scl.word)
            
    ban_list = list(all_ban_list).copy()
    return ban_list

def convert_dol(dol2: str):
    '''Пока не нравится этот момент тк при каждой должность формируется \n
    бан лист а так не должно быть'''
    ban_list = ban_list_func()
    dol2 = re.sub(r'[–——-]', '-', dol2)
    dol2 = re.sub(r'\s+', ' ', dol2)
    dol = dol2.split('-')
    indextire = 0
    if len(dol) > 1:
        indextire = len(dol[0].split())

    all_dol = []
    for wordspl in dol:
        s = []
        word = wordspl.lower().split()
        for i in range(len(word)):
            word_comma = word[i].replace(',', '')

            if word_comma != word[i]:
                has_comma = True  
            else:
                has_comma = False
            
            if not word_comma:
                s.append(word[i])
                continue

            base_word = word[i].replace(',', '')

            if word[i].isdigit():
                s.append(word[i])
                continue


            ptag = str(morph.parse(base_word)[0].tag)
            if (base_word not in ban_list + ['и', 'в', 'на', 'по', 'с', 'из', 'от']) and ('gent' not in ptag and 'ablt' not in ptag):
                parsed = morph.parse(base_word)[0]
                dec = parsed.inflect({'datv'})
                if dec:
                    s.append(dec.word+(',' if has_comma else ''))
                else:
                    s.append(base_word+(',' if has_comma else ''))

            else:
                for j in range(i, len(word)):
                    s.append(word[j])
                break
        all_dol.extend(s)

    if indextire > 0:
        all_dol.insert(indextire, '-')
        return ' '.join(all_dol).lower()
    else:
        return ' '.join(all_dol).lower()