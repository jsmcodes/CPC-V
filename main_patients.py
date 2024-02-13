from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt

from database_manager import DatabaseManager
from UI.main_patients_ui import Ui_Patients
from main_patient_dialog import PatientDialog


class Patients(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.database = DatabaseManager()
        self.patients = self.get_data()
        self.populate_table(self.patients)
        self.connect_functions_to_buttons()

    def setup_ui(self):
        self.ui = Ui_Patients()
        self.ui.setupUi(self)

        self.ui.tblwdgt_patients.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def get_data(self, filtered=False):
        try:
            self.database.connect()

            query = f"USE `{self.database.database_name}`"
            self.database.c.execute(query)

            if filtered:
                pass
            else:
                query = """
                    SELECT id,
                        name,
                        sex,
                        age
                    FROM patients
                    ORDER BY id ASC
                """
            self.database.c.execute(query)

            patients = self.database.c.fetchall()

            return patients
        except Exception as e:
            print(f"Error in get_data: {e}")
        finally:
            self.database.disconnect()

    def populate_table(self, patients):
        self.ui.tblwdgt_patients.setRowCount(0)
        try:
            for patient in patients:
                id = str(patient[0])
                name = patient[1]
                sex = patient[2]
                age = str(patient[3])

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

    def handle_add(self):
        dialog = PatientDialog(False)
        result = dialog.exec_()

        if result == dialog.Accepted:
            self.patients = self.get_data()
            self.populate_table(self.patients)

    def handle_edit(self):
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

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_add.clicked.connect(self.handle_add)
        self.ui.pshbtn_edit.clicked.connect(self.handle_edit)
