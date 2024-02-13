from PyQt5.QtWidgets import QWidget

from database_manager import DatabaseManager
from UI.main_content_ui import Ui_Content
from main_patients import Patients


class Content(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.setup_ui()
        self.connect_functions_to_buttons()

    def setup_ui(self):
        self.ui = Ui_Content()
        self.ui.setupUi(self)

        self.pg_patients = Patients()

        self.ui.stckdwdgt_content.addWidget(self.pg_patients)

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

            query = f"USE `{self.database.database_name}`"
            self.database.c.execute(query)

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

    def handle_logout(self):
        patients = self.pg_patients.get_data()
        self.pg_patients.populate_table(patients)
        self.parent.stckdwdgt_main.setCurrentIndex(0)

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_logout.clicked.connect(self.handle_logout)