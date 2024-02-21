from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt

from database_manager import DatabaseManager
from UI.main_doctors_ui import Ui_Doctors
from main_doctor_dialog import DoctorDialog


class Doctors(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.archived = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Doctors()
        self.ui.setupUi(self)

        self.ui.tblwdgt_doctors.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tblwdgt_doctors.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.populate_table()
        self.connect_functions()

    def get_data(self, filtered=False, value=None) -> tuple:
        self.database.connect()

        if filtered:
            query = f"""
                SELECT 
                    u.id, 
                    u.name, 
                    p.name
                FROM 
                    users AS u
                JOIN
                    positions AS p
                ON
                    u.position_id = p.id
                WHERE 
                    u.name LIKE '%{value}%'
                AND
                    u.position_id <> 3
                AND
                    u.archived = {self.archived}
                ORDER BY
                    id DESC
            """
        else:
            query = f"""
                SELECT 
                    u.id, 
                    u.name, 
                    p.name
                FROM 
                    users AS u
                JOIN
                    positions AS p
                ON
                    u.position_id = p.id
                WHERE 
                    u.position_id <> 3
                AND
                    u.archived = {self.archived}
                ORDER BY
                    id DESC
            """
        self.database.c.execute(query)

        doctors = self.database.c.fetchall()

        self.database.disconnect()

        return doctors

    def populate_table(self, filtered=False, value=None) -> None:
        self.ui.tblwdgt_doctors.setRowCount(0)

        doctors = self.get_data(filtered, value)

        for doctor in doctors:
            id, name, position = doctor

            row = self.ui.tblwdgt_doctors.rowCount()
            self.ui.tblwdgt_doctors.insertRow(row)
                
            self.ui.tblwdgt_doctors.setItem(row, 0, QTableWidgetItem(str(id)))
            self.ui.tblwdgt_doctors.setItem(row, 1, QTableWidgetItem(name.title()))
            self.ui.tblwdgt_doctors.setItem(row, 2, QTableWidgetItem(position))

            for col in range(self.ui.tblwdgt_doctors.columnCount()):
                item = self.ui.tblwdgt_doctors.item(row, col)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)

    def handle_add(self):
        dialog = DoctorDialog(self)
        result = dialog.exec_()

        if result == dialog.Accepted:
            self.populate_table()

    def handle_edit(self) -> None:
        selected_item = self.ui.tblwdgt_doctors.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            doctor_id = self.ui.tblwdgt_doctors.item(selected_row, 0).text()
            name = self.ui.tblwdgt_doctors.item(selected_row, 1).text()
            position = self.ui.tblwdgt_doctors.item(selected_row, 2).text()

            doctor_data = doctor_id, name, position

            dialog = DoctorDialog(self, True, doctor_data)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.populate_table()

    def handle_archive(self):
        selected_item = self.ui.tblwdgt_doctors.selectedItems()

        if selected_item:
            selected_row = selected_item[0].row()
            doctor_id = self.ui.tblwdgt_doctors.item(selected_row, 0).text()

            self.update_doctor_archive(doctor_id)
            self.populate_table()

    def update_doctor_archive(self, doctor_id) -> None:
        self.database.connect()

        archive = not self.archived

        query = f"""
            UPDATE users 
            SET
                archived = {archive}
            WHERE
                id = {doctor_id}
        """

        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def handle_archived_check(self, state) -> None:
        if state == Qt.Checked:
            self.archived = 1
            self.ui.pshbtn_archive.setText("Unarchive")
        else:
            self.archived = 0
            self.ui.pshbtn_archive.setText("Archive")
        self.populate_table()

    def handle_name_search(self, text) -> None:
        if text:
            self.populate_table(True, text)
        else:
            self.populate_table()

    def connect_functions(self):
        self.ui.pshbtn_add.clicked.connect(self.handle_add)
        self.ui.pshbtn_edit.clicked.connect(self.handle_edit)
        self.ui.pshbtn_archive.clicked.connect(self.handle_archive)

        self.ui.chkbx_archived.stateChanged.connect(self.handle_archived_check)
        
        self.ui.lnedit_name.textChanged.connect(self.handle_name_search)