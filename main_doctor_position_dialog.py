from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_doctor_position_dialog_ui import Ui_PositionDialog


class PositionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.setup_ui()
        self.setup_window()

    def setup_ui(self) -> None:
        self.ui = Ui_PositionDialog()
        self.ui.setupUi(self)
        
        self.connect_functions()
        
    def setup_window(self) -> None:
        self.setFixedSize(400, 300)
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

    def handle_add(self) -> None:
        name = self.ui.lnedit_name.text().strip()

        if name:
            self.insert_position(name)
            print("Inserted New Position")
            self.accept()
            print("Accepted")

    def handle_cancel(self):
        self.close()

    def insert_position(self, position_name: str) -> None:
        self.database.connect()

        query = f"""
            INSERT INTO 
                positions (
                    name,
                    archived
                )
            VALUES
                (
                    '{position_name}',
                    0
                )
        """
        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def connect_functions(self):
        self.ui.pshbtn_save.clicked.connect(self.handle_add)
        self.ui.pshbtn_cancel.clicked.connect(self.handle_cancel)