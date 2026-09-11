import sys
import os

# Добавляем родительскую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from settings.settings import DB_PATH



conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()



def in_conf_func():
    data = [x[0] for x in cur.execute("""SELECT in_conf FROM peopledb""").fetchall()]
    all_data = []
    for i in data:
        all_data.extend(i.split(' / '))
    return sorted(set(all_data))



def max_people_number():
    row = cur.execute("""SELECT MAX(people_number) FROM peopledb""").fetchone()
    return row[0] if row else 0


def in_conf_list(number):
    row = cur.execute("""SELECT in_conf FROM peopledb WHERE people_number = ?""", (number, )).fetchone()
    return row[0] if row else 0


def insert_data_file_draft(lines: list):
    for line in lines:
        number = line[0]
        fio = line[1]
        name_lastname = line[2]
        dat_lastname = line[3]
        company = line[4]
        post = line[5]
        dat_post = line[6]
        phone = line[7]
        email = line[8]
        in_base = line[9]
        in_conf = line[10]
        in_ban_list = line[11]
        cur.execute("""
            INSERT INTO file_draft 
            (number, fio, name_lastname, dat_lastname, company, post, 
             dat_post, phone, email, in_base, in_conf, in_ban_list)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (number, fio, name_lastname, dat_lastname, company, post,
              dat_post, phone, email, in_base, in_conf, in_ban_list))
    conn.commit()

def delete_data_file_draft():
    cur.execute("""
        DELETE FROM file_draft
        """)
    conn.commit()


def is_in_file():
    data = cur.execute('''SELECT 1 FROM file_draft LIMIT 1''').fetchall()
    if data:
        return True
    return False


def select_data_file_draft():
    data = cur.execute('''SELECT number, fio, name_lastname, dat_lastname, company, post, 
             dat_post, phone, email, in_base, in_conf FROM file_draft
             ''').fetchall()
    return [list(x) for x in data] if data else [] # тут что-то придумать

def ban_list_file_draft():
    data = cur.execute('''SELECT number FROM file_draft WHERE in_ban_list = 1''').fetchall()
    return [x[0] for x in data] if data else []

def add_ban_file_draft(index):
    cur.execute('''UPDATE file_draft SET in_ban_list = 1 WHERE number = ?''', (index, ))
    conn.commit()



def insert_data_company(comp_data: list):
    cur.execute('''INSERT INTO data_company (comp_name, comp_adress, comp_tel, comp_email, comp_extra, comp_post) VALUES (?, ?, ?, ?, ?, ?)''', (comp_data))
    conn.commit()



def insert_data_people(people_data: list):
    cur.execute('''INSERT INTO peopledb (in_company, FIO, IO, FIO_Dp, post, post_2, tel_1, tel_2, email, post_index, extra, in_conf, people_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (people_data))
    conn.commit()