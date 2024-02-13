from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_patient_dialog_ui import Ui_PatientDialog


class PatientDialog(QDialog):
    def __init__(self, edit, patient_data=None):
        super().__init__()
        self.database = DatabaseManager()
        self.edit = edit
        self.patient_data = patient_data
        self.setup_ui()
        self.setup_window()
        self.connect_functions_to_buttons()

    def setup_ui(self):
        self.ui = Ui_PatientDialog()
        self.ui.setupUi(self)
            
        self.ui.dtedit_birthdate.dateChanged.connect(self.calculate_age)
        self.calculate_age(QDate.currentDate())

        if self.edit:
            self.patient_id, name, sex = self.patient_data
            birthdate, contact_number, address = self.fetch_patient_data(self.patient_id)

            self.ui.cmbox_sex.lineEdit().setAlignment(Qt.AlignCenter)

            self.ui.lbl_id.setText(f"Patient #{self.patient_id}")
            self.ui.lnedit_name.setText(name)
            self.ui.cmbox_sex.setCurrentText(sex)
            self.ui.dtedit_birthdate.setDate(birthdate)
            self.ui.lnedit_contact_number.setText(contact_number)
            self.ui.txtedit_address.setText(address)
        else:
            self.patient_id = self.get_last_patient_id() + 1
            self.ui.lbl_id.setText(f"Patient #{self.patient_id}")

            self.ui.cmbox_sex.lineEdit().setAlignment(Qt.AlignCenter)
            self.ui.dtedit_birthdate.setDate(QDate.currentDate())

    def fetch_patient_data(self, patient_id):
        self.database.connect()

        query = f"""
            SELECT 
                birthdate,
                contact_number,
                address
            FROM
                patients
            WHERE
                id = {patient_id}
        """
        self.database.c.execute(query)

        patient_data = self.database.c.fetchone()

        self.database.disconnect()

        return patient_data

    def setup_window(self):
        self.setFixedSize(500, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        icon = QIcon()
        pixmap = QPixmap(":/window_icon.ico")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        store_name = self.get_store_name()
        self.setWindowTitle(store_name[0])

    def get_store_name(self) -> str:
        conn = sqlite3.connect("Database/setup.db")
        c = conn.cursor()

        query = """
            SELECT store_name
            FROM setup
        """

        c.execute(query)

        store_name = c.fetchone()

        return store_name

    def calculate_age(self, birthdate) -> str:
        current_date = QDate.currentDate()

        age_years = current_date.year() - birthdate.year()
        age_months = current_date.month() - birthdate.month()

        if age_months < 0:
            age_years -= 1
            age_months += 12

        age_text = f"{age_years}y {age_months}m"
        self.ui.lnedit_age.setText(age_text)

    def get_last_patient_id(self) -> int:
        self.database.connect()

        query = f"USE `{self.database.database_name}`"
        self.database.c.execute(query)

        query = """
            SELECT COUNT(id) 
            FROM patients
        """
        self.database.c.execute(query)

        last_patient_id = self.database.c.fetchone()

        self.database.disconnect()

        return last_patient_id[0]
    
    def handle_save(self):
        id, name, sex, birthdate, age, contact_number, address = self.get_patient_data()

        if name and birthdate != QDate.currentDate() and len(contact_number) == 17 and address:
            patient_data = (id, name, sex, birthdate, age, contact_number, address)
            if self.edit:
                self.update_patient_data(patient_data)
            else:
                self.insert_patient_data(patient_data)
            self.accept()

    def get_patient_data(self):
        id = self.patient_id
        name = self.ui.lnedit_name.text().strip()
        sex = self.ui.cmbox_sex.currentText()
        birthdate = self.ui.dtedit_birthdate.date().toPyDate()
        age = self.ui.lnedit_age.text()
        contact_number = self.ui.lnedit_contact_number.text().strip()
        address = self.ui.txtedit_address.toPlainText().strip()

        return id, name, sex, birthdate, age, contact_number, address

    def insert_patient_data(self, patient_data):
        id, name, sex, birthdate, age, contact_number, address = patient_data

        self.database.connect()

        query = f"""
            INSERT INTO patients (
                id, 
                name, 
                sex, 
                age, 
                birthdate,
                contact_number,
                address
            )
            VALUES (
                {id}, 
                '{name}', 
                '{sex}', 
                '{age}', 
                '{birthdate}',
                '{contact_number}',
                '{address}'
            )
        """
        self.database.c.execute(query)

        self.database.conn.commit()
        self.database.disconnect()

    def update_patient_data(self, patient_data):
        id, name, sex, birthdate, age, contact_number, address = patient_data

        self.database.connect()

        query = f"""
            UPDATE patients
            SET 
                name = '{name}', 
                sex = '{sex}', 
                age = '{age}', 
                birthdate = '{birthdate}',
                contact_number = '{contact_number}',
                address = '{address}'
            WHERE
                id = {id}
        """
        self.database.c.execute(query)

        self.database.conn.commit()
        self.database.disconnect()

    def handle_reset(self):
        if self.edit:
            patient_id, name, sex = self.patient_data
            birthdate, contact_number, address = self.fetch_patient_data(patient_id)

            self.ui.cmbox_sex.lineEdit().setAlignment(Qt.AlignCenter)

            self.ui.lbl_id.setText(f"Patient #{patient_id}")
            self.ui.lnedit_name.setText(name)
            self.ui.cmbox_sex.setCurrentText(sex)
            self.ui.dtedit_birthdate.setDate(birthdate)
            self.ui.lnedit_contact_number.setText(contact_number)
            self.ui.txtedit_address.setText(address)
        else:
            self.ui.lnedit_name.clear()
            self.ui.cmbox_sex.setCurrentIndex(0)
            self.ui.dtedit_birthdate.setDate(QDate.currentDate())
            self.ui.lnedit_contact_number.clear()
            self.ui.txtedit_address.clear()

    def handle_cancel(self):
        self.close()

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_save.clicked.connect(self.handle_save)
        self.ui.pshbtn_reset.clicked.connect(self.handle_reset)
        self.ui.pshbtn_cancel.clicked.connect(self.handle_cancel)