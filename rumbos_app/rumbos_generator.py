import os
import csv
import sys
import tempfile
import shutil
from pathlib import Path

from PySide6.QtGui import QPixmap, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from gui.rumbos_ui import Ui_MainWindow
from workers import DataProcessor, MapGenerator, Rumboscreator, GenerateGraph


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initializeUI()

    def initializeUI(self):
        self.setUpMainWindow()
        self.createActions()
        self.show()

    def setUpMainWindow(self):
        self.coordinate_csv = None

        self.ui.generate_btn.setDisabled(True)
        self.ui.generate_btn.setToolTip("Generate Rumbos Table")
        self.ui.generate_btn.setStatusTip("Generate Rumbos Table")
        self.ui.save_btn.setDisabled(True)
        self.ui.save_btn.setToolTip("Save Files")
        self.ui.save_btn.setStatusTip("Save Files")
        self.ui.clear_btn.setDisabled(True)
        self.ui.clear_btn.setToolTip("Clear All")
        self.ui.clear_btn.setStatusTip("Clear All")
        self.ui.crs_tedit.setText("epsg:32616")
        self.ui.crs_tedit.setToolTip(
            "Stablish the Origin of Coordinate system of the CSV File"
        )
        self.ui.crs_tedit.setStatusTip("Only allowed UTM projections formats")
        self.ui.crs_tedit.setDisabled(True)

        self.model_coordinate = QStandardItemModel()
        self.ui.coordinate_table.verticalHeader().setVisible(False)
        self.ui.coordinate_table.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.ui.coordinate_table.setModel(self.model_coordinate)
        self.model_coordinate.setRowCount(1)
        self.model_coordinate.setColumnCount(3)

        self.model_rumbos = QStandardItemModel()
        self.ui.rumbos_table.verticalHeader().setVisible(False)
        self.ui.rumbos_table.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.ui.rumbos_table.setModel(self.model_rumbos)
        self.model_rumbos.setRowCount(1)
        self.model_rumbos.setColumnCount(7)

    def createActions(self):
        self.ui.actionAdd_CSV_File.setShortcut("Ctrl+O")
        self.ui.actionAdd_CSV_File.triggered.connect(self.openCsvFile)
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave.triggered.connect(self.saveAll)
        self.ui.actionSave.setDisabled(True)
        self.ui.actionClear.setShortcut("Ctrl+W")
        self.ui.actionClear.triggered.connect(self.clearAll)
        self.ui.actionClear.setDisabled(True)
        self.ui.actionQuit.setShortcut("Ctrl+Q")
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.generate_btn.clicked.connect(self.generateRumbos)
        self.ui.save_btn.clicked.connect(self.saveAll)
        self.ui.clear_btn.clicked.connect(self.clearAll)

    def openCsvFile(self):
        """Open a CSV file with the header punto,x,y."""
        MANDATORY_HEADERS = ["punto", "x", "y"]

        self.coordinate_csv, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "CSV Files (*.csv)"
        )
        if self.coordinate_csv:
            with open(self.coordinate_csv, "r") as csv_f:
                reader = csv.reader(csv_f)
                header_labels = next(reader)
                if header_labels == MANDATORY_HEADERS:
                    self.model_coordinate.setHorizontalHeaderLabels(header_labels)
                    for i, row in enumerate(csv.reader(csv_f)):
                        items = [QStandardItem(item) for item in row]
                        self.model_coordinate.insertRow(i, items)

                    self.ui.crs_tedit.setDisabled(False)
                    self.ui.generate_btn.setDisabled(False)
                    self.ui.generate_btn.setDisabled(False)
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        """<p>Error processing the CSV file selected,
                        Please review your document and make sure that
                        the CSV file have the following headers
                        <b>punto,x,y</b></p>""",
                        QMessageBox.StandardButton.Ok,
                    )
            self.ui.clear_btn.setDisabled(False)
            self.ui.actionClear.setDisabled(False)

    def generateRumbos(self):
        self.file_name_file_csv = os.path.splitext(
            os.path.basename(self.coordinate_csv)
        )[0]
        self.target_dir = Path(tempfile.mkdtemp())
        self.target_names = {
            "rumbos": f"rumbos_{self.file_name_file_csv}.csv",
            "description": f"description_{self.file_name_file_csv}.txt",
            "web_map": f"web_map_{self.file_name_file_csv}.html",
            "plot": f"plot_{self.file_name_file_csv}.png",
        }

        self.rumbos_output_file = os.path.join(
            self.target_dir, self.target_names["rumbos"]
        )
        self.rumbos_table_generated = Rumboscreator(
            self.coordinate_csv, self.rumbos_output_file
        )
        self.rumbos_table_generated.generate_rumbos()

        with open(self.rumbos_output_file, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            self.model_rumbos.setHorizontalHeaderLabels(header_labels)
            for i, row in enumerate(csv.reader(csv_f)):
                items = [QStandardItem(item) for item in row]
                self.model_rumbos.insertRow(i, items)

        self.description_output_file = os.path.join(
            self.target_dir, self.target_names["description"]
        )
        self.generate_processed_paragraph = DataProcessor(
            self.rumbos_output_file, self.description_output_file
        )
        self.generate_processed_paragraph.process_data()
        self.generate_processed_paragraph.save_to_file()

        # Generate Web Map location
        self.csr_origin = self.ui.crs_tedit.text()
        self.web_map_output_file = os.path.join(
            self.target_dir, self.target_names["web_map"]
        )
        self.generate_web_map = MapGenerator(
            self.coordinate_csv, self.csr_origin, self.web_map_output_file
        )
        self.generate_web_map.generate_map()

        self.ui.coordinate_table.repaint()
        self.ui.rumbos_table.repaint()

        self.plot_output_file = os.path.join(self.target_dir, self.target_names["plot"])

        self.plot = GenerateGraph(self.coordinate_csv, self.plot_output_file)
        self.plot.generate()
        self.pixmap = QPixmap(self.plot_output_file)
        self.ui.graph_label.setPixmap(self.pixmap)

        self.ui.actionSave.setDisabled(False)
        self.ui.save_btn.setDisabled(False)

    def saveAll(self):
        self.file_path_to_save = QFileDialog.getExistingDirectory(
            self, "Select Folder to Save Files", os.path.curdir
        )

        list_files_to_save = [
            self.rumbos_output_file,
            self.description_output_file,
            self.web_map_output_file,
            self.plot_output_file,
        ]

        file_name = ["rumbos", "description", "web_map", "plot"]

        if self.file_path_to_save:
            for source_file, name_file in zip(list_files_to_save, file_name):
                shutil.copy(
                    source_file,
                    os.path.join(self.file_path_to_save, self.target_names[name_file]),
                )
            QMessageBox.information(
                self,
                "Files Successfully Saved",
                f"""<p><b>Files successfully saved to:</b>
                <br>{self.file_path_to_save}
                <br><b>Files:</b><br>
                - {'<br>- '.join(list(self.target_names.values()))}</p>""",
            )

    def clearAll(self):
        self.coordinate_csv = None
        self.target_dir = None

        self.model_coordinate.clear()
        self.ui.coordinate_table.setModel(self.model_coordinate)
        self.model_rumbos.clear()
        self.ui.rumbos_table.setModel(self.model_rumbos)

        self.ui.graph_label.clear()
        self.ui.graph_label.setText("Graph")
        self.plot.reset()

        self.ui.actionSave.setDisabled(True)
        self.ui.save_btn.setDisabled(True)
        self.ui.generate_btn.setDisabled(True)
        self.ui.clear_btn.setDisabled(True)
        self.ui.crs_tedit.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
