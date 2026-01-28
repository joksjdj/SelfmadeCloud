from pathlib import Path
import sys
import os
import json
import shutil
import zipfile
# pip install pyperclip
import pyperclip
# pip install PyQt5
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QMenu,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QPushButton, QListView, QMessageBox
)
from PyQt5.QtCore import QDir, QModelIndex
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 File Explorer")
        self.setGeometry(2000, 100, 1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Address bar
        address_layout = QHBoxLayout()
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.go_to_path)

        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.go_forward)

        # New buttons
        self.new_folder_button = QPushButton("New Folder")
        self.new_folder_button.clicked.connect(self.create_new_folder)

        self.new_file_button = QPushButton("New File")
        self.new_file_button.clicked.connect(self.create_new_file)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_item)

        # Add widgets to layout
        address_layout.addWidget(self.back_button)
        address_layout.addWidget(self.forward_button)
        address_layout.addWidget(self.address_bar)
        address_layout.addWidget(self.new_folder_button)
        address_layout.addWidget(self.new_file_button)
        address_layout.addWidget(self.delete_button)

        layout.addLayout(address_layout)


        # File system model
        path = os.path.abspath("Cloud")
        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
        self.model.setRootPath(path)

        self.tree_model = QFileSystemModel()
        self.tree_model.setReadOnly(False)
        self.tree_model.setRootPath(path)
        self.tree_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)  # <-- folders only

        # Tree view (left)
        self.tree = QTreeView()
        self.tree.setModel(self.tree_model)
        tree_index = self.tree_model.index(path)
        self.tree.setRootIndex(tree_index)
        self.tree.setColumnWidth(0, 300)
        self.tree.clicked.connect(self.on_tree_clicked)

        # List view (right)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        list_index = self.model.index(path)  # <-- must use self.model here
        self.list_view.setRootIndex(list_index)
        self.list_view.doubleClicked.connect(self.on_list_double_clicked)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_list_context_menu)

        # Enable drag & drop
        for view in (self.tree, self.list_view):
            view.setDragEnabled(True)
            view.setAcceptDrops(True)
            view.viewport().setAcceptDrops(True)
            view.setDropIndicatorShown(True)
            view.setDragDropMode(view.DragDrop)
            view.setDefaultDropAction(Qt.MoveAction)

        # 🔥 SPLITTER (Explorer-style)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.list_view)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        # History for back/forward
        self.history = []
        self.history_index = -1


    # Navigation functions
    def go_to_path(self):
        path = self.address_bar.text()
        if os.path.exists(path):
            self.set_path(path)

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.set_path(self.history[self.history_index], add_history=False)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.set_path(self.history[self.history_index], add_history=False)

    def set_path(self, path, add_history=True):
        index = self.model.index(path)
        if index.isValid():
            self.tree.setCurrentIndex(index)
            self.tree.expand(index)
            self.list_view.setRootIndex(index)
            self.address_bar.setText(path)
            if add_history:
                self.history = self.history[:self.history_index+1]
                self.history.append(path)
                self.history_index += 1

    def on_tree_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        self.set_path(path)

    def on_list_double_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.set_path(path)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))


    # Interactive functions for files and folders
    def create_new_folder(self):
        current_path = self.address_bar.text()
        if os.path.isdir(current_path):
            folder_name = "New Folder"
            new_path = Path(current_path) / folder_name
            counter = 1
            while new_path.exists():
                new_path = Path(current_path) / f"{folder_name} ({counter})"
                counter += 1
            try:
                new_path.mkdir()
                self.set_path(current_path)  # refresh list view
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create folder:\n{e}")

    def create_new_file(self):
        current_path = self.address_bar.text()
        if os.path.isdir(current_path):
            file_name = "New File.txt"
            new_path = Path(current_path) / file_name
            counter = 1
            while new_path.exists():
                new_path = Path(current_path) / f"New File ({counter}).txt"
                counter += 1
            try:
                new_path.touch()
                self.set_path(current_path)  # refresh list view
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create file:\n{e}")

    def delete_item(self):
        # Get selected index in list view
        index = self.list_view.currentIndex()
        if not index.isValid():
            QMessageBox.information(self, "Delete", "No file or folder selected.")
            return

        path = self.model.filePath(index)
        reply = QMessageBox.question(
            self,
            "Delete",
            f"Are you sure you want to delete:\n{path}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(path):
                    os.rmdir(path)  # only works if folder is empty
                else:
                    os.remove(path)
                self.set_path(self.address_bar.text())  # refresh
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete:\n{e}")


    def show_list_context_menu(self, position):
        index = self.list_view.indexAt(position)
        if not index.isValid():
            return

        path = self.model.filePath(index)
        menu = QMenu()

        # Rename
        rename_action = menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.list_view.edit(index))

        # Copy path
        copy_action = menu.addAction("Copy path")
        copy_action.triggered.connect(lambda: self.copy_item_path(path))

        # Compress / Extract
        if os.path.isdir(path):
            compress_action = menu.addAction("Compress folder")
            compress_action.triggered.connect(lambda: self.compress_folder(path))
        elif path.lower().endswith(".zip"):
            extract_action = menu.addAction("Extract zip")
            extract_action.triggered.connect(lambda: self.extract_zip(path))

        menu.exec_(self.list_view.viewport().mapToGlobal(position))

    def copy_item_path(self, path):
        pyperclip.copy(path)  # copies path to clipboard
        QMessageBox.information(self, "Copy", f"Copied path:\n{path}")

    def compress_folder(self, path):
        zip_path = f"{path}.zip"
        try:
            shutil.make_archive(path, 'zip', path)
            QMessageBox.information(self, "Compress", f"Compressed to:\n{zip_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not compress:\n{e}")

    def extract_zip(self, path):
        extract_to = str(Path(path).parent / Path(path).stem)
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            QMessageBox.information(self, "Extract", f"Extracted to:\n{extract_to}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not extract:\n{e}")


    def closeEvent(self, event):
        # Clear all internal variables
        self.history = []
        self.history_index = -1
        self.address_bar.clear()
        
        # Clear models (tree and list)
        if hasattr(self, 'tree_model'):
            self.tree_model = None
        if hasattr(self, 'list_model'):
            self.list_model = None
        if hasattr(self, 'model'):
            self.model = None
        
        # Optional: delete child widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec())
