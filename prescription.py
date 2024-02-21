import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import Qt, QUrl, QByteArray, QIODevice, QBuffer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QImage, QPixmap
import os

import resource_rc

class PrescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Prescription/Invoice Generator')

        # Create input fields
        self.doctor_name_label = QLabel('Doctor Name:')
        self.doctor_name_input = QLineEdit()
        self.doctor_name_input.textChanged.connect(self.update_html)

        self.patient_name_label = QLabel('Patient Name:')
        self.patient_name_input = QLineEdit()
        self.patient_name_input.textChanged.connect(self.update_html)

        self.prescription_label = QLabel('Prescription:')
        self.prescription_input = QLineEdit()
        self.prescription_input.textChanged.connect(self.update_html)

        self.medicine_label = QLabel('Medicine(s) Bought:')
        self.medicine_input = QLineEdit()
        self.medicine_input.textChanged.connect(self.update_html)

        # Create HTML display area with QWebEngineView
        self.web_view = QWebEngineView()

        # Create print button
        self.print_button = QPushButton('Print Prescription/Invoice')
        self.print_button.clicked.connect(self.print_html)

        # Set up layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.doctor_name_label)
        input_layout.addWidget(self.doctor_name_input)
        input_layout.addWidget(self.patient_name_label)
        input_layout.addWidget(self.patient_name_input)
        input_layout.addWidget(self.prescription_label)
        input_layout.addWidget(self.prescription_input)
        input_layout.addWidget(self.medicine_label)
        input_layout.addWidget(self.medicine_input)

        display_layout = QVBoxLayout()
        display_layout.addWidget(self.web_view)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.print_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(display_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Call update_html initially to set the HTML content
        self.update_html()

    def update_html(self):
        # Create HTML content based on input
        doctor_name = self.doctor_name_input.text()
        patient_name = self.patient_name_input.text()
        prescription = self.prescription_input.text()
        medicines = self.medicine_input.text()
        
        # Construct the QUrl from the local file path
        logo_path = "Resource/big_logo.png"
        logo_url = QUrl.fromLocalFile(logo_path)

        # Load the image using QImage
        image = QImage(logo_path)

        # Convert QImage to QByteArray
        image_byte_array = QByteArray()
        buffer = QBuffer(image_byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, "PNG")

        # Encode the QByteArray to Base64 to create a data URL
        image_data_url = "data:image/png;base64," + image_byte_array.toBase64().data().decode()

        # Update the HTML content to use the data URL for the image
        html_content = f"""
        <html>
            <body>
                <h2>Prescription/Invoice</h2>
                <p><strong>Doctor Name:</strong> {doctor_name}</p>
                <p><strong>Patient Name:</strong> {patient_name}</p>
                <p><strong>Prescription:</strong> {prescription}</p>
                <p><strong>Medicine(s) Bought:</strong> {medicines}</p>
                <img src="{image_data_url}" alt="Image Description">
            </body>
        </html>
        """

        # Display HTML content in the QWebEngineView
        self.web_view.setHtml(html_content)

    def print_html(self):
        # Print the HTML content directly
        print("1")
        printer = QPrinter()
        print("2")
        self.handle_paint_request(printer)
        print("3")

    def handle_paint_request(self, printer):
        # Handle paint request for direct printing
        print("a")
        self.web_view.page().print(printer, self.print_finished)
        print("b")

    def print_finished(self, success):
        if success:
            print("Print successful!")
        else:
            print("Print failed!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrescriptionWindow()
    window.show()
    sys.exit(app.exec_())
