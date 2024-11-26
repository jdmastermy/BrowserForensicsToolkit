
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QPushButton, QComboBox,
    QLineEdit, QHBoxLayout, QFileDialog, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from modules.parsing import find_browser_profile_files, extract_history, extract_downloads, extract_cookies
from modules.utils import write_to_csv
import json
from pandas import DataFrame

class BrowserDataParserApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Browser Data Parser")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget(self.central_widget)
        self.main_layout.addWidget(self.tab_widget)

        self.history_tab = self.create_tab("History", ["Visit Time", "URL", "Title", "Visit Count", "Visit Type", "Duration", "Browser", "User Profile", "Source"])
        self.downloads_tab = self.create_tab("Downloads", ["Start Time", "End Time", "File Path", "Total Bytes", "Received Bytes", "Danger Type", "Interrupt Reason", "Opened", "Browser", "User Profile", "Source"])
        self.cookies_tab = self.create_tab("Cookies", ["Host", "Name", "Value", "Creation Time", "Last Access Time", "Expiry Time", "Secure", "HTTP Only", "Browser", "User Profile", "Source"])

        self.tab_widget.addTab(self.history_tab, "History")
        self.tab_widget.addTab(self.downloads_tab, "Downloads")
        self.tab_widget.addTab(self.cookies_tab, "Cookies")

        self.controls_layout = QHBoxLayout()
        self.main_layout.addLayout(self.controls_layout)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.controls_layout.addWidget(self.progress_bar)

        self.root_folder_btn = QPushButton("Select Root Folder", self)
        self.root_folder_btn.clicked.connect(self.select_root_folder)
        self.controls_layout.addWidget(self.root_folder_btn)

        self.output_folder_btn = QPushButton("Select Output Folder", self)
        self.output_folder_btn.clicked.connect(self.select_output_folder)
        self.controls_layout.addWidget(self.output_folder_btn)

        self.start_btn = QPushButton("Start Parsing", self)
        self.start_btn.clicked.connect(self.start_parsing)
        self.controls_layout.addWidget(self.start_btn)

        self.export_button = QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_results)
        self.file_type_dropdown = QComboBox(self)
        self.file_type_dropdown.addItems(["CSV", "JSON", "TXT", "HTML"])
        self.controls_layout.addWidget(self.file_type_dropdown)
        self.controls_layout.addWidget(self.export_button)

        self.status_label = QLabel("Status: Ready", self)
        self.controls_layout.addWidget(self.status_label)

        self.root_folder = ""
        self.output_folder = ""

    def create_tab(self, title, headers):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        search_layout = QHBoxLayout()
        search_bar = QLineEdit(tab)
        search_bar.setPlaceholderText(f"Search {title}...")
        search_button = QPushButton("Search", tab)
        search_layout.addWidget(search_bar)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Data Table
        table = QTableWidget(tab)
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.setSortingEnabled(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table)
        table.setObjectName(f"{title.lower()}_table")

        search_button.clicked.connect(lambda: self.search_table(table, search_bar.text()))

        return tab

    def update_table(self, table_widget, data):
        table_widget.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def search_table(self, table_widget, keyword):
        for row in range(table_widget.rowCount()):
            match = False
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item and keyword.lower() in item.text().lower():
                    match = True
                    break
            table_widget.setRowHidden(row, not match)

    def select_root_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Root Folder")
        if folder:
            self.root_folder = folder
            self.status_label.setText(f"Root Folder: {folder}")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.status_label.setText(f"Output Folder: {folder}")

    
    def start_parsing(self):
        if not self.root_folder or not self.output_folder:
            QMessageBox.warning(self, "Error", "Please select both root and output folders!")
            return

        self.status_label.setText("Parsing started...")
        self.progress_bar.setValue(0)

        try:
            # Profile files
            profile_files = find_browser_profile_files(self.root_folder)

            # Parse History Files
            history_data = extract_history("chrome", profile_files.get("history", []), "default_user")
            history_table = self.history_tab.findChild(QTableWidget, "history_table")
            self.update_table(history_table, history_data)
            history_output = os.path.join(self.output_folder, "history.csv")
            write_to_csv(history_data, ["Visit Time", "URL", "Title", "Visit Count", "Visit Type", "Duration", "Browser", "User Profile", "Source"], history_output)

            # Parse Downloads
            downloads_data = extract_downloads("chrome", profile_files.get("history", []), "default_user")
            downloads_table = self.downloads_tab.findChild(QTableWidget, "downloads_table")
            self.update_table(downloads_table, downloads_data)
            downloads_output = os.path.join(self.output_folder, "downloads.csv")
            write_to_csv(downloads_data, ["Start Time", "End Time", "File Path", "Total Bytes", "Received Bytes", "Danger Type", "Interrupt Reason", "Opened", "Browser", "User Profile", "Source"], downloads_output)

            # Parse Cookies
            cookies_data = extract_cookies("chrome", profile_files.get("cookies", []), "default_user")
            cookies_table = self.cookies_tab.findChild(QTableWidget, "cookies_table")
            self.update_table(cookies_table, cookies_data)
            cookies_output = os.path.join(self.output_folder, "cookies.csv")
            write_to_csv(cookies_data, ["Host", "Name", "Value", "Creation Time", "Last Access Time", "Expiry Time", "Secure", "HTTP Only", "Browser", "User Profile", "Source"], cookies_output)

            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Success", f"Parsing completed! Default CSV files saved in {self.output_folder}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_label.setText("Parsing failed!")

        if not self.root_folder or not self.output_folder:
            QMessageBox.warning(self, "Error", "Please select both root and output folders!")
            return

        self.status_label.setText("Parsing started...")
        self.progress_bar.setValue(0)

        try:
            # Profiles files
            profile_files = find_browser_profile_files(self.root_folder)

            # History Files
            history_data = extract_history("chrome", profile_files.get("history", []), "default_user")
            history_table = self.history_tab.findChild(QTableWidget, "history_table")
            self.update_table(history_table, history_data)

            # Downloads
            downloads_data = extract_downloads("chrome", profile_files.get("history", []), "default_user")
            downloads_table = self.downloads_tab.findChild(QTableWidget, "downloads_table")
            self.update_table(downloads_table, downloads_data)

            # Cookies
            cookies_data = extract_cookies("chrome", profile_files.get("cookies", []), "default_user")
            cookies_table = self.cookies_tab.findChild(QTableWidget, "cookies_table")
            self.update_table(cookies_table, cookies_data)

            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Success", "Parsing completed!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status_label.setText("Parsing failed!")

    def export_results(self):
        current_tab = self.tab_widget.currentWidget()
        table_widget = current_tab.findChild(QTableWidget)
        if table_widget is None:
            QMessageBox.warning(self, "Error", "No data to export!")
            return

        # Get data
        data = []
        headers = [table_widget.horizontalHeaderItem(col).text() for col in range(table_widget.columnCount())]
        for row in range(table_widget.rowCount()):
            if not table_widget.isRowHidden(row):
                row_data = [table_widget.item(row, col).text() if table_widget.item(row, col) else "" for col in range(table_widget.columnCount())]
                data.append(row_data)

        # Get file type
        file_type = self.file_type_dropdown.currentText().lower()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Results", "", f"{file_type.upper()} Files (*.{file_type})", options=options)
        if not file_path:
            return

        # Export data
        if file_type == "csv":
            write_to_csv(data, headers, file_path)
        elif file_type == "json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([dict(zip(headers, row)) for row in data], f, ensure_ascii=False, indent=4)
        elif file_type == "txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("    ".join(headers) + "\n")
                for row in data:
                    f.write("    ".join(row) + "\n")
        elif file_type == "html":
            df = DataFrame(data, columns=headers)
            df.to_html(file_path, index=False)
        else:
            QMessageBox.warning(self, "Error", f"Unsupported file format: {file_type}")
            return

        QMessageBox.information(self, "Success", f"Results exported to {file_path}!")

def main():
    app = QApplication(sys.argv)
    main_window = BrowserDataParserApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()