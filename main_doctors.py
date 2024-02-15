from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt

from database_manager import DatabaseManager
from UI.main_doctors_ui import Ui_Doctors


class Doctors(QWidget):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Doctors()
        self.ui.setupUi(self)

        self.ui.tblwdgt_doctors.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.tblwdgt_doctors.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.populate_table()

    def get_data(self) -> tuple:
        self.database.connect()

        query = """
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
            ORDER BY
                u.id ASC
        """

        self.database.c.execute(query)

        doctors = self.database.c.fetchall()

        self.database.disconnect()

        return doctors

    def populate_table(self) -> None:
        self.ui.tblwdgt_doctors.setRowCount(0)

        doctors = self.get_data()

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