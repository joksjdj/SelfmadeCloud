import os, sys
import subprocess
#pip install PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QListView, QSplitter
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

expanded_paths = []
class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Cloud Explorer")
        self.setGeometry(100, 100, 1200, 800)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Sidebar tree
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Folders"])
        self.tree = QTreeView()
        self.tree.setModel(self.tree_model)
        self.tree.clicked.connect(self.on_tree_clicked)

        # File list
        self.list_model = QStandardItemModel()
        self.list_view = QListView()
        self.list_view.setModel(self.list_model)
        self.list_view.doubleClicked.connect(self.on_body_doubleClicked)


        splitter.addWidget(self.tree)
        splitter.addWidget(self.list_view)
        splitter.setSizes([250, 550])
        self.setCentralWidget(splitter)

        # Populate tree starting at cloud folder
        cloud_path = r"cloud"  # <-- change this path to your cloud folder
        self.populate_tree(cloud_path, None)

    def populate_tree(self, path, parent):
        if parent is None:
            parent = self.tree_model.invisibleRootItem()
        try:
            for name in os.listdir(path):
                full_path = os.path.join(path, name)
                if os.path.isdir(full_path):
                    # For sidebar
                    tree_item = QStandardItem(name)
                    tree_item.setData(full_path, Qt.ItemDataRole.UserRole)
                    parent.appendRow(tree_item)

                # For body
                body_item = QStandardItem(name)
                body_item.setData(full_path, Qt.ItemDataRole.UserRole)
                self.list_model.appendRow(body_item)
        except PermissionError:
            pass

    # ----------------------------
    # Sidebar interactions
    # ----------------------------
    def on_tree_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        path = item.data(Qt.ItemDataRole.UserRole)
        self.list_model.setHorizontalHeaderLabels(["Files"])
        try:
            if path not in expanded_paths:
                self.list_model.clear()
                expanded_paths.append(path)
                self.tree.expand(index)
                self.populate_tree(path, item)
            else:
                item.removeRows(0, item.rowCount())
                self.tree.collapse(index)
                expanded_paths.remove(path)
        except PermissionError:
            pass
        
    # ----------------------------
    # Body
    # ----------------------------
    def on_body_doubleClicked(self, index):
        item = self.list_model.itemFromIndex(index)
        path = item.data(Qt.ItemDataRole.UserRole)

        if os.path.isdir(path):

            self.list_model.clear()
            self.populate_tree(path, item)

        elif os.path.isfile(path):
            if os.path.isfile(path):
                os.startfile(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())