import sys
import os

# Добавляем родительскую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from settings.settings import DB_PATH

cur = sqlite3.connect(DB_PATH).cursor()

def __init_file_draft_table():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS file_draft (
        id INTEGER PRIMARY KEY,
        number INTEGER,
        fio TEXT,
        name_lastname TEXT,
        dat_lastname TEXT,
        company TEXT,
        post TEXT,
        dat_post TEXT,
        phone TEXT,
        email TEXT,
        in_base BOOL,
        in_conf TEXT,
        in_ban_list BOOL,
        last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )