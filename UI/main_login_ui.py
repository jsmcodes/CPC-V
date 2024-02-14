# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\main_login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(1080, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setWindowTitle("")
        self.main_layout = QtWidgets.QHBoxLayout(Login)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.main_layout.setObjectName("main_layout")
        self.wdgt_login = QtWidgets.QWidget(Login)
        self.wdgt_login.setObjectName("wdgt_login")
        self.wdgt_login_layout = QtWidgets.QVBoxLayout(self.wdgt_login)
        self.wdgt_login_layout.setContentsMargins(0, 0, 0, 0)
        self.wdgt_login_layout.setSpacing(10)
        self.wdgt_login_layout.setObjectName("wdgt_login_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 133, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.wdgt_login_layout.addItem(spacerItem)
        self.wdgt_input = QtWidgets.QWidget(self.wdgt_login)
        self.wdgt_input.setObjectName("wdgt_input")
        self.wdgt_input_layout = QtWidgets.QVBoxLayout(self.wdgt_input)
        self.wdgt_input_layout.setContentsMargins(10, 10, 10, 10)
        self.wdgt_input_layout.setSpacing(10)
        self.wdgt_input_layout.setObjectName("wdgt_input_layout")
        self.lbl_username = QtWidgets.QLabel(self.wdgt_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_username.sizePolicy().hasHeightForWidth())
        self.lbl_username.setSizePolicy(sizePolicy)
        self.lbl_username.setObjectName("lbl_username")
        self.wdgt_input_layout.addWidget(self.lbl_username)
        self.lnedit_username = QtWidgets.QLineEdit(self.wdgt_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedit_username.sizePolicy().hasHeightForWidth())
        self.lnedit_username.setSizePolicy(sizePolicy)
        self.lnedit_username.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_username.setObjectName("lnedit_username")
        self.wdgt_input_layout.addWidget(self.lnedit_username)
        self.lbl_password = QtWidgets.QLabel(self.wdgt_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_password.sizePolicy().hasHeightForWidth())
        self.lbl_password.setSizePolicy(sizePolicy)
        self.lbl_password.setObjectName("lbl_password")
        self.wdgt_input_layout.addWidget(self.lbl_password)
        self.lnedit_password = QtWidgets.QLineEdit(self.wdgt_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lnedit_password.sizePolicy().hasHeightForWidth())
        self.lnedit_password.setSizePolicy(sizePolicy)
        self.lnedit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lnedit_password.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_password.setObjectName("lnedit_password")
        self.wdgt_input_layout.addWidget(self.lnedit_password)
        self.pshbtn_login = QtWidgets.QPushButton(self.wdgt_input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pshbtn_login.sizePolicy().hasHeightForWidth())
        self.pshbtn_login.setSizePolicy(sizePolicy)
        self.pshbtn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_login.setObjectName("pshbtn_login")
        self.wdgt_input_layout.addWidget(self.pshbtn_login)
        self.wdgt_input_layout.setStretch(0, 1)
        self.wdgt_input_layout.setStretch(1, 1)
        self.wdgt_input_layout.setStretch(2, 1)
        self.wdgt_input_layout.setStretch(3, 1)
        self.wdgt_input_layout.setStretch(4, 1)
        self.wdgt_login_layout.addWidget(self.wdgt_input)
        spacerItem1 = QtWidgets.QSpacerItem(20, 133, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.wdgt_login_layout.addItem(spacerItem1)
        self.wdgt_login_layout.setStretch(0, 1)
        self.wdgt_login_layout.setStretch(1, 3)
        self.wdgt_login_layout.setStretch(2, 1)
        self.main_layout.addWidget(self.wdgt_login)
        self.pxmp_logo = QtWidgets.QLabel(Login)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pxmp_logo.sizePolicy().hasHeightForWidth())
        self.pxmp_logo.setSizePolicy(sizePolicy)
        self.pxmp_logo.setText("")
        self.pxmp_logo.setPixmap(QtGui.QPixmap(":/big_logo.png"))
        self.pxmp_logo.setScaledContents(True)
        self.pxmp_logo.setObjectName("pxmp_logo")
        self.main_layout.addWidget(self.pxmp_logo)
        self.main_layout.setStretch(0, 4)
        self.main_layout.setStretch(1, 6)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_username.setText(_translate("Login", "Username:"))
        self.lnedit_username.setPlaceholderText(_translate("Login", "Enter username..."))
        self.lbl_password.setText(_translate("Login", "Password:"))
        self.lnedit_password.setPlaceholderText(_translate("Login", "Enter password..."))
        self.pshbtn_login.setText(_translate("Login", "Log In"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QWidget()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
