from PySide2.QtCore import QItemSelectionModel, QSortFilterProxyModel
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QTreeView, QVBoxLayout, QWidget
from shiboken2 import wrapInstance

import maya.OpenMayaUI as apiUI


COLUMN_HEADERS = [
    "Column 0",
    "Column 1",
    "Column 2"
]


class CheckInWidget(QWidget):
    def __init__(self, parent=None):
        super(CheckInWidget, self).__init__(parent)

        # UI widgets
        self.cmbo_bx_tasks = None
        self.lbl_tasks = None
        self.tree_view = None

        self.setup_ui()

    def connect_signals(self):
        pass

    def setup_ui(self):
        self.tree_view = QTreeView(self)

        proxy_model = QSortFilterProxyModel(self)
        source_model = ModelImport(self.tree_view)
        proxy_model.setSourceModel(source_model)
        self.tree_view.setModel(proxy_model)

        self.lbl_tasks = QLabel("Tasks")
        self.cmbo_bx_tasks = QComboBox(self)

        lyt_h_tasks = QHBoxLayout()
        lyt_h_tasks.addWidget(self.lbl_tasks)
        lyt_h_tasks.addWidget(self.cmbo_bx_tasks)

        lyt_v_main = QVBoxLayout()
        lyt_v_main.addLayout(lyt_h_tasks)
        lyt_v_main.addWidget(self.tree_view)
        self.setLayout(lyt_v_main)

        self.connect_signals()

        source_model.populate()


class ModelImport(QStandardItemModel):
    def __init__(self, parent=None):
        super(ModelImport, self).__init__(parent)

        self.setHorizontalHeaderLabels(COLUMN_HEADERS)

    def populate(self):
        for r in range(10):
            item_asset = QStandardItem(str(r))
            self.invisibleRootItem().appendRow(item_asset)
            for v in range(3):
                items_row = []
                for c in range(len(COLUMN_HEADERS)):
                    column = COLUMN_HEADERS[c]
                    item_column = QStandardItem("{}v, {}".format(3 - v, c))
                    items_row.append(item_column)
                item_asset.appendRow(items_row)


def get_maya_main_window():
    """Get the Maya main window.

    Returns:
        PySide2.QtWidgets.QWidget: 'MainWindow' Maya main window.
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QWidget)


if __name__ == "__main__":
    dialog = QDialog(get_maya_main_window())
    dialog.setWindowTitle("Check-In")
    import_widget = CheckInWidget(dialog)
    lyt_v_dialog = QVBoxLayout()
    lyt_v_dialog.addWidget(import_widget)
    dialog.setLayout(lyt_v_dialog)

    dialog.show()
