from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QMenu
from ui.main_ui import Ui_Main
from popele_conteiner import People_contauner
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction
import sys
from main_function import convert_data
from component_to_db.workwithdb import insert_data_file_draft, delete_data_file_draft, select_data_file_draft, add_ban_file_draft, ban_list_file_draft
from components.to_main_db import to_main_db
from settings.settings import get_settings_data, save_settings_data

class MainWindow(QWidget):
    def __init__(self, file_name, in_conf_name, file_path: str = 'РАБОЧИЙ СПИСОК АРМАТУРА.docx', is_from = 1):
        super().__init__()
        '''
        is_from - откуда мы пришли в этот файл, если 1 - то из файла
        выбра ворд файла, если 0 - значит пришли из черновика 
        '''

        closed = QtCore.pyqtSignal()
        if is_from == 1:
            self.file_path = file_path
            convertdata = convert_data(self.file_path)

            if not isinstance(convertdata, list):
                raise ValueError(convertdata)
            
            delete_data_file_draft()

            self.data = convertdata[1:] #№№,ФИО,ИО,ФИОРодП,Компания,Должность,ДолжностьПадеж,Телефон,Почта
            self.company = sorted(set([x[4] for x in self.data]))
            self.ban_list_people = []
        
        if is_from == 0:
            self.file_path = file_path
            self.ban_list_people = ban_list_file_draft()
            self.data = select_data_file_draft()
            self.company = sorted(set([x[4] for x in self.data]))
        
        self.ban_list_company = []
        self.in_conf_name = in_conf_name


        self.isdraft = False
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.ui.listView.setMinimumWidth(220)
        self.ui.listView.setMaximumWidth(260)
        
        self.set_style()
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: black;")
        self.ui.verticalLayout.insertWidget(1, line)
        self.ui.label_2.setText("v. 1.0.0     Импорт из WORD")

        
        self.ui.listView.clicked.connect(self.add_windet)
        self.ui.label.setText(file_name)
        self.ui.label_5.setText(in_conf_name)
        self.ui.label_6.setText('')
        self.ui.pushButton_3.setText('Сохранить')
        self.ui.pushButton_2.clicked.connect(self.to_draft_close)
        self.ui.pushButton.clicked.connect(self.to_crm)
        self.ui.pushButton_3.clicked.connect(self.update_company_name)
        self.ui.lineEdit.textChanged.connect(self.comp_name_changed_update_style_but)
        self.start_method()

    
        
    def start_method(self):
        self.settings()
        self.add_left_comp_list()


    def settings(self):
        self.ui.listView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.listView.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.listView.customContextMenuRequested.connect(self.show_context_menu)
    

    def add_left_comp_list(self):
        self.model = QStandardItemModel()
        self.ui.listView.setModel(self.model)
        for text in self.company:
            self.model.appendRow(QStandardItem(text))


    def show_context_menu(self, pos):
        index = self.ui.listView.indexAt(pos)
        if not index.isValid():
            return 
        menu = QMenu(self)
        delete_action = QAction("Удалить компанию", self)
        delete_action.triggered.connect(lambda: self.delete_company(index))
        menu.addAction(delete_action)
        menu.exec(self.ui.listView.viewport().mapToGlobal(pos))


    def delete_company(self, index):
        company_name = self.model.itemFromIndex(index).text()
        self.model.removeRow(index.row())
        if company_name in self.company:
            self.ban_list_company.append(company_name)
            self.company.remove(company_name)
    #-------------

    def update_company_name(self):
        new_comp_name = self.ui.lineEdit.text()
        for ind in range(len(self.data)):
            if self.data[ind][4] == self.cur_comp:
                self.data[ind][4] = new_comp_name
        for ind in range(len(self.company)):
            if self.cur_comp == self.company[ind]:
                self.company[ind] = new_comp_name
                break
        self.ui.pushButton_3.setStyleSheet("background-color: #E4E7EB;")
        self.add_left_comp_list()


    def add_windet(self, index = 0):
        self.cur_comp = index.data()
        self.index_comp = index
        cur_data = [x for x in self.data if x[4] == self.cur_comp]
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setSpacing(16)
        self.ui.lineEdit.setText(self.cur_comp)
        for _ in range(len(cur_data)):
            if cur_data[_][0] not in self.ban_list_people:

                peop_cont = People_contauner(self, cur_data[_])
                layout.addWidget(peop_cont)
        
        layout.addStretch()
        self.ui.scrollArea.setWidget(container)


    def add_ban_list_people(self, index):
        self.ban_list_people.append(index)
        add_ban_file_draft(index)
        self.add_windet(self.index_comp)

    
    def set_style(self):
        with open('ui/style/mainstyle.css', 'r') as f:
            file = f.read()
            self.setStyleSheet(file)
    

    def to_draft_close(self):
        '''
        когда нажимаем кнопку отложить
        '''
        delete_data_file_draft()
        settings = get_settings_data()
        settings['file_config']['file_name'] = self.ui.label.text()
        settings['file_config']['in_conf_name'] = self.ui.label_5.text()
        settings['file_config']['file_path'] = self.file_path
        save_settings_data(settings)
        data_to_db = []
        for i in self.data:
            if i[0] in self.ban_list_people:
                i.append(1)
            else:
                i.append(0)
            if i[4]!='ОШИБКА' and len(i) == 12 and i[4] not in self.ban_list_company:
                data_to_db.append(i)
        # print('1212121212121')
        self.isdraft = True
        insert_data_file_draft(data_to_db)
        self.close()


    def closeEvent(self, a0):
        '''
        когда нажимаем кнопку закрыть
        '''
        if self.isdraft:
            return super().closeEvent(a0)
        else:
            delete_data_file_draft()
            settings = get_settings_data()
            settings['file_config']['file_name'] = ''
            settings['file_config']['in_conf_name'] = ''
            settings['file_config']['file_path'] = ''
            save_settings_data(settings)
            return super().closeEvent(a0)
    

    def comp_name_changed_update_style_but(self):
        '''
        обновление цвета кнопики при изменении названия компании
        '''

        if self.cur_comp != self.ui.lineEdit.text():
            self.ui.pushButton_3.setStyleSheet("background-color: green;")
        else:
            self.ui.pushButton_3.setStyleSheet("background-color: #E4E7EB;")
    

    def to_crm(self):
        '''
        отправление данных в базу данных
        '''
        to_main_db(self.in_conf_name, self.data)
        self.close()



def start_main_window(file_name, in_conf, file_path, is_from):
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow(file_name, in_conf, file_path, is_from)
    mw.show()
    sys.exit(app.exec())