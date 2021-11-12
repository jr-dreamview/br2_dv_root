import sys

from PySide2.QtCore import QItemSelectionModel, QSize, QSortFilterProxyModel, Qt, Signal
from PySide2.QtGui import QBrush, QColor, QStandardItem, QStandardItemModel, QTextDocument
from PySide2.QtWidgets import (QComboBox, QDialog, QHBoxLayout, QLabel, QStyledItemDelegate, QTreeView,
                               QVBoxLayout, QWidget)
from shiboken2 import wrapInstance

maya_path = r"C:\Users\john.russell\Code\git_stuff\dreamview-studios-inc\DreamViewStudios\application\maya"
if maya_path not in sys.path:
    sys.path.append(maya_path)
from br2.dv_root_node.node_handler import MayaRootHandler
from br2.update_assets.maya_utils import get_all_dv_root_nodes, get_main_window_ptr
from br2.update_assets.test_db import get_versions_data
from br2.update_assets.test_version_swap import swap_version


COL_LBL_ASSET = "Asset"
COL_LBL_VERSION = "Version in Scene"
COL_LBL_USER = "User"
COL_LBL_DATE = "Date Created"
COL_LBL_KIND = "Kind"
COL_LBL_STATUS = "Status"
COLUMN_HEADERS = [
    COL_LBL_ASSET,
    COL_LBL_VERSION,
    COL_LBL_USER,
    COL_LBL_DATE,
    COL_LBL_KIND,
    COL_LBL_STATUS
]


class ImportWidget(QWidget):
    def __init__(self, parent=None):
        """

        Args:
            parent (PySide2.QtCore.QObject):
        """
        super(ImportWidget, self).__init__(parent)

        # UI widgets
        # self.cmbo_bx_tasks = None
        self.lbl_tasks = None
        self.tree_view = None
        self.source_model = None

        self.setup_ui()

    def connect_signals(self):
        """

        """
        self.source_model.itemChanged.connect(self.source_model.swap_ver)
        self.source_model.rows_updated.connect(self.resize_columns)

    def resize_columns(self):
        """

        """
        header = self.tree_view.header()
        header.setSectionResizeMode(header.ResizeToContents)
        header.resizeSections()
        # header.resizeSections(header.ResizeToContents)

    def setup_ui(self):
        """

        """
        self.tree_view = QTreeView(self)
        self.tree_view.setAlternatingRowColors(True)

        # Model
        proxy_model = QSortFilterProxyModel(self.tree_view)
        self.source_model = ModelImport(self.tree_view)
        proxy_model.setSourceModel(self.source_model)
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

        self.source_model.populate()
        self.tree_view.expandAll()


