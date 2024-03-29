from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QPixmap, QKeyEvent

from database_manager import DatabaseManager
from UI.main_login_ui import Ui_Login


class Login(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.database = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        pixmap = QPixmap(":/big_logo.png")
        self.ui.pxmp_logo.setPixmap(pixmap)

        self.connect_functions_to_buttons()

    def handle_login(self):
        username = self.ui.lnedit_username.text().strip()
        password = self.ui.lnedit_password.text().strip()

        if username and password:
            user_data = self.check_if_user_exists(username, password)

            if user_data:
                name = user_data[1]
                position = user_data[2]
                self.insert_to_login_history(user_data)
                self.ui.lnedit_username.clear()
                self.ui.lnedit_password.clear()
                self.ui.lnedit_username.setFocus()
                self.parent.stckdwdgt_main.setCurrentIndex(1)
                self.parent.update_content_ui(name, position)

    def check_if_user_exists(self, username, password) -> tuple:
        try:
            self.database.connect()

            query = f"""
                SELECT 
                    u.id,
                    u.name,
                    p.name
                FROM
                    users AS u
                JOIN
                    positions AS p
                ON
                    u.position_id = p.id
                WHERE
                    username = '{username}'
                AND
                    password = '{password}'
            """
            self.database.c.execute(query)

            user_data = self.database.c.fetchone()

            return user_data

        except Exception as e:
            print(f"Error in check_if_user_exists: {e}")
            return None

        finally:
            self.database.disconnect()

    def insert_to_login_history(self, user_data: tuple) -> None:
        try:
            user_id, name, position = user_data
            date = QDate.currentDate().toPyDate()
            time = QTime.currentTime().toString(Qt.ISODate)

            self.database.connect()

            query = f"""
                INSERT INTO login_history (
                    user_id,
                    name,
                    position,
                    date,
                    time
                )
                VALUES (
                    {user_id},
                    '{name}',
                    '{position}',
                    '{date}',
                    '{time}'
                )
            """
            self.database.c.execute(query)

            self.database.conn.commit()

        except Exception as e:
            print(f"Error in insert_to_login_history: {e}")

        finally:
            self.database.disconnect()

    def connect_functions_to_buttons(self) -> None:
        self.ui.pshbtn_login.clicked.connect(self.handle_login)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.handle_login()
