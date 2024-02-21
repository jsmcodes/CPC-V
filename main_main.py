from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont

import sqlite3
import sys

from database_manager import DatabaseManager
from main_login import Login
from main_content import Content


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()
        self.setup_ui()
        self.setup_window()
        self.add_pages()

    def setup_ui(self):
        self.stckdwdgt_main = QStackedWidget(self)
        self.setCentralWidget(self.stckdwdgt_main)

    def setup_window(self):
        self.setFixedSize(1350, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        icon = QIcon()
        pixmap = QPixmap(":/window_icon.ico")
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        store_name = self.get_store_name()
        self.setWindowTitle(store_name[0])
        font = QFont()
        font.setFamily("Verdana")
        font.setPointSize(8)
        self.setFont(font)

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

    def add_pages(self):
        self.pages = {
            "login": Login(self),
            "content": Content(self)
        }

        for name, page in self.pages.items():
            self.stckdwdgt_main.addWidget(page)

    def update_content_ui(self, name, position):
        self.pages["content"].user_name = name
        self.pages["content"].user_position = position
        self.pages["content"].switch_page("dashboard")
        self.pages["content"].set_user_name_and_position()
        self.pages["content"].set_patients_page_ui(position)
        self.pages["content"].set_doctors_page_ui(position)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
