# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI\main_doctors_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Doctors(object):
    def setupUi(self, Doctors):
        Doctors.setObjectName("Doctors")
        Doctors.resize(942, 829)
        Doctors.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Doctors)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_search_filter = QtWidgets.QLabel(Doctors)
        self.lbl_search_filter.setObjectName("lbl_search_filter")
        self.horizontalLayout.addWidget(self.lbl_search_filter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pshbtn_refresh = QtWidgets.QPushButton(Doctors)
        self.pshbtn_refresh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_refresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pshbtn_refresh.setIcon(icon)
        self.pshbtn_refresh.setObjectName("pshbtn_refresh")
        self.horizontalLayout.addWidget(self.pshbtn_refresh)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.wdgt_search_filter = QtWidgets.QWidget(Doctors)
        self.wdgt_search_filter.setObjectName("wdgt_search_filter")
        self.wdgt_search_filter_layout = QtWidgets.QHBoxLayout(self.wdgt_search_filter)
        self.wdgt_search_filter_layout.setContentsMargins(0, 0, 0, 0)
        self.wdgt_search_filter_layout.setSpacing(10)
        self.wdgt_search_filter_layout.setObjectName("wdgt_search_filter_layout")
        self.chkbx_archived = QtWidgets.QCheckBox(self.wdgt_search_filter)
        self.chkbx_archived.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chkbx_archived.setObjectName("chkbx_archived")
        self.wdgt_search_filter_layout.addWidget(self.chkbx_archived)
        self.lnedit_name = QtWidgets.QLineEdit(self.wdgt_search_filter)
        self.lnedit_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lnedit_name.setObjectName("lnedit_name")
        self.wdgt_search_filter_layout.addWidget(self.lnedit_name)
        self.wdgt_search_filter_layout.setStretch(1, 1)
        self.verticalLayout.addWidget(self.wdgt_search_filter)
        self.tblwdgt_doctors = QtWidgets.QTableWidget(Doctors)
        self.tblwdgt_doctors.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tblwdgt_doctors.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblwdgt_doctors.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblwdgt_doctors.setAlternatingRowColors(True)
        self.tblwdgt_doctors.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblwdgt_doctors.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblwdgt_doctors.setObjectName("tblwdgt_doctors")
        self.tblwdgt_doctors.setColumnCount(3)
        self.tblwdgt_doctors.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblwdgt_doctors.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblwdgt_doctors.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblwdgt_doctors.setHorizontalHeaderItem(2, item)
        self.tblwdgt_doctors.horizontalHeader().setHighlightSections(False)
        self.tblwdgt_doctors.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tblwdgt_doctors)
        self.wdgt_page_buttons = QtWidgets.QWidget(Doctors)
        self.wdgt_page_buttons.setObjectName("wdgt_page_buttons")
        self.wdgt_pg_buttons_layout = QtWidgets.QHBoxLayout(self.wdgt_page_buttons)
        self.wdgt_pg_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.wdgt_pg_buttons_layout.setSpacing(10)
        self.wdgt_pg_buttons_layout.setObjectName("wdgt_pg_buttons_layout")
        self.pshbtn_add = QtWidgets.QPushButton(self.wdgt_page_buttons)
        self.pshbtn_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_add.setObjectName("pshbtn_add")
        self.wdgt_pg_buttons_layout.addWidget(self.pshbtn_add)
        self.pshbtn_edit = QtWidgets.QPushButton(self.wdgt_page_buttons)
        self.pshbtn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_edit.setObjectName("pshbtn_edit")
        self.wdgt_pg_buttons_layout.addWidget(self.pshbtn_edit)
        self.pshbtn_archive = QtWidgets.QPushButton(self.wdgt_page_buttons)
        self.pshbtn_archive.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pshbtn_archive.setObjectName("pshbtn_archive")
        self.wdgt_pg_buttons_layout.addWidget(self.pshbtn_archive)
        self.wdgt_pg_buttons_layout.setStretch(0, 1)
        self.wdgt_pg_buttons_layout.setStretch(1, 1)
        self.wdgt_pg_buttons_layout.setStretch(2, 1)
        self.verticalLayout.addWidget(self.wdgt_page_buttons)

        self.retranslateUi(Doctors)
        QtCore.QMetaObject.connectSlotsByName(Doctors)

    def retranslateUi(self, Doctors):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_search_filter.setText(_translate("Doctors", "Search/Filter:"))
        self.chkbx_archived.setText(_translate("Doctors", "Archived"))
        self.lnedit_name.setPlaceholderText(_translate("Doctors", "Enter name..."))
        item = self.tblwdgt_doctors.horizontalHeaderItem(0)
        item.setText(_translate("Doctors", "ID"))
        item = self.tblwdgt_doctors.horizontalHeaderItem(1)
        item.setText(_translate("Doctors", "Name"))
        item = self.tblwdgt_doctors.horizontalHeaderItem(2)
        item.setText(_translate("Doctors", "Position"))
        self.pshbtn_add.setText(_translate("Doctors", "Add"))
        self.pshbtn_edit.setText(_translate("Doctors", "Edit"))
        self.pshbtn_archive.setText(_translate("Doctors", "Archive"))
import dev_resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Doctors = QtWidgets.QWidget()
    ui = Ui_Doctors()
    ui.setupUi(Doctors)
    Doctors.show()
    sys.exit(app.exec_())
