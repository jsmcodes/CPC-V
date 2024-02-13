from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from UI.main_patient_dialog_ui import Ui_PatientDialog


class PatientDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_window()

    def setup_ui(self):
        self.ui = Ui_PatientDialog()
        self.ui.setupUi(self)

        self.ui.cmbox_sex.lineEdit().setAlignment(Qt.AlignCenter)
        self.ui.dtedit_birthdate.setDate(QDate.currentDate())
        
        self.ui.dtedit_birthdate.dateChanged.connect(self.calculate_age)
        self.calculate_age(QDate.currentDate())

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

    def calculate_age(self, birthdate):
        current_date = QDate.currentDate()

        age_years = current_date.year() - birthdate.year()
        age_months = current_date.month() - birthdate.month()

        if age_months < 0:
            age_years -= 1
            age_months += 12

        age_text = f"{age_years}y {age_months}m"
        self.ui.lnedit_age.setText(age_text)