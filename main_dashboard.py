from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QTimer

from datetime import datetime

from database_manager import DatabaseManager
from UI.main_dashboard_ui import Ui_Dashboard
from main_dashboard_consultation_dialog import DashboardConsultationDialog


class Dashboard(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)

        self.ui.trwdgt_dashboard.setHeaderHidden(True)
        self.ui.trwdgt_dashboard.setColumnCount(2)
        self.ui.trwdgt_dashboard.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.populate_tree)
        # self.timer.start(1000)

        self.populate_tree()

        self.connect_functions()

    def populate_tree(self):
        doctors = self.fetch_doctors()

        self.ui.trwdgt_dashboard.clear()

        for doctor in doctors:
            doctor_name = doctor[0]

            doctor_item = self.add_tree_item(doctor_name, None)

            patients = self.fetch_patients_for_doctor(doctor_name)

            for patient in patients:
                patient_name, status = patient

                # Add both patient name and status in the second column
                patient_item = self.add_tree_item(patient_name, status, doctor_item)

    def add_tree_item(self, name, value, parent=None):
        item = QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setText(1, value)

        if parent is None:
            self.ui.trwdgt_dashboard.addTopLevelItem(item)
            item.setExpanded(True)

        return item

    def fetch_patients_for_doctor(self, doctor_name):
        self.database.connect()

        get_doctor_id = f"""
            SELECT
                id
            FROM
                users
            WHERE
                name = '{doctor_name}'
        """
        self.database.c.execute(get_doctor_id)
        doctor_id = self.database.c.fetchone()

        current_date = datetime.now().strftime("%Y-%m-%d")  # Format the current date

        query = f"""
            SELECT
                p.name,
                c.status
            FROM
                consultations AS c
            JOIN
                patients AS p
            ON
                c.patient_id = p.id
            WHERE
                doctor_id = {doctor_id[0]}
            AND
                date = '{current_date}'
            AND
                c.archived = 0
            ORDER BY
                c.id ASC
        """
        self.database.c.execute(query)
        patients = self.database.c.fetchall()

        self.database.disconnect()

        return patients

    def fetch_doctors(self):
        self.database.connect()

        query = """
            SELECT
                name
            FROM
                users
            WHERE
                position_id <> 3
            ORDER BY
                name ASC
        """
        self.database.c.execute(query)

        doctors = self.database.c.fetchall()

        self.database.disconnect()

        return doctors
    
    def handle_start_consultation(self):
        dialog = DashboardConsultationDialog(self)
        result = dialog.exec_()

        if result == dialog.Accepted:
            pass

    def connect_functions(self):
        self.ui.pshbtn_start_consultation.clicked.connect(self.handle_start_consultation)