import sqlite3
import pandas as pd

def first_word_post():
    '''Функция первого слова из актульной бд'''
    cur = sqlite3.connect('components/db.db').cursor()
    data = sorted(list(set([x[0].split(' ')[0].lower() for x in cur.execute("""SELECT post FROM peopledb""").fetchall()])))
    return data
