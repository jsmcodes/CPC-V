from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_position_dialog_ui import Ui_PositionDialog


class PositionDialog(QDialog):
    def __init__(self, parent, edit:bool=False, position_data=None):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.edit = edit
        self.position_data = position_data
        self.setup_ui()
        self.setup_window()

    def setup_ui(self) -> None:
        self.ui = Ui_PositionDialog()
        self.ui.setupUi(self)

        if self.edit:
            self.ui.lbl_position_id.setText(f"Position #{self.position_data[0]}")
            self.ui.lnedit_name.setText(self.position_data[1])
        else:
            current_position_id = self.get_last_position_id()[0] + 1
            self.ui.lbl_position_id.setText(f"Position #{current_position_id}")
        
        self.connect_functions()
        
    def get_last_position_id(self):
        self.database.connect()

        query = """
            SELECT
                COUNT(id)
            FROM
                positions
        """
        self.database.c.execute(query)

        last_position_id = self.database.c.fetchone()

        self.database.disconnect()

        return last_position_id

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
            if self.edit:
                id = self.position_data[0]
                self.update_position(id, name)
                self.accept()
            else:
                self.insert_position(name)
                self.accept()

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

    def update_position(self, position_id:int, position_name:str):
        self.database.connect()

        query = f"""
            UPDATE
                positions
            SET
                name = '{position_name}'
            WHERE
                id = {position_id}
        """
        self.database.c.execute(query)

        self.database.conn.commit()

        self.database.disconnect()

    def handle_reset(self):
        if self.edit:
            self.ui.lnedit_name.setText(self.position_data[1])
        else:
            self.ui.lnedit_name.clear()

    def handle_cancel(self):
        self.close()

    def connect_functions(self):
        self.ui.pshbtn_save.clicked.connect(self.handle_add)
        self.ui.pshbtn_reset.clicked.connect(self.handle_reset)
        self.ui.pshbtn_cancel.clicked.connect(self.handle_cancel)