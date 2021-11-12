from PySide2.QtCore import QItemSelectionModel, QModelIndex, QSortFilterProxyModel, Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QComboBox, QDialog, QHBoxLayout, QLabel, QStyledItemDelegate, QTreeView, QVBoxLayout, QWidget, QListView
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI


COLUMN_HEADERS = [
    "Asset",
    "Version in Scene",
    "User"
]


class AssetComboBox(QComboBox):
    def __init__(self, parent=None):
        super(AssetComboBox, self).__init__(parent)


class ImportWidget(QWidget):
    def __init__(self, parent=None):
        super(ImportWidget, self).__init__(parent)

        # UI widgets
        # self.cmbo_bx_tasks = None
        self.lbl_tasks = None
        self.tree_view = None

        self.setup_ui()

    def connect_signals(self):
        pass

    def setup_ui(self):
        self.tree_view = QTreeView(self)
        self.tree_view.setAlternatingRowColors(True)

        # Model
        proxy_model = QSortFilterProxyModel(self.tree_view)
        source_model = ModelImport(self.tree_view)
        proxy_model.setSourceModel(source_model)
        self.tree_view.setModel(proxy_model)

        # Delegate
        delegate = TreeDelegate(self.tree_view)
        self.tree_view.setItemDelegate(delegate)

        # Selection Model
        sel_model = QItemSelectionModel(proxy_model)
        self.tree_view.setSelectionModel(sel_model)

        # Layout
        lyt_v_main = QVBoxLayout()

        # lyt_h_tasks = QHBoxLayout()
        # self.lbl_tasks = QLabel("Tasks")
        # self.cmbo_bx_tasks = QComboBox(self)
        # lyt_h_tasks.addWidget(self.lbl_tasks)
        # lyt_h_tasks.addWidget(self.cmbo_bx_tasks)
        # lyt_v_main.addLayout(lyt_h_tasks)

        lyt_v_main.addWidget(self.tree_view)
        self.setLayout(lyt_v_main)

        self.connect_signals()

        source_model.populate()
        self.tree_view.expandAll()

        source_model.get_indexes(proxy_model.mapToSource(self.tree_view.rootIndex()))


class ModelImport(QStandardItemModel):
    asset_data_role = Qt.UserRole

    def __init__(self, parent=None):
        """Initialize model.

        Args:
            parent (PySide2.QtCore.QObject):
        """
        super(ModelImport, self).__init__(parent)

        self.setHorizontalHeaderLabels(COLUMN_HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        """

        Args:
            index (PySide2.QtCore.QModelIndex):
            role (int):

        Returns:
            object:
        """
        return super(ModelImport, self).data(index, role)

    def get_indexes(self, index):
        """

        Args:
            index (PySide2.QtCore.QModelIndex):

        Returns:

        """
        if index.isValid():
            print(f"{index.row()}, {index.column()}, {self.data(index, role=self.asset_data_role)}")
        if not self.hasChildren(index) or (index.flags() & Qt.ItemNeverHasChildren):
            return

        for r in range(self.rowCount(index)):
            for c in range(self.columnCount(index)):
                self.get_indexes(self.index(r, c, index))

    def populate(self):
        dv_root_nodes = cmds.ls(type="br2DvRootNode")
        kinds = {}
        for r in dv_root_nodes:
            kind = cmds.getAttr(f"{r}.asset_type")
            if kinds.get(kind) is None:
                kinds[kind] = QStandardItem(kind)
                self.invisibleRootItem().appendRow(kinds.get(kind))
            item_kind = kinds.get(kind)

            items_row = []
            for column in COLUMN_HEADERS:
                if column == "Asset":
                    item = QStandardItem(str(r))
                    item.setEditable(False)
                    items_row.append(item)
                elif column == "User":
                    item = QStandardItem(cmds.getAttr(f"{r}.user"))
                    item.setEditable(False)
                    items_row.append(item)
                else:
                    item = QStandardItem(cmds.getAttr(f"{r}.version"))
                    # item.setBackground(Qt.green)
                    items_row.append(item)
            item_kind.appendRow(items_row)

            current_row = item_kind.rowCount() - 1
            index_version = self.index(
                current_row, COLUMN_HEADERS.index("Version in Scene"), self.indexFromItem(item_kind))
            versions_data = get_versions_data(cmds.getAttr(f"{r}.dpack_id"))
            self.setData(index_version, versions_data, role=self.asset_data_role)

    def setData(self, index, value, role=Qt.EditRole):
        """

        Args:
            index (PySide2.QtCore.QModelIndex):
            value (object):
            role (int):

        Returns:
            bool:
        """
        return super(ModelImport, self).setData(index, value, role)


class TreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        self.tree = parent
        self.proxy_model = parent.model()
        self.model = parent.model().sourceModel()

        super(TreeDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        """

        Args:
            parent (PySide2.QtWidgets.QWidget):
            option (PySide2.QtWidgets.QStyleOptionViewItem):
            index (PySide2.QtCore.QModelIndex):

        Returns:
            PySide2.QtWidgets.QWidget:
        """
        if COLUMN_HEADERS[index.column()] == "Version in Scene":
            return QComboBox(parent)
        return super(TreeDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """

        Args:
            editor (PySide2.QtWidgets.QWidget):
            index (PySide2.QtCore.QModelIndex):
        """
        idx = self.proxy_model.mapToSource(index)
        if COLUMN_HEADERS[idx.column()] == "Version in Scene":
            idx = self.proxy_model.mapToSource(index)
            editor.view().setAlternatingRowColors(True)
            asset_data = self.model.data(idx, role=self.model.asset_data_role)
            item_versions = sorted([a.get("version_fc") for a in asset_data], reverse=True)
            # item_text = ["Item_3", "Item_2", "Item_1"]
            editor.addItems(item_versions)
            for i, text in enumerate(item_versions):
                if len(item_versions) == i:
                    bg_color = Qt.green
                else:
                    bg_color = Qt.yellow
                editor.setItemData(i, bg_color, Qt.BackgroundRole)
            return
        return super(TreeDelegate, self).setEditorData(editor, index)


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
    dialog.setWindowTitle("Update")
    import_widget = ImportWidget(dialog)
    lyt_v_dialog = QVBoxLayout()
    lyt_v_dialog.addWidget(import_widget)
    dialog.setLayout(lyt_v_dialog)

    dialog.show()
