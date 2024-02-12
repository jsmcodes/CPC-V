from PyQt5.QtWidgets import QApplication

import sys

from setup_login import DevLogin
from setup import Setup


def main():
    app = QApplication(sys.argv)
    
    dev_login = DevLogin()
    result = dev_login.exec_()

    if result == DevLogin.Accepted:
        main_window = Setup()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()