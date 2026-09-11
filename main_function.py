from docx import *
import re
from components.del_space import del_extra_space
from components.all_first_word import all_first_word_func
from components.phonedetector import phone_finder
from components.emaildetector import email_finder
from components.name_lastname import name_lastname
from morfy.morfology_name import convert_name
from morfy.morfology_comp import convert_dol
from component_to_db.workwithdb import max_people_number, in_conf_list
from components.find_in_base import check_in_data, check_in_data_company
from components.to_norm_vid import restore_company


all_word = all_first_word_func()
pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, all_word)) + r')\b', re.IGNORECASE)

def read_docx(table):
    try:
        data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                pre_data = del_extra_space(cell.text)
                row_data.append(pre_data)
            data.append(row_data)
        return data
    except Exception as e:
        return f'Кажется что-то пошло не так :( \n Ошибка: \n {e}'



def convert_data(path) -> list:
    try:
        list_ = read_docx(Document(path).tables[0])
        if not all(len(x) == 5 for x in list_):
            return f'Кажется что-то пошло не так :( \n Ошибка: \n Неподходящая ширина таблицы'
    except Exception as e:
        return f'Кажется что-то пошло не так :( \n Ошибка: \n{e}'
    max_number = max_people_number()

    all_data = []
    for line in list_:
        nn = line[0]
        name = line[1]
        comp_post = line[2]
        email_phone = line[4]
        
        math = pattern.search(comp_post)
        if math:
            company = comp_post[:math.start()].strip().replace('"', ' ').replace('«', ' ').replace('»', ' ')
            post = comp_post[math.start():].strip()
        else:
            company = 'ОШИБКА'
            post = 'ОШИБКА'

        already_in, zz = check_in_data(name, company) # относится к человеку и его компании
        company = restore_company(company) # нормализую название компании которую распознало
        db_comp = zz if zz else check_in_data_company(company) # тут ищу совпадение просто компании если не нашлость совпадение с человеком
        company = db_comp if db_comp else company # тут в приоритете ставлю если нашлась компания вместе с челоеком внутри


        if not already_in:
            # если нет то присваиваю максимальный посдений +1
            max_number += 1
            number = max_number
        else:
            number = already_in
        in_base = True if already_in else False
        in_conf = in_conf_list(already_in) if already_in else ''
        if len(name.split()) > 1:
            cur_name = ' '.join([name.split()[0].upper()] + name.split()[1:])
        else:
            cur_name = name
        # print(name)
        new_line = [
            number, #номер
            cur_name.title(), #фио
            name_lastname(name), #уважаемый илья евгеньевич
            convert_name(name), #беляеву е.е.
            company, # название компании
            post.capitalize(), # должность
            convert_dol(post).capitalize(), # должность в дат падеже
            phone_finder(email_phone), # телефон
            email_finder(email_phone), # почта
            in_base, # в базе или нет
            in_conf # учвстие в конф
        ]
        all_data.append(new_line)

    return all_data
