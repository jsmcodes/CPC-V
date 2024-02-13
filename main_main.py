from PyQt5.QtWidgets import QApplication

import sys

from main_login import Login
from main_main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    login = Login()
    result = login.exec_()

    if result == login.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()