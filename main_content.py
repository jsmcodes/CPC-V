from PyQt5.QtWidgets import QWidget

from database_manager import DatabaseManager
from UI.main_content_ui import Ui_Content
from main_dashboard import Dashboard
from main_consultations import Consultations
from main_patients import Patients
from main_doctors import Doctors
from main_positions import Positions


class Content(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.user_name = None
        self.user_position = None
        self.database = DatabaseManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Content()
        self.ui.setupUi(self)

        self.add_pages()

        self.connect_functions_to_buttons()

    def add_pages(self) -> None:
        self.pages = {
            "dashboard": Dashboard(self),
            "consultations": Consultations(self),
            "patients": Patients(self),
            "doctors": Doctors(self),
            "positions": Positions(self)
        }

        for name, page in self.pages.items():
            self.ui.stckdwdgt_content.addWidget(page)

    def switch_page(self, page_name: str) -> None:
        index = list(self.pages.keys()).index(page_name)
        self.ui.stckdwdgt_content.setCurrentIndex(index)

    def set_user_name_and_position(self):
        self.ui.lbl_name.setText(self.user_name)
        self.ui.lbl_position.setText(self.user_position)

    def set_patients_page_ui(self, position):
        if position == "Receptionist":
            self.pages["patients"].ui.pshbtn_add.setEnabled(True)
            self.pages["patients"].ui.pshbtn_edit.setEnabled(True)
            self.pages["patients"].ui.pshbtn_archive.setEnabled(False)
        else:
            self.pages["patients"].ui.pshbtn_add.setEnabled(False)
            self.pages["patients"].ui.pshbtn_edit.setEnabled(False)
            self.pages["patients"].ui.pshbtn_archive.setEnabled(False)

    def set_doctors_page_ui(self, position):
        if position == "Receptionist":
            self.pages["doctors"].ui.pshbtn_archive.setEnabled(False)
        else:
            self.pages["doctors"].ui.pshbtn_archive.setEnabled(True)
    
    def handle_logout(self) -> None:
        self.pages["patients"].ui.chkbox_archived.setCheckState(False)
        patients = self.pages["patients"].get_data()
        self.pages["patients"].populate_table(patients)
        self.parent.stckdwdgt_main.setCurrentIndex(0)

    def connect_functions_to_buttons(self) -> None:
        self.ui.pshbtn_dashboard.clicked.connect(lambda: self.switch_page("dashboard"))
        self.ui.pshbtn_consultations.clicked.connect(lambda: self.switch_page("consultations"))
        self.ui.pshbtn_patients.clicked.connect(lambda: self.switch_page("patients"))
        self.ui.pshbtn_doctors.clicked.connect(lambda: self.switch_page("doctors"))
        self.ui.pshbtn_positions.clicked.connect(lambda: self.switch_page("positions"))
        self.ui.pshbtn_logout.clicked.connect(self.handle_logout)