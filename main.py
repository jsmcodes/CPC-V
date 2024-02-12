from PyQt5.QtWidgets import QApplication

import sys

from login import Login


def main():
    app = QApplication(sys.argv)
    
    login = Login()
    login.show()
    # result = login.exec_()
    sys.exit(app.exec_())

    # if result == DevLogin.Accepted:
    #     main_window = Setup()
    #     main_window.show()
    #     sys.exit(app.exec_())

if __name__ == "__main__":
    main()