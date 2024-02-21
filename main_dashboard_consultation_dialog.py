from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

from database_manager import DatabaseManager
from UI.main_dashboard_consultation_dialog_ui import Ui_Dialog


class DashboardConsultationDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.setup_ui()
        self.setup_window()

    def setup_ui(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
    
    def setup_window(self) -> None:
        self.setFixedSize(1350, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)

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
    
    def handle_finish(self):
        self.accept()

    def connect_functions(self):
        self.ui.psh