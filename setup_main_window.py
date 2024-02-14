from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QUrl, QRegExp, Qt
from PyQt5.QtGui import QDesktopServices, QPixmap, QRegExpValidator

import sqlite3
import os
import subprocess
import shutil
import socket

from database_manager import DatabaseManager
from UI.setup_window_ui import Ui_Setup


class Setup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.connect_functions_to_buttons()

    def setup_window(self):
        self.setFixedSize(400, 800)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def setup_ui(self):
        self.ui = Ui_Setup()
        self.ui.setupUi(self)
        ip_regex = QRegExp(r"^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$")
        validator = QRegExpValidator(ip_regex)
        self.ui.lnedit_server_ip_address.setValidator(validator)

    def get_ip_address(self):
        hostname = socket.gethostname()
        
        ip_address = socket.gethostbyname(hostname)

        self.ui.lnedit_server_ip_address.setText(ip_address)

    def handle_change_window_icon(self):
        self.window_icon_path = None
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.ico);;All Files (*)", options=options)

        if file_name:
            self.window_icon_path = file_name
            pixmap = QPixmap(file_name)
            self.ui.pxmp_window_icon.setPixmap(pixmap)

    def handle_change_big_logo(self):
        self.big_logo_path = None
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.ico);;All Files (*)", options=options)

        if file_name:
            self.big_logo_path = file_name
            pixmap = QPixmap(file_name)
            self.ui.pxmp_big_logo.setPixmap(pixmap)

    def handle_change_small_logo(self):
        self.small_logo_path = None
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.ico);;All Files (*)", options=options)

        if file_name:
            self.small_logo_path = file_name
            pixmap = QPixmap(file_name)
            self.ui.pxmp_small_logo.setPixmap(pixmap)

    def handle_save(self):
        server_ip_address = self.ui.lnedit_server_ip_address.text().strip()
        store_name = self.ui.lnedit_store_name.text().strip()

        if server_ip_address and store_name:
            self.create_database_and_tables()
            self.insert_values(server_ip_address, store_name)
            self.create_qrc_file()
            self.convert_qrc_to_py()
            # self.install_xampp()

    def handle_clear(self):
        self.ui.lnedit_server_ip_address.clear()
        self.ui.lnedit_store_name.clear()
        self.ui.pxmp_window_icon.clear()
        self.ui.pxmp_window_icon.setText(r"[WINDOW ICON HERE]")
        self.ui.pxmp_big_logo.clear()
        self.ui.pxmp_big_logo.setText(r"[BIG LOGO HERE]")
        self.ui.pxmp_small_logo.clear()
        self.ui.pxmp_small_logo.setText(r"[SMALL LOGO HERE]")

    def create_database_and_tables(self):
        try:
            conn = sqlite3.connect("Database/setup.db")
            cursor = conn.cursor()

            query = """
                CREATE TABLE IF NOT EXISTS setup (
                    server_ip_address VARCHAR(15),
                    store_name VARCHAR(255)
                )
            """

            cursor.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn.close()

    def insert_values(self, server_ip_address, store_name):
        try:
            conn = sqlite3.connect("Database/setup.db")
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO setup (
                    server_ip_address,
                    store_name
                )
                VALUES (
                    ?,
                    ?
                )
            """

            cursor.execute(insert_query, (server_ip_address, store_name))
            conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn.close()

    def create_qrc_file(self):
        try:
            resource_folder = "Resource"

            for image_path in [self.window_icon_path, self.big_logo_path, self.small_logo_path]:
                extension = os.path.splitext(image_path)[1]
                new_path = os.path.join(resource_folder, f"{os.path.basename(image_path).replace(extension, '')}{extension}")
                shutil.copy(image_path, new_path)

            self.window_icon_path = f"window_icon{os.path.splitext(self.window_icon_path)[1]}"
            self.big_logo_path = f"big_logo{os.path.splitext(self.big_logo_path)[1]}"
            self.small_logo_path = f"small_logo{os.path.splitext(self.small_logo_path)[1]}"

            qrc_content = f"""
                <RCC>
                    <qresource>
                        <file>{self.window_icon_path}</file>
                        <file>{self.big_logo_path}</file>
                        <file>{self.small_logo_path}</file>
                    </qresource>
                </RCC>
            """

            qrc_file_path = os.path.join(resource_folder, "resource.qrc")
            with open(qrc_file_path, "w") as qrc_file:
                qrc_file.write(qrc_content)

        except Exception as e:
            print(f"An error occurred while creating QRC file: {e}")

    def convert_qrc_to_py(self):
        try:
            command = f"pyrcc5 Resource/resource.qrc -o resource_rc.py"
            subprocess.run(command, shell=True)

        except Exception as e:
            print(f"An error occurred while converting QRC to PY: {e}")

    def install_xampp(self):
        try:
            xampp_path = r"Install\xampp-windows-x64-8.2.12-0-VS16-installer.exe"
            QDesktopServices.openUrl(QUrl.fromLocalFile(xampp_path))

        except Exception as e:
            print(f"An error occurred while trying to open XAMPP installer: {e}")

    def replace_config_file(self):
        try:
            source_path = r"Install\httpd-xampp.conf"
            destination_path = r"C:\xampp\apache\conf\extra"

            shutil.copy(source_path, destination_path)

            database = DatabaseManager()
            database.create_database()
            database.create_tables()
            database.insert_values()
            database.insert_positions()
            database.insert_users()

        except FileNotFoundError as file_error:
            print(f"Error copying file: {file_error}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def connect_functions_to_buttons(self):
        self.ui.pshbtn_get_server_ip_address.clicked.connect(self.get_ip_address)
        self.ui.pshbtn_change_window_icon.clicked.connect(self.handle_change_window_icon)
        self.ui.pshbtn_change_big_logo.clicked.connect(self.handle_change_big_logo)
        self.ui.pshbtn_change_small_logo.clicked.connect(self.handle_change_small_logo)
        self.ui.pshbtn_save.clicked.connect(self.handle_save)
        self.ui.pshbtn_config.clicked.connect(self.replace_config_file)
        self.ui.pshbtn_clear.clicked.connect(self.handle_clear)
