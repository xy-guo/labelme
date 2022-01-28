# -*- encoding: utf-8 -*-

from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import Qt

from .label_list_widget import HTMLDelegate

# from .escapable_qlist_widget import EscapableQListWidget


class UniqueLabelQListWidget(QtWidgets.QListView):
    def __init__(self):
        super(UniqueLabelQListWidget, self).__init__()
        # self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setWindowFlags(Qt.Window)
        self.setModel(QtGui.QStandardItemModel())
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setItemDelegate(HTMLDelegate())

    def mousePressEvent(self, event):
        super(UniqueLabelQListWidget, self).mousePressEvent(event)
        if not self.indexAt(event.pos()).isValid():
            self.clearSelection()
            return

    @property
    def itemChanged(self):
        return self.model().itemChanged

    def __len__(self):
        return self.model().rowCount()

    def __getitem__(self, i):
        return self.model().item(i)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def findItemsByLabel(self, label):
        items = []
        for row in range(self.model().rowCount()):
            item = self.model().item(row, 0)
            if item.data(Qt.UserRole) == label:
                items.append(item)
        return items

    def createItemFromLabel(self, label):
        item = QtGui.QStandardItem()
        item.setFlags(item.flags() | Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        item.setData(label, Qt.UserRole)
        return item

    def setItemLabel(self, item, label, color=None):
        # qlabel = QtWidgets.QLabel()
        if color is None:
            item.setText("{}".format(label))
        else:
            item.setText(
                '{} <font color="#{:02x}{:02x}{:02x}">●</font>'.format(label, *color)
            )
        # qlabel.setAlignment(Qt.AlignBottom)

        # item.setSizeHint(qlabel.sizeHint())
        item.setFlags(item.flags() | Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)

        # self.setItemWidget(item, qlabel)

    def addItem(self, item):
        if not isinstance(item, QtGui.QStandardItem):
            raise TypeError("item must be QtGui.QStandardItem")
        self.model().setItem(self.model().rowCount(), 0, item)
        # item.setSizeHint(self.itemDelegate().sizeHint(None, None))

    def selectedItems(self):
        return [self.model().itemFromIndex(i) for i in self.selectedIndexes()]
