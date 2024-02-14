from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt

from database_manager import DatabaseManager
from UI.main_patients_ui import Ui_Patients
from main_patient_dialog import PatientDialog


class Patients(QWidget):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.archived = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Patients()
        self.ui.setupUi(self)

        self.ui.tblwdgt_patients.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.patients = self.get_data()
        self.populate_table(self.patients)

        self.connect_functions()

    def get_data(self, filtered=False, value=None) -> tuple:
        try:
            self.database.connect()

            if filtered:
                query = f"""
                    SELECT 
                        id, 
                        name, 
                        sex, 
                        age 
                    FROM 
                        patients 
                    WHERE 
                        name 
                    LIKE 
                        '%{value}%'
                    AND
                        archived = {self.archived}
                """
            else:
                query = f"""
                    SELECT 
                        id,
                        name,
                        sex,
                        age
                    FROM 
                        patients
                    WHERE
                        archived = {self.archived}
                    ORDER BY 
                        id ASC 
                """
            self.database.c.execute(query)

            patients = self.database.c.fetchall()

            return patients
        except Exception as e:
            print(f"Error in get_data: {e}")
        finally:
            self.database.disconnect()

    def populate_table(self, patients) -> None:
        self.ui.tblwdgt_patients.setRowCount(0)
        try:
            for patient in patients:
                id = str(patient[0])
                name = patient[1]
                sex = patient[2]
                age = patient[3]

                row = self.ui.tblwdgt_patients.rowCount()
                self.ui.tblwdgt_patients.insertRow(row)
                
                self.ui.tblwdgt_patients.setItem(row, 0, QTableWidgetItem(id))
                self.ui.tblwdgt_patients.setItem(row, 1, QTableWidgetItem(name.title()))
                self.ui.tblwdgt_patients.setItem(row, 2, QTableWidgetItem(sex))
                self.ui.tblwdgt_patients.setItem(row, 3, QTableWidgetItem(age))

                for col in range(self.ui.tblwdgt_patients.columnCount()):
                    item = self.ui.tblwdgt_patients.item(row, col)
                    if item is not None:
                        item.setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            self.ui.tblwdgt_patients.setRowCount(0)
            print(f"Error in populate_table: {e}")

    def handle_archived_check(self, state):
        if state == Qt.Checked:
            self.archived = 1
            self.ui.pshbtn_archive.setText("Unarchive")
        else:
            self.archived = 0
            self.ui.pshbtn_archive.setText("Archive")
        self.patients = self.get_data()
        self.populate_table(self.patients)

    def handle_name_search(self, text) -> None:
        if text:
            self.patients = self.get_data(True, text)
            self.populate_table(self.patients)
        else:
            self.patients = self.get_data()
            self.populate_table(self.patients)

    def handle_add(self) -> None:
        dialog = PatientDialog(False)
        result = dialog.exec_()

        if result == dialog.Accepted:
            self.patients = self.get_data()
            self.populate_table(self.patients)

    def handle_edit(self) -> None:
        selected_item = self.ui.tblwdgt_patients.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            patient_id = self.ui.tblwdgt_patients.item(selected_row, 0).text()
            name = self.ui.tblwdgt_patients.item(selected_row, 1).text()
            sex = self.ui.tblwdgt_patients.item(selected_row, 2).text()
            
            patient_data = patient_id, name, sex

            dialog = PatientDialog(True, patient_data)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.patients = self.get_data()
                self.populate_table(self.patients)

    def handle_archive(self) -> None:
        selected_item = self.ui.tblwdgt_patients.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            patient_id = self.ui.tblwdgt_patients.item(selected_row, 0).text()

            self.update_patient_archive(patient_id)
            self.patients = self.get_data()
            self.populate_table(self.patients)

    def update_patient_archive(self, patient_id) -> None:
        self.database.connect()

        archive = not self.archived

        query = f"""
            UPDATE patients 
            SET
                archived = {archive}
            WHERE
                id = {patient_id}
        """

        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def connect_functions(self) -> None:
        self.ui.pshbtn_add.clicked.connect(self.handle_add)
        self.ui.pshbtn_edit.clicked.connect(self.handle_edit)
        self.ui.pshbtn_archive.clicked.connect(self.handle_archive)

        self.ui.chkbox_archived.stateChanged.connect(self.handle_archived_check)
        
        self.ui.lnedit_name.textChanged.connect(self.handle_name_search)