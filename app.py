from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton,
QLineEdit, QComboBox,QDateEdit, QTableWidget, QVBoxLayout,
QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView)

from PyQt6.QtCore import QDate, Qt
from unicodedata import category

from database import fetch_appointments, add_appointment, delete_appointment

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Calendar Database Viewer')

    # design
    def initUI(self):
        # create all objects
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.start_time = QLineEdit()
        self.end_time = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton('Add Appointment')
        self.btn_delete = QPushButton('Delete Appointment')
        self.btn_delete.setObjectName('btn_delete') # can be used as id in CSS

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Start Time', 'End Time', 'Category', 'Description'])
        # edit table width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_appointment)
        self.btn_delete.clicked.connect(self.delete_appointment)

        self.apply_styles()

        # add widgets to a layout (row/column)
        self.setup_layout()



    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        # row 1
        row1.addWidget(QLabel('Date'))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel('Category'))
        row1.addWidget(self.dropdown)

        # row 2
        row2.addWidget(QLabel('Start Time'))
        row2.addWidget(self.start_time)
        row2.addWidget(QLabel('End Time'))
        row2.addWidget(self.end_time)

        # row 3
        row3.addWidget(QLabel('Description'))
        row3.addWidget(self.description)

        # row 4
        row4.addWidget(self.btn_add)
        row4.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addLayout(row4)
        master.addWidget(self.table)

        self.setLayout(master)

    # you can add CSS style!!
    def apply_styles(self):
        # in setStyleSheet, you can target each individual class
        self.setStyleSheet("""
                            QWidget{
                            background-color: #e3e9f2;
                            font-family: Arial, sans-serif;
                            font-size: 14px;
                            color:#333
                            }
                            QLabel{
                                font-size: 16px;
                                color: #2c3e50;
                                font-weight: bold;
                                padding: 5px;
                            }         
                            QLineEdit, QComboBox, QDateEdit{
                                background-color: #e3e9f2;
                                font-size: 14px;
                                color:#333;
                                border: 1px solid #b0bfc6;
                                border-radius: 15px;
                                padding: 5px;
                            } 
                            QLineEdit:hover, QCombo:hover, QDateEdit:hover{
                                border: 1px solid #4caf50;
                            }
                            QLineEdit:focus, QCombo:focus, QDateEdit:focus{
                                border: 1px solid #2a9d8f;
                                background-color: #f5f9fc;
                            }
                            QTableWidget{
                                background-color: #fff;
                                alternate-background-color: #f2f7fb;
                                gridline-color: #c0c9d0;
                                selection-background-color: #4caf50;
                                selection-color: white;
                                font-size: 14px;
                                border 1px solid #cfd9e1;
                            }
                            
                            """)




    def populate_dropdown(self):
        categories = ['Personal', 'Meals', 'Medical', 'Classes', 'Chores', 'Recreation']
        self.dropdown.addItems(categories)

    def load_table_data(self): # takes the info from our database and projects it into our application
        appointments = fetch_appointments() # returns a list
        self.table.setRowCount(0) # ensure that table starts at 0
        for row_idx, appointment in enumerate(appointments):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(appointment):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.start_time.clear()
        self.end_time.clear()
        self.description.clear()

    def add_appointment(self):
        date = self.date_box.date().toString('yyyy-MM-dd')
        category = self.dropdown.currentText() # QComboBox
        start_time = self.start_time.text() # QLineEdit
        end_time = self.end_time.text()
        description = self.description.text()

        if not start_time or not end_time or not description:
            # QMessageBox.warning(self, 'Input Error', 'Amount and Description can not be empty')
            QMessageBox.warning(self, 'Input Error', 'Times and Description cannot be empty')
            return

        if add_appointment(date, start_time, end_time, category, description):
            self.load_table_data()
            # clear inputs
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "failed to add appointment")

    def delete_appointment(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "you need to choose a row to delete!")
            return

        appointment_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "are you sure you want to delete?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes and delete_appointment(appointment_id):
            self.load_table_data()