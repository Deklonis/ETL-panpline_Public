from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget
from ui.p_conteiner_2_ui import Ui_Form


class People_contauner(QWidget):
    def __init__(self, mw, cur_data):
        super().__init__()

        self.mw = mw
        self.cur_data = cur_data
        self.number = cur_data[0]
        self.fio = cur_data[1]
        self.io = cur_data[2]
        self.fiorod = cur_data[3]
        comp = cur_data[4]
        self.post = cur_data[5]
        self.postrod = cur_data[6]
        self.tel = cur_data[7]
        self.email = cur_data[8]
        in_base = cur_data[9]
        self.in_conf = cur_data[10]
        

        self.setObjectName("Form")

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.set_style()
        self.ui.comboBox.setMinimumWidth(150)
        self.ui.comboBox.setMinimumHeight(25)
        self.ui.comboBox.addItems(['Уважаемый', 'Уважаемая'])
        if in_base:
            self.ui.number.setStyleSheet('background-color: green;')
        
        self.ui.Del_but.setText('Удалить')
        self.ui.Del_but.setFixedHeight(20)
        self.ui.Del_but.clicked.connect(self.del_people)

        self.set_text()



        self.ui.lineEdit.textChanged.connect(self.update_data)
        self.ui.lineEdit_2.textChanged.connect(self.update_data)
        self.ui.comboBox.currentTextChanged.connect(self.update_data)
        self.ui.lineEdit_3.textChanged.connect(self.update_data)
        self.ui.lineEdit_4.textChanged.connect(self.update_data)
        self.ui.lineEdit_5.textChanged.connect(self.update_data)
        self.ui.lineEdit_6.textChanged.connect(self.update_data)
        self.ui.lineEdit_7.textChanged.connect(self.update_data)
        self.ui.lineEdit_8.textChanged.connect(self.update_data)

    def set_text(self):
        self.ui.number.setText(str(self.number))
        self.ui.lineEdit.setText(self.fio)
        self.ui.lineEdit_2.setText(' '.join(self.io.split()[1:]))
        self.ui.comboBox.setCurrentText(self.io.split()[0])
        self.ui.lineEdit_3.setText(self.fiorod)
        self.ui.lineEdit_4.setText(self.post)
        self.ui.lineEdit_5.setText(self.postrod)
        self.ui.lineEdit_6.setText(self.tel)
        self.ui.lineEdit_7.setText(self.email)
        self.ui.lineEdit_8.setText(self.in_conf)
    
    def del_people(self):
        self.mw.add_ban_list_people(self.number)

    def update_data(self):
        self.cur_data[1] = self.ui.lineEdit.text()
        self.cur_data[2] = self.ui.comboBox.currentText() + ' ' + self.ui.lineEdit_2.text()
        self.cur_data[3] = self.ui.lineEdit_3.text()
        self.cur_data[5] = self.ui.lineEdit_4.text()
        self.cur_data[6] = self.ui.lineEdit_5.text()
        self.cur_data[7] = self.ui.lineEdit_6.text()
        self.cur_data[8] = self.ui.lineEdit_7.text()

    def set_style(self):
        with open('ui/style/people_container.css', 'r') as f:
            file = f.read()
            self.setStyleSheet(file)
