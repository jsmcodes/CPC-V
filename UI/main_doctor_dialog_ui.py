# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\main_doctor_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DoctorDialog(object):
    def setupUi(self, DoctorDialog):
        DoctorDialog.setObjectName("DoctorDialog")
        DoctorDialog.resize(500, 720)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        DoctorDialog.setFont(font)
        self.main_layout = QtWidgets.QVBoxLayout(DoctorDialog)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.main_layout.setObjectName("main_layout")
        self.lbl_id = QtWidgets.QLabel(DoctorDialog)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_id.setFont(font)
        self.lbl_id.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_id.setObjectName("lbl_id")
        self.main_layout.addWidget(self.lbl_id)
        self.lbl_position = QtWidgets.QLabel(DoctorDialog)
        self.lbl_position.setObjectName("lbl_position")
        self.main_layout.addWidget(self.lbl_position)
        self.cmbox_position = QtWidgets.QComboBox(DoctorDialog)
        self.cmbox_position.setEditable(True)
        self.cmbox_position.setMaxVisibleItems(6)
        self.cmbox_position.setMaxCount(100)
        self.cmbox_position.setObjectName("cmbox_position")
        self.cmbox_position.addItem("")
        self.main_layout.addWidget(self.cmbox_position)
        self.lbl_name = QtWidgets.QLabel(DoctorDialog)
        self.lbl_name.setObjectName("lbl_name")
        self.main_layout.addWidget(self.lbl_name)
        self.lnedit_name = QtWidgets.QLineEdit(DoctorDialog)
        self.lnedit_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_name.setClearButtonEnabled(True)
        self.lnedit_name.setObjectName("lnedit_name")
        self.main_layout.addWidget(self.lnedit_name)
        self.lbl_sex = QtWidgets.QLabel(DoctorDialog)
        self.lbl_sex.setObjectName("lbl_sex")
        self.main_layout.addWidget(self.lbl_sex)
        self.cmbox_sex = QtWidgets.QComboBox(DoctorDialog)
        self.cmbox_sex.setStyleSheet("")
        self.cmbox_sex.setEditable(True)
        self.cmbox_sex.setMaxVisibleItems(2)
        self.cmbox_sex.setMaxCount(2)
        self.cmbox_sex.setModelColumn(0)
        self.cmbox_sex.setObjectName("cmbox_sex")
        self.cmbox_sex.addItem("")
        self.cmbox_sex.addItem("")
        self.main_layout.addWidget(self.cmbox_sex)
        self.lbl_birthdate = QtWidgets.QLabel(DoctorDialog)
        self.lbl_birthdate.setObjectName("lbl_birthdate")
        self.main_layout.addWidget(self.lbl_birthdate)
        self.dtedit_birthdate = QtWidgets.QDateEdit(DoctorDialog)
        self.dtedit_birthdate.setAlignment(QtCore.Qt.AlignCenter)
        self.dtedit_birthdate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dtedit_birthdate.setProperty("showGroupSeparator", False)
        self.dtedit_birthdate.setCalendarPopup(True)
        self.dtedit_birthdate.setObjectName("dtedit_birthdate")
        self.main_layout.addWidget(self.dtedit_birthdate)
        self.lbl_age = QtWidgets.QLabel(DoctorDialog)
        self.lbl_age.setObjectName("lbl_age")
        self.main_layout.addWidget(self.lbl_age)
        self.lnedit_age = QtWidgets.QLineEdit(DoctorDialog)
        self.lnedit_age.setMaxLength(8)
        self.lnedit_age.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_age.setReadOnly(True)
        self.lnedit_age.setObjectName("lnedit_age")
        self.main_layout.addWidget(self.lnedit_age)
        self.lbl_contact_number = QtWidgets.QLabel(DoctorDialog)
        self.lbl_contact_number.setObjectName("lbl_contact_number")
        self.main_layout.addWidget(self.lbl_contact_number)
        self.lnedit_contact_number = QtWidgets.QLineEdit(DoctorDialog)
        self.lnedit_contact_number.setCursorPosition(0)
        self.lnedit_contact_number.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_contact_number.setClearButtonEnabled(True)
        self.lnedit_contact_number.setObjectName("lnedit_contact_number")
        self.main_layout.addWidget(self.lnedit_contact_number)
        self.lbl_address = QtWidgets.QLabel(DoctorDialog)
        self.lbl_address.setObjectName("lbl_address")
        self.main_layout.addWidget(self.lbl_address)
        self.txtedit_address = QtWidgets.QTextEdit(DoctorDialog)
        self.txtedit_address.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtedit_address.setTabChangesFocus(True)
        self.txtedit_address.setObjectName("txtedit_address")
        self.main_layout.addWidget(self.txtedit_address)
        self.lbl_username = QtWidgets.QLabel(DoctorDialog)
        self.lbl_username.setObjectName("lbl_username")
        self.main_layout.addWidget(self.lbl_username)
        self.lnedit_username = QtWidgets.QLineEdit(DoctorDialog)
        self.lnedit_username.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_username.setObjectName("lnedit_username")
        self.main_layout.addWidget(self.lnedit_username)
        self.lbl_password = QtWidgets.QLabel(DoctorDialog)
        self.lbl_password.setObjectName("lbl_password")
        self.main_layout.addWidget(self.lbl_password)
        self.lnedit_password = QtWidgets.QLineEdit(DoctorDialog)
        self.lnedit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lnedit_password.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_password.setObjectName("lnedit_password")
        self.main_layout.addWidget(self.lnedit_password)
        self.wdgt_dialog_buttons = QtWidgets.QWidget(DoctorDialog)
        self.wdgt_dialog_buttons.setObjectName("wdgt_dialog_buttons")
        self.wdgt_dialog_buttons_layout = QtWidgets.QHBoxLayout(self.wdgt_dialog_buttons)
        self.wdgt_dialog_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.wdgt_dialog_buttons_layout.setSpacing(10)
        self.wdgt_dialog_buttons_layout.setObjectName("wdgt_dialog_buttons_layout")
        self.pshbtn_save = QtWidgets.QPushButton(self.wdgt_dialog_buttons)
        self.pshbtn_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_save.setObjectName("pshbtn_save")
        self.wdgt_dialog_buttons_layout.addWidget(self.pshbtn_save)
        self.pshbtn_reset = QtWidgets.QPushButton(self.wdgt_dialog_buttons)
        self.pshbtn_reset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_reset.setObjectName("pshbtn_reset")
        self.wdgt_dialog_buttons_layout.addWidget(self.pshbtn_reset)
        self.pshbtn_cancel = QtWidgets.QPushButton(self.wdgt_dialog_buttons)
        self.pshbtn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_cancel.setObjectName("pshbtn_cancel")
        self.wdgt_dialog_buttons_layout.addWidget(self.pshbtn_cancel)
        self.wdgt_dialog_buttons_layout.setStretch(0, 1)
        self.wdgt_dialog_buttons_layout.setStretch(1, 1)
        self.wdgt_dialog_buttons_layout.setStretch(2, 1)
        self.main_layout.addWidget(self.wdgt_dialog_buttons)

        self.retranslateUi(DoctorDialog)
        self.cmbox_sex.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DoctorDialog)

    def retranslateUi(self, DoctorDialog):
        _translate = QtCore.QCoreApplication.translate
        DoctorDialog.setWindowTitle(_translate("DoctorDialog", "Dialog"))
        self.lbl_id.setText(_translate("DoctorDialog", "Doctor #"))
        self.lbl_position.setText(_translate("DoctorDialog", "Position:"))
        self.cmbox_position.setItemText(0, _translate("DoctorDialog", "+"))
        self.lbl_name.setText(_translate("DoctorDialog", "Name:"))
        self.lnedit_name.setPlaceholderText(_translate("DoctorDialog", "Enter name..."))
        self.lbl_sex.setText(_translate("DoctorDialog", "Sex:"))
        self.cmbox_sex.setItemText(0, _translate("DoctorDialog", "Female"))
        self.cmbox_sex.setItemText(1, _translate("DoctorDialog", "Male"))
        self.lbl_birthdate.setText(_translate("DoctorDialog", "Birthdate:"))
        self.dtedit_birthdate.setDisplayFormat(_translate("DoctorDialog", "MMM dd, yyyy"))
        self.lbl_age.setText(_translate("DoctorDialog", "Age:"))
        self.lnedit_age.setPlaceholderText(_translate("DoctorDialog", "Enter age..."))
        self.lbl_contact_number.setText(_translate("DoctorDialog", "Contact Number:"))
        self.lnedit_contact_number.setInputMask(_translate("DoctorDialog", "(+63)\\900-000-0000"))
        self.lnedit_contact_number.setPlaceholderText(_translate("DoctorDialog", "Enter contact number..."))
        self.lbl_address.setText(_translate("DoctorDialog", "Address:"))
        self.txtedit_address.setPlaceholderText(_translate("DoctorDialog", "Enter address..."))
        self.lbl_username.setText(_translate("DoctorDialog", "Username:"))
        self.lnedit_username.setPlaceholderText(_translate("DoctorDialog", "Enter username..."))
        self.lbl_password.setText(_translate("DoctorDialog", "Password:"))
        self.lnedit_password.setPlaceholderText(_translate("DoctorDialog", "Enter password..."))
        self.pshbtn_save.setText(_translate("DoctorDialog", "Save"))
        self.pshbtn_reset.setText(_translate("DoctorDialog", "Reset"))
        self.pshbtn_cancel.setText(_translate("DoctorDialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DoctorDialog = QtWidgets.QDialog()
    ui = Ui_DoctorDialog()
    ui.setupUi(DoctorDialog)
    DoctorDialog.show()
    sys.exit(app.exec_())
