from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

import sqlite3

from UI.main_window_ui import Ui_MainWindow
from main_patients import Patients


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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