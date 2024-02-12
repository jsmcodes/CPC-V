import os
import subprocess

def convert_ui_to_python(ui_file_path):
    ui_file_name = os.path.basename(ui_file_path)
    ui_name_without_extension = os.path.splitext(ui_file_name)[0]

    python_file_path = os.path.join(os.path.dirname(ui_file_path), f"{ui_name_without_extension}.py")

    command = f"pyuic5 -x {ui_file_path} -o {python_file_path}"
    subprocess.run(command, shell=True)

    print(f"Conversion completed: {ui_file_name} -> {os.path.basename(python_file_path)}")

def convert_all_ui_files(ui_folder):
    ui_files = [file for file in os.listdir(ui_folder) if file.endswith(".ui")]

    for ui_file in ui_files:
        ui_file_path = os.path.join(ui_folder, ui_file)
        convert_ui_to_python(ui_file_path)

if __name__ == "__main__":
    ui_folder = "UI"
    convert_all_ui_files(ui_folder)
