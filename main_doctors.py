from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt

from database_manager import DatabaseManager
from UI.main_doctors_ui import Ui_Doctors


class Doctors(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_Doctors()
        self.ui.setupUi(self)