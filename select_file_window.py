from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from ui.your_file_ui import Ui_Select
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import sys
from component_to_db.workwithdb import in_conf_func



class Select_file(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Select()
        self.ui.setupUi(self)
        self.ui.select_file_wind.setAcceptDrops(True)
        self.ui.select_file_wind.setPlaceholderText('Перетащите сюда файл')
        self.ui.select_file_wind.textChanged.connect(self.only_url)
        self.ui.select_file.clicked.connect(self.only_url_but)
        self.ui.close.clicked.connect(self.close)
        self.ui.next.clicked.connect(self.to_next_window)
        self.ui.conf_comboBox.addItems(in_conf_func())
        self.ui.conf_comboBox.currentTextChanged.connect(lambda x: self.ui.conf.setText(''))
        self.ui.conf.textChanged.connect(lambda x: self.ui.conf_comboBox.setCurrentIndex(0))
        self.currect_file = 0
    
    def only_url(self):
        text = self.ui.select_file_wind.toPlainText()
        if 'file:///' in text and (text[-3:] == 'doc' or text[-4:] == 'docx'):
            file_name = text.split('/')[-1]
            self.currect_file = 1
            self.ui.select_file_wind.blockSignals(True)
            self.ui.select_file_wind.setText(file_name)
            self.ui.select_file_wind.blockSignals(False)
            self.file_path = text.split('///')[1]
        else:
            self.ui.select_file_wind.blockSignals(True)
            self.ui.select_file_wind.setText('Неподходящий файл')
            self.ui.select_file_wind.blockSignals(False)
            self.currect_file = 0
    
    def only_url_but(self):
        file_dialog = QFileDialog(self)
        self.file_path = file_dialog.getOpenFileName(self, 'Выберите файл')[0]
        file_name = self.file_path.split('/')[-1]
        if (file_name[-3:] == 'doc' or file_name[-4:] == 'docx'):
            self.currect_file = 1
            self.ui.select_file_wind.blockSignals(True)
            self.ui.select_file_wind.setText(file_name)
            self.ui.select_file_wind.blockSignals(False)
        else:
            self.ui.select_file_wind.blockSignals(True)
            self.ui.select_file_wind.setText('Неподходящий файл')
            self.ui.select_file_wind.blockSignals(False)
            self.currect_file = 0
    

    def to_next_window(self):
        if self.currect_file and (self.ui.conf.text() or self.ui.conf_comboBox.currentIndex()!=0):
            from main import MainWindow
            try:
                file_name = self.file_path.split('/')[-1]
                in_conf_name = self.ui.conf_comboBox.currentText() or self.ui.conf.text()
                self.mw = MainWindow(file_name, in_conf_name, '/'+self.file_path)
                self.mw.show()
                super().close()
            except ValueError as e:
                error = QMessageBox()
                error.setText(str(e))
                error.setStandardButtons(QMessageBox.StandardButton.Close)
                error.exec()

    def close(self):
        return super().close()


def start_select_file_window():
    app = QtWidgets.QApplication(sys.argv)
    wind = Select_file()
    wind.show()
    sys.exit(app.exec())

# start_select_file_window()
