from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from UI.setup_login_ui import Ui_DevLogin


class DevLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.connect_functions_to_buttons()

    def setup_window(self):
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def setup_ui(self):
        self.ui = Ui_DevLogin()
        self.ui.setupUi(self)

    def handle_login(self):
        dev_username = "jasssamcodes"
        dev_password = "!JasssamCodes0210"
        dev_username = "asd"
        dev_password = "asd"

        username = self.ui.lnedit_username.text().strip()
        password = self.ui.lnedit_password.text().strip()

        if username and password:
            if username == dev_username and password == dev_password:
                self.accept()

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_login.clicked.connect(self.handle_login)
