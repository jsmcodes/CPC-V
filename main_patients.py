from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt

from create_database import DatabaseManager
from UI.main_patients_ui import Ui_Patients
from main_patient_dialog import PatientDialog


class Patients(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.database = DatabaseManager()
        patients = self.get_data()
        self.populate_table(patients)
        self.connect_functions_to_buttons()

    def setup_ui(self):
        self.ui = Ui_Patients()
        self.ui.setupUi(self)

        self.ui.tblwdgt_patients.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def get_data(self):
        try:
            self.database.connect()

            query = f"USE `{self.database.database_name}`"
            self.database.c.execute(query)

            query = """
                SELECT id,
                    name,
                    sex,
                    age,
                    birthdate
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
        try:
            for patient in patients:
                self.ui.tblwdgt_patients.setRowCount(0)

                id = str(patient[0])
                name = patient[1]
                sex = patient[2]
                age = str(patient[3])
                birthdate = patient[4]
                birthdate_str = birthdate.strftime('%Y-%m-%d')
                birthdate_qdate = QDate.fromString(birthdate_str, 'yyyy-MM-dd')
                birthdate_display = birthdate_qdate.toString('MMM d, yyyy')

                row = self.ui.tblwdgt_patients.rowCount()
                self.ui.tblwdgt_patients.insertRow(row)
                
                self.ui.tblwdgt_patients.setItem(row, 0, QTableWidgetItem(id))
                self.ui.tblwdgt_patients.setItem(row, 1, QTableWidgetItem(name.title()))
                self.ui.tblwdgt_patients.setItem(row, 2, QTableWidgetItem(sex))
                self.ui.tblwdgt_patients.setItem(row, 3, QTableWidgetItem(age))
                self.ui.tblwdgt_patients.setItem(row, 4, QTableWidgetItem(birthdate_display))

                for col in range(self.ui.tblwdgt_patients.columnCount()):
                    item = self.ui.tblwdgt_patients.item(row, col)
                    if item is not None:
                        item.setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            self.ui.tblwdgt_patients.setRowCount(0)
            print(f"Error in populate_table: {e}")

    def handle_add(self):
        dialog = PatientDialog()
        dialog.exec_()

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_add.clicked.connect(self.handle_add)