from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from UI.main_login_ui import Ui_Login


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        # self.connect_functions_to_buttons()

    def setup_window(self):
        self.setFixedSize(500, 500)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/window_icon.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def setup_ui(self):
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        pixmap = QPixmap(":/big_logo.png")
        self.ui.pxmp_logo.setPixmap(pixmap)