from rapidfuzz import fuzz
import re
import sqlite3
import pandas as pd
import csv

cur = sqlite3.connect('components/db.db').cursor()

def normolise(s: str) -> str:
    if not s:
        return ''
    s = s.lower().strip()
    s = re.sub(r'\{\.mark\}', '', s)
    for ch in ['"', '«', '»', '—', '–', '-', ',', '|', '“', '”']:
        s = s.replace(ch, ' ')
    s = re.sub(r'\s+', ' ', s)
    s = s.strip()
    legal_forms = {
        'общество с ограниченной ответственностью': 'ооо',
        'публичное акционерное общество': 'пао',
        'акционерное общество': 'ао',
        'закрытое акционерное общество': 'зао',
        'открытое акционерное общество': 'оао',
        'производственная компания': 'пк'
    }
    for full, short in legal_forms.items():
        s = s.replace(full, short)
    
    return s


def short_company(s: str) -> str:
    comp = normolise(s).split()
    comp_words = comp[1:]
    # print([x[0] for x in comp_words])
    if len(comp_words) > 2:
        first_letters = ''.join([x[0] for x in comp_words])
        return comp[0]+' '+first_letters
    else:
        return None
    

def strip_legal(s: str) -> str:
    legal = {'ооо', 'ао', 'пао', 'зао', 'оао', 'тпп', 'нгду', 'тд', 'пк'}
    words = [w for w in s.split() if w not in legal]
    return ' '.join(words)

def match_contact_company(a_word: str, b_word: str) -> int:
    a_word = normolise(a_word)
    b_word = normolise(b_word)

    COMMON_NAMES = {
        "компания",
        "завод",
        "центр",
        "холдинг",
        "группа",
        "предприятие",
        "корпорация",
        "фирма",
    }

    if a_word in COMMON_NAMES or b_word in COMMON_NAMES:
        return a_word == b_word
    
    score = fuzz.token_set_ratio(a_word, b_word)
    if score >= 85:
        return True # ставим насколько точно будет совпадения
    
    a_clean = strip_legal(a_word)  # "ритэк"
    b_clean = strip_legal(b_word)

    a_words = set(a_clean.split())
    b_words = set(b_clean.split())
    
    a_key = {w for w in a_words if len(w) > 3}
    b_key = {w for w in b_words if len(w) > 3}
    
    shorter_key = a_key if len(a_key) <= len(b_key) else b_key
    longer_key  = b_key if len(a_key) <= len(b_key) else a_key
    
    if shorter_key and shorter_key.issubset(longer_key):
        return True
    
    if short_company(a_word) == b_word or short_company(b_word) == a_word:
        return True
    
    return False


def check_in_data(fio: str, comp: str):
    '''
    проверяю есть ли конект компании и человека
    те есть человек в определённой компании
    '''
    data = cur.execute("""SELECT people_number, FIO, in_company FROM peopledb""").fetchall()

    for number, db_fio, db_comp in data:
        norm_fio = normolise(fio)
        norm_db_fio = normolise(db_fio)
        fio_score = fuzz.token_sort_ratio(norm_fio, norm_db_fio)
        if fio_score >= 90 and match_contact_company(db_comp, comp):
            return [number, db_comp]
        
    return [None, None] 


def check_in_data_company(comp: str):
    data = cur.execute("SELECT DISTINCT in_company FROM peopledb").fetchall()

    best = None
    best_score = 0
    norm_comp = strip_legal(normolise(comp))

    for (db_comp,) in data:
        # сначала грубая проверка
        if not match_contact_company(db_comp, comp):
            continue

        # потом более строгая оценка — юр. форма уже убрана с обеих сторон
        score = fuzz.token_sort_ratio(
            strip_legal(normolise(db_comp)),
            norm_comp
        )

        if score > best_score:
            best = db_comp
            best_score = score

    if best_score >= 90:
        return best

    return None