class ModelImport(QStandardItemModel):
    # roles
    asset_data_role = Qt.UserRole
    latest_version_role = Qt.UserRole + 1
    node_role = Qt.UserRole + 2
    row_type_role = Qt.UserRole + 3
    vers_size_hint_width_role = Qt.UserRole + 4
    vers_text_role = Qt.UserRole + 5

    # signal
    rows_updated = Signal()

    def __init__(self, parent=None):
        """Initialize model.

        Args:
            parent (PySide2.QtCore.QObject):
        """
        self.column_label_indexes = {}

        super(ModelImport, self).__init__(parent)

    def get_column_header_label(self, index):
        """

        Args:
            index (PySide2.QtCore.QModelIndex):

        Returns:
            str:
        """
        return self.horizontalHeaderItem(index.column()).text()

    def populate(self):
        """

        """
        self.beginResetModel()
        self.clear()
        self.setHorizontalHeaderLabels(COLUMN_HEADERS)
        self.endResetModel()

        kinds = {}
        for node_name in get_all_dv_root_nodes():
            node_handler = MayaRootHandler(node_name)
            kind = node_handler.asset_type
            if kinds.get(kind) is None:
                kinds[kind] = QStandardItem(kind)
                self.invisibleRootItem().appendRow(kinds.get(kind))
            item_kind = kinds.get(kind)

            items_row = []
            version_item = None
            for c in range(self.columnCount()):
                column = self.horizontalHeaderItem(c).text()
                if column not in self.column_label_indexes:
                    self.column_label_indexes[column] = c
                item = QStandardItem()
                if column != COL_LBL_VERSION:
                    item.setEditable(False)
                else:
                    version_item = item
                    item.setTextAlignment(Qt.AlignCenter)
                items_row.append(item)
            item_kind.appendRow(items_row)

            # Get all versions data from asset.
            current_row = item_kind.rowCount() - 1
            index_version = self.index(
                current_row, self.column_label_indexes[COL_LBL_VERSION], self.indexFromItem(item_kind))
            versions_data = get_versions_data(node_handler.dpack_id)
            latest_version = sorted([v.version_fc for v in versions_data])[-1]

            version_text = {}
            max_width_size = None
            for asset in sorted(versions_data, key=lambda x: x.version_fc, reverse=True):
                text = "{} | {} | {} | {}".format(asset.version_fc, asset.user, asset.date_created, asset.status)
                version_text[asset.version_fc] = text
                document = QTextDocument(text)
                size = document.idealWidth() + 10  # width of combo box text plus arrow control
                if max_width_size is None or size > max_width_size:
                    max_width_size = size

            self.blockSignals(True)
            self.setData(index_version, versions_data, role=self.asset_data_role)
            self.setData(index_version, latest_version, role=self.latest_version_role)
            self.setData(index_version, node_name, role=self.node_role)
            self.setData(index_version, max_width_size, role=self.vers_size_hint_width_role)
            self.setData(index_version, version_text, role=self.vers_text_role)
            self.blockSignals(False)

            self.update_row(version_item, initialize=True)
        self.rows_updated.emit()

    def swap_ver(self, item):
        """

        Args:
            item (PySide2.QtGui.QStandardItem):
        """
        index = self.indexFromItem(item)
        model = index.model()
        if self.get_column_header_label(index) != COL_LBL_VERSION:
            return
        versions = model.data(index, self.asset_data_role)
        node = model.data(index, self.node_role)
        version = item.text()
        new_ver = [v for v in versions if v.version_fc == version][0]

        swap_version(node, new_ver)

        self.update_row(item)
        self.rows_updated.emit()

    def update_row(self, version_item, initialize=False):
        """

        Args:
            version_item (PySide2.QtGui.QStandardItem):
            initialize (bool):
        """
        index = self.indexFromItem(version_item)
        node_name = self.data(index, self.node_role)
        node_handler = MayaRootHandler(node_name)
        latest_ver = self.data(index, self.latest_version_role)
        version = node_handler.version

        bg_color = None
        fg_color = QColor.fromRgba(4291348680)  # from Maya stylesheet
        if latest_ver != version:
            bg_color = Qt.yellow
            fg_color = Qt.blue
        for c in range(self.columnCount()):
            idx = index.siblingAtColumn(c)
            cur_item = self.itemFromIndex(idx)
            column_header_label = self.get_column_header_label(idx)

            # update colors
            if initialize and column_header_label == COL_LBL_VERSION:
                self.blockSignals(True)
            cur_item.setBackground(QBrush(bg_color))
            cur_item.setForeground(QBrush(fg_color))
            if initialize and column_header_label == COL_LBL_VERSION:
                self.blockSignals(False)

            # update item text
            if initialize:
                if column_header_label == COL_LBL_ASSET:
                    cur_item.setText(node_name)
                elif column_header_label == COL_LBL_VERSION:
                    self.blockSignals(True)
                    cur_item.setText(version)
                    self.blockSignals(False)
                elif column_header_label == COL_LBL_KIND:
                    cur_item.setText(node_handler.file_type)
            if column_header_label in [COL_LBL_ASSET, COL_LBL_VERSION]:
                continue
            if column_header_label == COL_LBL_USER:
                cur_item.setText(node_handler.user)
            elif column_header_label == COL_LBL_DATE:
                cur_item.setText(node_handler.date_created)
            elif column_header_label == COL_LBL_STATUS:
                cur_item.setText(node_handler.status)


class TreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        """Initialize the Delegate.

        Args:
            parent (PySide2.QtCore.QObject):
        """
        super(TreeDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        """Returns the editor to be used for editing the data item with the given index. Note that the index contains
        information about the model being used. The editor’s parent widget is specified by parent, and the item options
        by option.

        Args:
            parent (PySide2.QtWidgets.QWidget):
            option (PySide2.QtWidgets.QStyleOptionViewItem):
            index (PySide2.QtCore.QModelIndex):

        Returns:
            PySide2.QtWidgets.QWidget:
        """
        idx = index.model().mapToSource(index)
        model = idx.model()
        if model.get_column_header_label(idx) == COL_LBL_VERSION:
            return QComboBox(parent)
        return super(TreeDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """Sets the data for the item at the given index in the model to the contents of the given editor.

        Args:
            editor (PySide2.QtWidgets.QWidget):
            index (PySide2.QtCore.QModelIndex):
        """
        idx = index.model().mapToSource(index)
        model = idx.model()
        if model.get_column_header_label(idx) == COL_LBL_VERSION:
            current_ver = model.data(idx, role=Qt.DisplayRole)
            current_ver_index = None
            editor.view().setAlternatingRowColors(True)
            ver_text_dict = model.data(idx, role=model.vers_text_role)
            for i, ver in enumerate(sorted(ver_text_dict, reverse=True)):
                editor.addItem(ver_text_dict[ver], userData=ver)
                if i == 0:
                    # Set color
                    editor.setItemData(i, QBrush(Qt.green), role=Qt.BackgroundRole)
                    editor.setItemData(i, QBrush(Qt.magenta), role=Qt.ForegroundRole)
                if current_ver == ver:
                    current_ver_index = i
            editor.setCurrentIndex(current_ver_index)
            return
        return super(TreeDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """Sets the data for the item at the given index in the model to the contents of the given editor.

        Args:
            editor (PySide2.QtWidgets.QWidget):
            model (PySide2.QtCore.QSortFilterProxyModel):
            index (PySide2.QtCore.QModelIndex):
        """
        idx = model.mapToSource(index)
        if model.sourceModel().get_column_header_label(idx) == COL_LBL_VERSION:
            model.setData(index, editor.itemData(editor.currentIndex(), role=Qt.UserRole))
            return
        return super(TreeDelegate, self).setModelData(editor, model, index)

    def sizeHint(self, option, index):
        """

        Args:
            option (PySide2.QtWidgets.QStyleOptionViewItem):
            index (PySide2.QtCore.QModelIndex):

        Returns:
            PySide2.QtCore.QSize:
        """
        proxy_model = index.model()
        idx = proxy_model.mapToSource(index)
        model = proxy_model.sourceModel()
        if (model.get_column_header_label(idx) == COL_LBL_VERSION
                and not model.itemFromIndex(idx.siblingAtColumn(0)).hasChildren()):
            size = QSize(model.data(idx, role=model.vers_size_hint_width_role) + 10, option.fontMetrics.height())
            return size

        return super(TreeDelegate, self).sizeHint(option, index)


def get_maya_main_window():
    """Get the Maya main window.

    Returns:
        PySide2.QtWidgets.QWidget: 'MainWindow' Maya main window.
    """
    ptr = get_main_window_ptr()
    if ptr is not None:
        return wrapInstance(int(ptr), QWidget)


if __name__ == "__main__":
    dialog = QDialog(get_maya_main_window())
    dialog.setWindowTitle("Update")
    import_widget = ImportWidget(dialog)
    lyt_v_dialog = QVBoxLayout()
    lyt_v_dialog.addWidget(import_widget)
    dialog.setLayout(lyt_v_dialog)
    dialog.resize(1000, dialog.sizeHint().height())

    dialog.show()
