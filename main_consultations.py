from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate

from datetime import datetime

from database_manager import DatabaseManager
from UI.main_consultations_ui import Ui_Consultations
from main_consultation_dialog import ConsultationDialog


class Consultations(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.archived = 0
        self.date_checked = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Consultations()
        self.ui.setupUi(self)

        self.ui.tblwdgt_consultations.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tblwdgt_consultations.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.ui.cmbox_status.lineEdit().setAlignment(Qt.AlignCenter)

        self.ui.dtedit_date.setDate(QDate.currentDate())

        self.populate_table()

        self.connect_functions()

    def get_data(self, patient_name, doctor_name, consultation_status, consultation_date) -> list:
        self.database.connect()

        if self.date_checked:
            query = f"""
                SELECT
                    c.id,
                    p.name AS patient_name,
                    u.name AS doctor_name,
                    date,
                    time,
                    status
                FROM
                    consultations AS c
                JOIN
                    patients AS p
                ON
                    c.patient_id = p.id
                JOIN
                    users AS u
                ON
                    c.doctor_id = u.id 
                WHERE
                    p.name LIKE '%{patient_name}%'
                AND
                    u.name LIKE '%{doctor_name}%'
                AND
                    c.date = '{consultation_date}'
                AND
                    c.status LIKE '%{consultation_status}%'
                AND
                    c.archived  = {self.archived}
                ORDER BY
                    id DESC
            """
        else:
            query = f"""
                SELECT
                    c.id,
                    p.name AS patient_name,
                    u.name AS doctor_name,
                    date,
                    time,
                    status
                FROM
                    consultations AS c
                JOIN
                    patients AS p
                ON
                    c.patient_id = p.id
                JOIN
                    users AS u
                ON
                    c.doctor_id = u.id 
                WHERE
                    p.name LIKE '%{patient_name}%'
                AND
                    u.name LIKE '%{doctor_name}%'
                AND
                    c.status LIKE '%{consultation_status}%'
                AND
                    c.archived  = {self.archived}
                ORDER BY
                    id DESC
            """
        self.database.c.execute(query)

        consultations = self.database.c.fetchall()

        self.database.disconnect()

        return consultations
    
    def populate_table(self) -> None:
        self.ui.tblwdgt_consultations.setRowCount(0)
        try:
            patient_name = self.ui.lnedit_patient_name.text()
            doctor_name = self.ui.lnedit_doctor_name.text()
            consultation_status = self.ui.cmbox_status.currentText()
            consultation_date = self.ui.dtedit_date.date().toPyDate()

            if consultation_status == "All":
                consultation_status = ""

            consultations = self.get_data(patient_name, doctor_name, consultation_status, consultation_date)

            for consultation in consultations:
                id, patient_name, doctor_name, date, time, status = consultation
                formatted_date = datetime.strptime(str(date), "%Y-%m-%d").strftime("%b %d, %Y")
                
                time_object = datetime.strptime(str(time), "%H:%M:%S").time()
                formatted_time = time_object.strftime("%I:%M %p")

                row = self.ui.tblwdgt_consultations.rowCount()
                self.ui.tblwdgt_consultations.insertRow(row)
                                
                self.ui.tblwdgt_consultations.setItem(row, 0, QTableWidgetItem(str(id)))
                self.ui.tblwdgt_consultations.setItem(row, 1, QTableWidgetItem(patient_name))
                self.ui.tblwdgt_consultations.setItem(row, 2, QTableWidgetItem(doctor_name))
                self.ui.tblwdgt_consultations.setItem(row, 3, QTableWidgetItem(formatted_date))
                self.ui.tblwdgt_consultations.setItem(row, 4, QTableWidgetItem(formatted_time))
                self.ui.tblwdgt_consultations.setItem(row, 5, QTableWidgetItem(status))


                for col in range(self.ui.tblwdgt_consultations.columnCount()):
                    item = self.ui.tblwdgt_consultations.item(row, col)
                    if item is not None:
                        item.setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Error in populate_table: {e}")
        
    def handle_archived_check(self, state):
        if state == Qt.Checked:
            self.archived = 1
            self.ui.pshbtn_archive.setText("Unarchive")
        else:
            self.archived = 0
            self.ui.pshbtn_archive.setText("Archive")
        self.populate_table()

    def handle_name_search(self):
        names = (self.ui.lnedit_patient_name, self.ui.lnedit_doctor_name)

        for name in names:
            name.textChanged.connect(self.populate_table)

    def handle_date_checked(self, state):
        if state == Qt.Checked:
            self.date_checked = 1
        else:
            self.date_checked = 0
        self.populate_table()

    def handle_reset(self):
        self.ui.chkbx_archived.setCheckState(Qt.Unchecked)
        self.ui.lnedit_patient_name.clear()
        self.ui.lnedit_doctor_name.clear()
        self.ui.cmbox_status.setCurrentIndex(0)
        self.ui.chkbx_date.setCheckState(Qt.Unchecked)
        self.ui.dtedit_date.setDate(QDate.currentDate())

    def handle_add(self):
        dialog = ConsultationDialog(self)
        result = dialog.exec_()

        if result == dialog.Accepted:
            self.populate_table()

    def handle_edit(self):
        selected_item = self.ui.tblwdgt_consultations.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            consultation_id = self.ui.tblwdgt_consultations.item(selected_row, 0).text()
            patient_name = self.ui.tblwdgt_consultations.item(selected_row, 1).text()
            doctor_name = self.ui.tblwdgt_consultations.item(selected_row, 2).text()
            consultation_date = self.ui.tblwdgt_consultations.item(selected_row, 3).text()
            consultation_time = self.ui.tblwdgt_consultations.item(selected_row, 4).text()

            consultation_data = consultation_id, patient_name, doctor_name, consultation_date, consultation_time

            dialog = ConsultationDialog(self, True, consultation_data)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.populate_table()

    def handle_archive(self):
        selected_item = self.ui.tblwdgt_consultations.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            consultation_id = self.ui.tblwdgt_consultations.item(selected_row, 0).text()

            self.update_consultation_archive(consultation_id)
            self.populate_table()

    def update_consultation_archive(self, consultation_id):
        self.database.connect()

        archive = not self.archived

        query = f"""
            UPDATE 
                consultations 
            SET
                archived = {archive}
            WHERE
                id = {consultation_id}
        """

        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def connect_functions(self):
        self.ui.chkbx_archived.stateChanged.connect(self.handle_archived_check)

        self.handle_name_search()

        self.ui.cmbox_status.currentTextChanged.connect(self.populate_table)

        self.ui.chkbx_date.stateChanged.connect(self.handle_date_checked)

        self.ui.pshbtn_reset.clicked.connect(self.handle_reset)

        self.ui.pshbtn_add.clicked.connect(self.handle_add)
        self.ui.pshbtn_edit.clicked.connect(self.handle_edit)
        self.ui.pshbtn_archive.clicked.connect(self.handle_archive)