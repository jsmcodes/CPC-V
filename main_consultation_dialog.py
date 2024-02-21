from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3
from datetime import datetime

from database_manager import DatabaseManager
from UI.main_consultation_dialog_ui import Ui_ConsultationDialog
from main_patient_dialog import PatientDialog
from main_doctor_dialog import DoctorDialog


class ConsultationDialog(QDialog):
    def __init__(self, parent, edit:bool=False, consultation_data=None):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.edit = edit
        self.consultation_data = consultation_data
        self.setup_ui()
        self.setup_window()

    def setup_ui(self) -> None:
        self.ui = Ui_ConsultationDialog()
        self.ui.setupUi(self)

        self.ui.cmbox_patient_name.lineEdit().setAlignment(Qt.AlignCenter)
        self.ui.cmbox_doctor_name.lineEdit().setAlignment(Qt.AlignCenter)
        self.insert_patients()
        self.insert_doctors()

        if self.edit:
            self.consultation_id, self.patient_name, self.doctor_name, consultation_date, consultation_time = self.consultation_data

            date_object = datetime.strptime(consultation_date, "%b %d, %Y").date()
            self.qdate = QDate(date_object.year, date_object.month, date_object.day)

            time_object = datetime.strptime(consultation_time, "%I:%M %p").time()
            self.qtime = QTime(time_object.hour, time_object.minute)

            self.ui.lbl_consultation_id.setText(f"Consultation #{self.consultation_id}")
            self.ui.cmbox_patient_name.setCurrentText(self.patient_name)
            self.ui.cmbox_doctor_name.setCurrentText(self.doctor_name)
            self.ui.dtedit_consultation_date.setDate(self.qdate)
            self.ui.tmedit_consultation_time.setTime(self.qtime)
        else:
            consultation_id = self.get_last_consultation_id()[0] + 1
            self.ui.lbl_consultation_id.setText(f"Consultation #{consultation_id}")
            self.ui.dtedit_consultation_date.setDate(QDate.currentDate())
            self.ui.tmedit_consultation_time.setTime(QTime.currentTime())

        self.connect_functions()

    def get_last_consultation_id(self):
        self.database.connect()

        query = """
            SELECT 
                COUNT(id)
            FROM
                consultations
        """
        self.database.c.execute(query)

        last_consultation_id = self.database.c.fetchone()

        self.database.disconnect()

        return last_consultation_id

    def insert_patients(self):
        self.ui.cmbox_patient_name.clear()
        self.ui.cmbox_patient_name.addItem("Add New Patient")
        self.ui.cmbox_patient_name.addItem("Select a patient...")
        self.ui.cmbox_patient_name.model().item(1).setEnabled(False)

        patients = self.fetch_patients()

        for patient in patients:
            self.ui.cmbox_patient_name.addItem(patient[0])

        self.ui.cmbox_patient_name.setCurrentIndex(1)

    def fetch_patients(self):
        self.database.connect()

        query = """
            SELECT
                name
            FROM
                patients
            WHERE
                archived = 0
        """
        self.database.c.execute(query)

        patients = self.database.c.fetchall()

        self.database.disconnect()

        return patients

    def insert_doctors(self):
        self.ui.cmbox_doctor_name.clear()
        self.ui.cmbox_doctor_name.addItem("Add New Doctor")
        self.ui.cmbox_doctor_name.addItem("Select a doctor...")
        self.ui.cmbox_doctor_name.model().item(1).setEnabled(False)

        doctors = self.fetch_doctors()

        for doctor in doctors:
            self.ui.cmbox_doctor_name.addItem(doctor[0])

        self.ui.cmbox_doctor_name.setCurrentIndex(1)

    def fetch_doctors(self):
        self.database.connect()

        query = """
            SELECT
                name
            FROM
                users
            WHERE
                position_id <> 3
            AND
                archived = 0
        """
        self.database.c.execute(query)

        doctors = self.database.c.fetchall()

        self.database.disconnect()

        return doctors

    def setup_window(self) -> None:
        self.setFixedSize(400, 300)
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

    def handle_add_patient(self, index):
        if index == 0:
            self.ui.cmbox_patient_name.setCurrentIndex(1)

            dialog = PatientDialog(False)

            result = dialog.exec_()

            if result == dialog.Accepted:
                self.insert_patients()

    def handle_add_doctor(self, index):
        if index == 0:
            self.ui.cmbox_doctor_name.setCurrentIndex(1)

            dialog = DoctorDialog(False)

            result = dialog.exec_()

            if result == dialog.Accepted:
                self.insert_doctors()
    
    def handle_add(self):
        patient_id, doctor_id, consultation_date, consultation_time = self.get_consultation_data()

        if patient_id and doctor_id:
            if self.edit:
                consultation_data = patient_id, doctor_id, consultation_date, consultation_time
                self.update_consultation(consultation_data)
                self.accept()
            else:
                consultation_data = patient_id, doctor_id, consultation_date, consultation_time
                self.insert_consultation(consultation_data)
                self.accept()

    def get_consultation_data(self):
        patient_name = self.ui.cmbox_patient_name.currentText()
        patient_id = self.get_patient_id(patient_name)[0]
        doctor_name = self.ui.cmbox_doctor_name.currentText()
        doctor_id = self.get_doctor_id(doctor_name)[0]
        consultation_date = self.ui.dtedit_consultation_date.date().toPyDate()
        consultation_time = self.ui.tmedit_consultation_time.time().toPyTime()

        return patient_id, doctor_id, consultation_date, consultation_time

    def insert_consultation(self, consultation_data):
        self.database.connect()

        patient_id, doctor_id, consultation_date, consultation_time = consultation_data

        query = f"""
            INSERT INTO
                consultations (
                    patient_id,
                    doctor_id,
                    date,
                    time
                )
            VALUES (
                {patient_id},
                {doctor_id},
                '{consultation_date}',
                '{consultation_time}'
            )
        """
        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def update_consultation(self, consultation_data):
        self.database.connect()

        patient_id, doctor_id, consultation_date, consultation_time = consultation_data

        query = f"""
            UPDATE
                consultations
            SET
                patient_id = {patient_id},
                doctor_id = {doctor_id},
                date = '{consultation_date}',
                time = '{consultation_time}'
            WHERE
                id = {self.consultation_id}
        """
        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def get_patient_id(self, patient_name):
        self.database.connect()

        query = f"""
            SELECT
                id
            FROM
                patients
            WHERE
                name = '{patient_name}'
        """
        self.database.c.execute(query)

        patient_id = self.database.c.fetchone()

        self.database.disconnect()

        return patient_id
    
    def get_doctor_id(self, doctor_name):
        self.database.connect()

        query = f"""
            SELECT
                id
            FROM
                users
            WHERE
                name = '{doctor_name}'
        """
        self.database.c.execute(query)

        doctor_id = self.database.c.fetchone()

        self.database.disconnect()

        return doctor_id

    def handle_reset(self):
        if self.edit:
            self.ui.cmbox_patient_name.setCurrentText(self.patient_name)
            self.ui.cmbox_doctor_name.setCurrentText(self.doctor_name)
            self.ui.dtedit_consultation_date.setDate(self.qdate)
            self.ui.tmedit_consultation_time.setTime(self.qtime)
        else:
            self.ui.cmbox_patient_name.setCurrentIndex(1)
            self.ui.cmbox_doctor_name.setCurrentIndex(1)
            self.ui.dtedit_consultation_date.setDate(QDate.currentDate())
            self.ui.tmedit_consultation_time.setTime(QTime.currentTime())

    def handle_cancel(self):
        self.close()

    def connect_functions(self):
        self.ui.cmbox_patient_name.currentIndexChanged.connect(self.handle_add_patient)
        self.ui.cmbox_doctor_name.currentIndexChanged.connect(self.handle_add_doctor)
        self.ui.pshbtn_save.clicked.connect(self.handle_add)
        self.ui.pshbtn_reset.clicked.connect(self.handle_reset)
        self.ui.pshbtn_cancel.clicked.connect(self.handle_cancel)