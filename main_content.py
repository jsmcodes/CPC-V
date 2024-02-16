from PyQt5.QtWidgets import QWidget

from database_manager import DatabaseManager
from UI.main_content_ui import Ui_Content
from main_patients import Patients
from main_doctors import Doctors


class Content(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.ui = Ui_Content()
        self.ui.setupUi(self)
        self.add_pages()
        self.connect_functions_to_buttons()

    def add_pages(self) -> None:
        self.pages = {
            "patients": Patients(),
            "doctors": Doctors()
        }

        for name, page in self.pages.items():
            self.ui.stckdwdgt_content.addWidget(page)

    def switch_page(self, page_name: str) -> None:
        index = list(self.pages.keys()).index(page_name)
        self.ui.stckdwdgt_content.setCurrentIndex(index)

    def set_user_name_and_position(self) -> None:
        user_data = self.get_user_name_and_position()

        if user_data:
            name, position = user_data

            self.ui.lbl_name.setText(name)
            self.ui.lbl_position.setText(position)

            if position == "Receptionist":
                pass
            elif position == "Administrator":
                pass
            else:
                pass

    def get_user_name_and_position(self) -> tuple:
        try:
            self.database.connect()

            query = """
                SELECT 
                    name,
                    position
                FROM
                    login_history
                ORDER BY
                    id
                DESC LIMIT 1
            """
            self.database.c.execute(query)

            user_data = self.database.c.fetchone()

            self.database.disconnect()

            return user_data

        except Exception as e:
            print(f"Error in get_user_name_and_position: {e}")
            return None

    def set_patients_page_ui(self, position):
        if position == "Receptionist":
            self.pages["patients"].ui.pshbtn_archive.setEnabled(False)
        else:
            self.pages["patients"].ui.pshbtn_archive.setEnabled(True)

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
        self.ui.pshbtn_patients.clicked.connect(lambda: self.switch_page("patients"))
        self.ui.pshbtn_doctors.clicked.connect(lambda: self.switch_page("doctors"))
        self.ui.pshbtn_logout.clicked.connect(self.handle_logout)