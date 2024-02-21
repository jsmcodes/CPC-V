from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_doctor_dialog_ui import Ui_DoctorDialog
from main_position_dialog import PositionDialog


class DoctorDialog(QDialog):
    def __init__(self, parent, edit:bool=False, doctor_data=None):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.edit = edit
        self.doctor_data = doctor_data
        self.setup_ui()
        self.setup_window()

    def setup_ui(self) -> None:
        self.ui = Ui_DoctorDialog()
        self.ui.setupUi(self)

        self.insert_positions()
        self.ui.cmbox_position.lineEdit().setAlignment(Qt.AlignCenter)
        
        self.ui.cmbox_sex.lineEdit().setAlignment(Qt.AlignCenter)
    
        self.ui.dtedit_birthdate.setDate(QDate.currentDate())
        self.ui.dtedit_birthdate.setMaximumDate(QDate.currentDate())

        self.ui.dtedit_birthdate.dateChanged.connect(self.calculate_age)
        self.calculate_age(QDate.currentDate())

        if self.edit:
            self.doctor_id, self.name, self.position = self.doctor_data
            self.sex, self.age, self.birthdate, self.contact_number, self.address, self.username, self.password = self.fetch_doctor_data(self.doctor_id)

            self.ui.lbl_id.setText(f"Doctor #{self.doctor_id}")
            self.ui.cmbox_position.setCurrentText(self.position)
            self.ui.lnedit_name.setText(self.name)
            self.ui.cmbox_sex.setCurrentText(self.sex)
            self.ui.dtedit_birthdate.setDate(self.birthdate)
            self.ui.lnedit_contact_number.setText(self.contact_number)
            self.ui.txtedit_address.setPlainText(self.address)
            self.ui.lnedit_username.setText(self.username)
            self.ui.lnedit_password.setText(self.password)
        else:
            self.doctor_id = self.get_last_user_id() + 1
            self.ui.lbl_id.setText(f"Doctor #{self.doctor_id}")

        self.connect_functions()

    def fetch_doctor_data(self, doctor_id: int) -> tuple:
        self.database.connect()

        query = f"""
            SELECT
                sex,
                age,
                birthdate,
                contact_number,
                address,
                username,
                password
            FROM
                users
            WHERE
                id = {doctor_id}
        """
        self.database.c.execute(query)

        doctor_data = self.database.c.fetchone()

        self.database.disconnect()

        return doctor_data
        
    def get_last_user_id(self) -> int:
        self.database.connect()

        query = """
            SELECT COUNT(id) 
            FROM users
        """
        self.database.c.execute(query)

        last_user_id = self.database.c.fetchone()

        self.database.disconnect()

        return last_user_id[0]

    def setup_window(self) -> None:
        self.setFixedSize(500, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)

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
    
    def calculate_age(self, birthdate):
            current_date = QDate.currentDate()

            age_years = current_date.year() - birthdate.year()
            age_months = current_date.month() - birthdate.month()

            if age_months < 0:
                age_years -= 1
                age_months += 12

            age_text = f"{age_years}y {age_months}m"
            self.ui.lnedit_age.setText(age_text)

    def get_positions(self) -> list:
        self.database.connect()

        query = """
            SELECT
                name
            FROM
                positions
            WHERE
                name <> 'Receptionist'
            ORDER BY
                name ASC
        """
        self.database.c.execute(query)

        positions = self.database.c.fetchall()

        self.database.disconnect()

        return positions
    
    def insert_positions(self) -> None:
        self.ui.cmbox_position.clear()
        self.ui.cmbox_position.insertItem(0, "+")
        positions = self.get_positions()

        for index, position in enumerate(positions):
            position_index = index + 1
            self.ui.cmbox_position.insertItem(position_index, position[0])

        self.ui.cmbox_position.setCurrentIndex(1)

    def on_position_changed(self, index):
        if index == 0:
            self.ui.cmbox_position.setCurrentIndex(1)

            dialog = PositionDialog(self)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.ui.cmbox_position.disconnect()
                self.insert_positions()
                self.ui.cmbox_position.currentIndexChanged.connect(self.on_position_changed)

    def handle_add(self) -> None:
        position, name, sex, birthdate, age, contact_number, address, username, password = self.get_doctor_data()

        if name and birthdate!= QDate.currentDate() and len(contact_number) == 17 and address:
            doctor_data = (position, name, sex, birthdate, age, contact_number, address, username, password)
            if self.edit:
                self.update_doctor_data(doctor_data)
                self.accept()
            else:
                self.insert_doctor_data(doctor_data)
                self.accept()

    def insert_doctor_data(self, doctor_data) -> None:
        try:
            self.database.connect()

            position, name, sex, birthdate, age, contact_number, address, username, password = doctor_data

            position_query = f"SELECT id FROM positions WHERE name = '{position}'"
            self.database.c.execute(position_query)
            position_id = self.database.c.fetchone()[0]

            query = f"""
                INSERT INTO users (
                    position_id,
                    name,
                    sex,
                    birthdate,
                    age,
                    contact_number,
                    address,
                    username,
                    password
                )
                VALUES (
                    {position_id},
                    '{name}',
                    '{sex}',
                    '{birthdate}',
                    '{age}',
                    '{contact_number}',
                    '{address}',
                    '{username}',
                    '{password}'
                )
            """
            self.database.c.execute(query)
            self.database.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.database.disconnect()

    def update_doctor_data(self, doctor_data) -> None:
        try:
            self.database.connect()

            position, name, sex, birthdate, age, contact_number, address, username, password = doctor_data

            position_query = f"SELECT id FROM positions WHERE name = '{position}'"
            self.database.c.execute(position_query)
            position_id = self.database.c.fetchone()[0]

            query = f"""
                UPDATE users
                SET
                    position_id = {position_id},
                    name = '{name}',
                    sex = '{sex}',
                    age = '{age}',
                    birthdate = '{birthdate}',
                    contact_number = '{contact_number}',
                    address = '{address}',
                    username = '{username}',
                    password = '{password}'
                WHERE
                    id = {self.doctor_id}
            """
            self.database.c.execute(query)
            self.database.conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.database.disconnect()

    def get_doctor_data(self) -> tuple:
        position = self.ui.cmbox_position.currentText()
        name = self.ui.lnedit_name.text().strip()
        sex = self.ui.cmbox_sex.currentText()
        birthdate = self.ui.dtedit_birthdate.date().toPyDate()
        age = self.ui.lnedit_age.text()
        contact_number = self.ui.lnedit_contact_number.text().strip()
        address = self.ui.txtedit_address.toPlainText().strip()
        username = self.ui.lnedit_username.text().strip()
        password = self.ui.lnedit_password.text().strip()

        return position, name, sex, birthdate, age, contact_number, address, username, password

    def handle_reset(self):
        if self.edit:
            self.ui.cmbox_position.setCurrentText(self.position)
            self.ui.lnedit_name.setText(self.name)
            self.ui.cmbox_sex.setCurrentText(self.sex)
            self.ui.dtedit_birthdate.setDate(self.birthdate)
            self.ui.lnedit_contact_number.setText(self.contact_number)
            self.ui.txtedit_address.setText(self.address)
            self.ui.lnedit_username.setText(self.username)
            self.ui.lnedit_password.setText(self.password)
        else:
            self.ui.cmbox_position.setCurrentIndex(1)
            self.ui.lnedit_name.clear()
            self.ui.cmbox_sex.setCurrentText("Female")
            self.ui.dtedit_birthdate.setDate(QDate.currentDate())
            self.ui.lnedit_contact_number.clear()
            self.ui.txtedit_address.clear()
            self.ui.lnedit_username.clear()
            self.ui.lnedit_password.clear()

    def handle_cancel(self):
        self.close()

    def connect_functions(self) -> None:
        self.ui.cmbox_position.currentIndexChanged.connect(self.on_position_changed)

        self.ui.pshbtn_save.clicked.connect(self.handle_add)
        self.ui.pshbtn_reset.clicked.connect(self.handle_reset)
        self.ui.pshbtn_cancel.clicked.connect(self.handle_cancel)