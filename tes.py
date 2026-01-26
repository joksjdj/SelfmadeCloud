import sys
import os
#pip install PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QListView, QSplitter
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Cloud Explorer")
        self.setGeometry(100, 100, 800, 600)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sidebar tree
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Folders"])
        self.tree = QTreeView()
        self.tree.setModel(self.tree_model)
        self.tree.clicked.connect(self.on_tree_clicked)

        # File list
        self.list_model = QStandardItemModel()
        self.list_model.setHorizontalHeaderLabels(["Files"])
        self.list_view = QListView()
        self.list_view.setModel(self.list_model)

        splitter.addWidget(self.tree)
        splitter.addWidget(self.list_view)
        splitter.setSizes([250, 550])
        self.setCentralWidget(splitter)

        # Populate tree starting at cloud folder
        cloud_path = r"cloud"  # <-- change this path to your cloud folder
        self.populate_tree(cloud_path)

    def populate_tree(self, path, parent=None):
        if parent is None:
            parent = self.tree_model.invisibleRootItem()
        try:
            for name in os.listdir(path):
                full_path = os.path.join(path, name)
                if os.path.isdir(full_path):
                    item = QStandardItem(name)
                    item.setData(full_path, Qt.ItemDataRole.UserRole)
                    parent.appendRow(item)
                    # Optional: populate first level
                    # self.populate_tree(full_path, item)
        except PermissionError:
            pass

    def on_tree_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        path = item.data(Qt.ItemDataRole.UserRole)
        self.list_model.clear()
        self.list_model.setHorizontalHeaderLabels(["Files"])
        try:
            for f in os.listdir(path):
                if os.path.isfile(os.path.join(path, f)):
                    self.list_model.appendRow(QStandardItem(f))
        except PermissionError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())