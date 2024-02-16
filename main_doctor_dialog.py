from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_doctor_dialog_ui import Ui_DoctorDialog
from main_doctor_position_dialog import PositionDialog


class DoctorDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.setup_ui()
        self.setup_window()

    def setup_ui(self) -> None:
        self.ui = Ui_DoctorDialog()
        self.ui.setupUi(self)

        self.insert_positions()
        self.ui.cmbox_position.lineEdit().setAlignment(Qt.AlignCenter)
        self.ui.cmbox_position.setCurrentIndex(1)

        self.connect_functions()
        
    def setup_window(self) -> None:
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

            dialog = PositionDialog()
            result = dialog.exec_()

            if result == dialog.Accepted:
                print("Position Dialog Closed")
                self.ui.cmbox_position.disconnect()
                self.insert_positions()
                self.ui.cmbox_position.currentIndexChanged.connect(self.on_position_changed)
                print("Inserted Positions")

    def connect_functions(self):
        self.ui.cmbox_position.currentIndexChanged.connect(self.on_position_changed)