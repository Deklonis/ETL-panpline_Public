from components.find_in_base import check_in_data_company
from component_to_db.workwithdb import insert_data_company, insert_data_people

def to_main_db(new_conf_name, data):
    for cur_data in data:
        fio = cur_data[1]
        io = cur_data[2]
        fiorod = cur_data[3]
        comp = cur_data[4]
        post = cur_data[5]
        postrod = cur_data[6]
        tel = cur_data[7]
        email = cur_data[8]
        number = cur_data[0]
        in_base = cur_data[9]
        in_conf = cur_data[10]
        cur_in_conf = in_conf + ' / ' +  new_conf_name if in_conf else new_conf_name

        if not in_base and comp.lower() != 'ошибка' and fio.lower() != 'ошибка':
            data_to_peopledb = [
                    comp, #делаем запром WHERE in_company = comp
                    fio,
                    io,
                    fiorod,
                    post,
                    postrod,
                    tel,
                    '',
                    email,
                    '',
                    '',
                    cur_in_conf,
                    number
                ]
            if not check_in_data_company(comp):
                
                data_to_data_company = [
                    comp,
                    '',
                    '',
                    '',
                    '',
                    '-'
                ]
                insert_data_company(data_to_data_company)
            insert_data_people(data_to_peopledb)