from component_to_db.draft_table import __init_file_draft_table
from select_file_window import start_select_file_window
from main import start_main_window
from component_to_db.workwithdb import is_in_file
from settings.settings import get_settings_data

 
__init_file_draft_table()

if __name__ == "__main__":
    if not is_in_file():
        start_select_file_window()
    else:
        start_main_window(get_settings_data()['file_config']['file_name'],
                          get_settings_data()['file_config']['in_conf_name'],
                          get_settings_data()['file_config']['file_path'],
                          0)




