import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QPushButton, QListView
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
        self.setGeometry(100, 100, 1000, 600)

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

        address_layout.addWidget(self.back_button)
        address_layout.addWidget(self.forward_button)
        address_layout.addWidget(self.address_bar)
        layout.addLayout(address_layout)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # Tree view (left)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setColumnWidth(0, 300)
        self.tree.clicked.connect(self.on_tree_clicked)

        # List view (right)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.doubleClicked.connect(self.on_list_double_clicked)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec())
