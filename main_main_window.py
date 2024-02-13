from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

import sqlite3

from create_database import DatabaseManager
from UI.main_window_ui import Ui_MainWindow
from main_patients import Patients


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.setup_ui()
        self.setup_window()
        # self.connect_functions_to_buttons()

    def setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        pixmap = QPixmap(":/small_logo.png")
        self.ui.pxmp_logo.setPixmap(pixmap)

        self.pg_patients = Patients()

        self.ui.stckdwdgt_content.addWidget(self.pg_patients)

        user_data = self.get_user_name_and_position()

        if user_data:
            name, position = user_data

            self.ui.lbl_full_name.setText(name)
            self.ui.lbl_position.setText(position)

            if position == "Receptionist":
                pass
            elif position == "Administrator":
                pass
            else:
                pass

    def setup_window(self):
        self.setFixedSize(1080, 720)
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
    
    def get_user_name_and_position(self) -> tuple:
        try:
            self.database.connect()

            query = f"USE `{self.database.database_name}`"
            self.database.c.execute(query)

            query = """
                SELECT 
                    name,
                    position
                FROM
                    login_history
                ORDER BY
                    id
                DESC LIMIT 1
            """
            self.database.c.execute(query)

            user_data = self.database.c.fetchone()

            self.database.disconnect()

            return user_data

        except Exception as e:
            print(f"Error in get_user_name_and_position: {e}")
            return None
