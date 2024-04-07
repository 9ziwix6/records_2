# # # import sys
# # # from PyQt5.QtWidgets import QApplication
# # # from PyQt5.QtGui import QFontDatabase

# # # # Создание экземпляра приложения
# # # app = QApplication(sys.argv)

# # # # Получение списка всех доступных шрифтов
# # # font_db = QFontDatabase()
# # # font_families = font_db.families()

# # # for font_family in font_families:
# # #     print(font_family)

# # # # Завершение приложения
# # # sys.exit(app.exec_())

import json
import os
from PyQt5.QtGui import QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QRadioButton,
    QPushButton, QLabel, QListWidget, QLineEdit, QColorDialog, QMessageBox, QDialog)
from instr import *




path_json_records = "record.json"


class EditDialog(QDialog):
    def __init__(self, parent=None):
        super(EditDialog, self).__init__(parent)

        self.setWindowTitle("Редактировать запись")
        self.layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.clicked.connect(self.save_edit)
        self.layout.addWidget(self.btn_save)

        self.setLayout(self.layout)

    def save_edit(self):
        new_text = self.line_edit.text()
        if new_text:
            current_item = self.parent().list_widget.currentItem()
            current_item.setText(new_text)
            records = self.parent().load_records(path_json_records)
            index = self.parent().list_widget.currentRow()
            records[index] = new_text
            self.parent().save_records(path_json_records, records)
            self.close()



    def showEvent(self, event):
        current_item = self.parent().list_widget.currentItem()
        if current_item:
            self.line_edit.setText(current_item.text())

class MainWin(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.set_appear()

        self.show()

        self.first_power()

        self.setAllrecords()




    def initUI(self):
        self.layout_line = QVBoxLayout()
        self.label_date = QLabel()
        self.line_search = QLineEdit()

        self.line_name = QLineEdit()
        self.layout_line.addWidget(self.line_name)
        self.line_name.setPlaceholderText("Введите текст сюда")
        
        self.list_widget = QListWidget() 
        self.list_widget.itemDoubleClicked.connect(self.edit_record)
        self.layout_line.addWidget(self.list_widget)

        self.btn_record_add = QPushButton('Добавить запись')
        self.btn_record_add.clicked.connect(self.add_record)

        self.btn_record_rem = QPushButton('Удалить запись')
        self.btn_record_rem.clicked.connect(self.rem_record)

        self.btn_list_clear = QPushButton('Очистить список')
        self.btn_list_clear.clicked.connect(self.list_clear)

        self.btn_color = QPushButton('Выбрать цвет')
        self.btn_color.clicked.connect(self.choose_color)
        
        self.line_search.setPlaceholderText("Поиск заметки")
        self.btn_search = QPushButton("Найти заметку")
        self.btn_search.clicked.connect(self.search_record)

        self.layout_line.addWidget(self.btn_record_add)
        self.layout_line.addWidget(self.btn_record_rem)
        self.layout_line.addWidget(self.btn_list_clear)
        self.layout_line.addWidget(self.label_date)
        self.layout_line.addWidget(self.line_search)
        self.layout_line.addWidget(self.btn_search)
        self.layout_line.addWidget(self.btn_color)
        
        self.setLayout(self.layout_line)

    def edit_record(self):
        edit_dialog = EditDialog(parent=self)
        edit_dialog.exec_()

    def setAllrecords(self):
        records = self.load_records(path_json_records)
        for record in records:
            self.list_widget.addItem(record)
            item = self.list_widget.item(self.list_widget.count() - 1)
            font = QFont("Segoe UI", 12)
            item.setFont(font)


    def choose_color(self):
        try:
            color = QColorDialog.getColor()
            if color.isValid():
                self.list_widget.currentItem().setBackground(QColor(color))
        except:
            pass

    def list_clear(self):

        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Warning)
        # setting message for Message Box 
        msg.setText("Внимание!!!\nВы точно хотите удалить все заметки?")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # start the app 
        msg.exec_()
        if msg.clickedButton().text() == 'OK':
            self.list_widget.clear()
            session = []
            with open(path_json_records, "w") as file:
                json.dump(session, file)


    def search_record(self):
        search_text = self.line_search.text()
        items = self.list_widget.findItems(search_text, Qt.MatchContains)
        if items:
            item = items[0]
            self.list_widget.setCurrentItem(item)

    def add_record(self):
        record_text = self.line_name.text()
        if record_text:
            current_datetime = QDateTime.currentDateTime()
            record_with_date = f"{record_text} ({current_datetime.toString('yyyy-MM-dd HH:mm').replace('T', ' ').replace('-', '/')})"
            self.list_widget.addItem(record_with_date)
            self.line_name.clear()
            item = self.list_widget.item(self.list_widget.count() - 1)
            font = QFont("Segoe UI", 12)
            item.setFont(font)
            
            records = self.load_records(path_json_records)
            records.append(record_with_date)
            self.save_records(path_json_records, records)

    def rem_record(self):
        try:
            remove_item = self.list_widget.currentItem()
            confirmation = QMessageBox.question(self, "Подтверждение", "Вы точно хотите удалить запись?",
                                                QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.list_widget.takeItem(self.list_widget.row(remove_item))
                records = self.load_records(path_json_records)
                records.remove(remove_item.text())
                self.save_records(path_json_records, records)
        except:
            pass

    def set_appear(self):
        self.setWindowTitle(title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)
        # self.setStyleSheet("QWidget { background-color: orange; }")



    def first_power(self):
        if os.path.isfile(path_json_records):
            print("файл есть")
        else:
            session = []
            with open(path_json_records, "w") as file:
                json.dump(session, file)



    def load_records(self, filename):
        with open(filename, "r") as file:
            records = json.load(file)
        return records

    def save_records(self, filename, records):
        with open(path_json_records, "w") as file:
            json.dump(records, file)





app = QApplication([])
mw = MainWin()
app.exec_()
