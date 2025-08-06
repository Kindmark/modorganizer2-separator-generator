# main_qt.py: Main entry for PySide6 app using ui_main_window.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QColorDialog, QStyledItemDelegate, QAbstractItemView, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QAction
from PySide6.QtCore import Qt, QSize
import backend as bck
from ui_main_window import Ui_MainWindow

class ColorBarDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        color = index.data(Qt.UserRole)
        if color and isinstance(color, str) and color.startswith('#') and len(color) == 7:
            painter.save()
            painter.fillRect(option.rect.x(), option.rect.y(), 4, option.rect.height(), QColor(color))
            painter.restore()
        # Shift the text rect to the right for spacing
        text_option = option
        text_option = QStyledItemDelegate.clone(self, option) if hasattr(QStyledItemDelegate, 'clone') else option
        text_option.rect = option.rect.adjusted(8, 0, 0, 0)  # 4px color + 4px space
        super().paint(painter, text_option, index)
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 20)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name"])
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setItemDelegateForColumn(0, ColorBarDelegate())
        self.ui.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.treeView.doubleClicked.connect(self.showEditPanel)
        self.ui.addBtn.clicked.connect(self.addSeparator)
        self.ui.removeBtn.clicked.connect(self.removeSeparator)
        self.ui.moveUpBtn.clicked.connect(lambda: self.moveSeparator(-1))
        self.ui.moveDownBtn.clicked.connect(lambda: self.moveSeparator(1))
        self.ui.genBtn.clicked.connect(self.generateFiles)
        self.ui.typeCombo.addItems(["Category", "Subcategory"])
        self.ui.typeCombo.currentIndexChanged.connect(self.updateCatCombo)
        self.ui.startColorBtn.clicked.connect(self.chooseStartColor)
        self.ui.endColorBtn.clicked.connect(self.chooseEndColor)
        self.ui.startColorEdit.editingFinished.connect(self.updateStartColor)
        self.ui.endColorEdit.editingFinished.connect(self.updateEndColor)
        self.ui.editSaveBtn.clicked.connect(self.saveEditPanel)
        self.ui.editCancelBtn.clicked.connect(self.hideEditPanel)
        self.ui.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.editPanelIndex = None
        self.buildMenu()
        self.refreshTree()
        self.updateCatCombo()
        self.ui.editPanel.hide()
        self.ui.startColorEdit.setText(bck.startColor)
        self.ui.endColorEdit.setText(bck.endColor)
        self.ui.startColorLabel.setStyleSheet(f"background:{bck.startColor}; border:1px solid gray;")
        self.ui.endColorLabel.setStyleSheet(f"background:{bck.endColor}; border:1px solid gray;")
    def buildMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction("New", self.fileNew)
        fileMenu.addAction("Open", self.fileOpen)
        fileMenu.addAction("Save", self.fileSave)
        fileMenu.addSeparator()
        fileMenu.addAction("Exit", self.close)
    def refreshTree(self):
        self.model.removeRows(0, self.model.rowCount())
        cats = list(bck.categories.keys())
        n = len(cats)
        for idx, cat in enumerate(cats):
            start = bck.categories[cat].get("startColor")
            end = bck.categories[cat].get("endColor")
            if not (isinstance(start, str) and start.startswith('#') and len(start) == 7):
                start = bck.startColor if (isinstance(bck.startColor, str) and bck.startColor.startswith('#') and len(bck.startColor) == 7) else '#000000'
            if not (isinstance(end, str) and end.startswith('#') and len(end) == 7):
                end = bck.endColor if (isinstance(bck.endColor, str) and bck.endColor.startswith('#') and len(bck.endColor) == 7) else '#ffffff'
            r1, g1, b1 = int(start[1:3],16), int(start[3:5],16), int(start[5:7],16)
            r2, g2, b2 = int(end[1:3],16), int(end[3:5],16), int(end[5:7],16)
            t = idx/(max(n-1,1))
            r = int(r1 + (r2-r1)*t)
            g = int(g1 + (g2-g1)*t)
            b = int(b1 + (b2-b1)*t)
            color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            item = QStandardItem(cat)
            item.setData(color, Qt.UserRole)
            self.model.appendRow(item)
            for sub in bck.categories[cat]["sub"]:
                subitem = QStandardItem(sub)
                subitem.setData(color, Qt.UserRole)
                item.appendRow(subitem)
    def updateCatCombo(self):
        self.ui.catCombo.clear()
        self.ui.catCombo.addItems(list(bck.categories.keys()))
    def addSeparator(self):
        name = self.ui.nameEdit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty.")
            return
        if self.ui.typeCombo.currentText() == "Category":
            bck.sepAdd("cat", name)
        else:
            parent = self.ui.catCombo.currentText()
            bck.sepAdd("sub", name, parent)
        self.refreshTree()
        self.updateCatCombo()
        self.ui.nameEdit.clear()
    def removeSeparator(self):
        index = self.ui.treeView.currentIndex()
        if not index.isValid():
            return
        item = self.model.itemFromIndex(index)
        if item.parent():
            cat = item.parent().text()
            bck.sepRemove("sub", item.text(), False, cat)
        else:
            bck.sepRemove("cat", item.text(), False, None)
        self.refreshTree()
        self.updateCatCombo()
    def moveSeparator(self, direction):
        index = self.ui.treeView.currentIndex()
        if not index.isValid():
            return
        item = self.model.itemFromIndex(index)
        parent = item.parent()
        if parent:
            siblings = [parent.child(i) for i in range(parent.rowCount())]
        else:
            siblings = [self.model.item(i) for i in range(self.model.rowCount())]
        row = item.row()
        new_row = row + direction
        if 0 <= new_row < len(siblings):
            siblings[row], siblings[new_row] = siblings[new_row], siblings[row]
            if parent:
                cat = parent.text()
                reordered = [siblings[i].text() for i in range(len(siblings))]
                bck.categories[cat]["sub"] = {k: bck.categories[cat]["sub"][k] for k in reordered}
            else:
                reordered = [siblings[i].text() for i in range(len(siblings))]
                bck.categories = {k: bck.categories[k] for k in reordered}
            self.refreshTree()
            self.ui.treeView.setCurrentIndex(siblings[new_row].index())
    def generateFiles(self):
        bck.outputGen()
    def showEditPanel(self, index):
        item = self.model.itemFromIndex(index)
        self.editPanelIndex = index
        self.ui.editNameEdit.setText(item.text())
        self.ui.editPanel.show()
        self.ui.editNameEdit.setFocus()
    def hideEditPanel(self):
        self.ui.editPanel.hide()
        self.editPanelIndex = None
    def saveEditPanel(self):
        if self.editPanelIndex is None:
            return
        item = self.model.itemFromIndex(self.editPanelIndex)
        new_name = self.ui.editNameEdit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Input Error", "Name cannot be empty.")
            return
        if item.parent():
            cat = item.parent().text()
            old = item.text()
            bck.categories[cat]["sub"][new_name] = bck.categories[cat]["sub"].pop(old)
        else:
            old = item.text()
            bck.categories[new_name] = bck.categories.pop(old)
        self.refreshTree()
        self.hideEditPanel()
    def chooseStartColor(self):
        color = QColorDialog.getColor(QColor(self.ui.startColorEdit.text()), self, "Choose Start Color")
        if color.isValid():
            self.ui.startColorEdit.setText(color.name())
            self.updateStartColor()
    def chooseEndColor(self):
        color = QColorDialog.getColor(QColor(self.ui.endColorEdit.text()), self, "Choose End Color")
        if color.isValid():
            self.ui.endColorEdit.setText(color.name())
            self.updateEndColor()
    def updateStartColor(self):
        color = self.ui.startColorEdit.text().strip()
        if not (isinstance(color, str) and color.startswith('#') and len(color) == 7):
            color = '#000000'
        bck.startColor = color
        self.ui.startColorLabel.setStyleSheet(f"background:{color}; border:1px solid gray;")
        self.refreshTree()
    def updateEndColor(self):
        color = self.ui.endColorEdit.text().strip()
        if not (isinstance(color, str) and color.startswith('#') and len(color) == 7):
            color = '#ffffff'
        bck.endColor = color
        self.ui.endColorLabel.setStyleSheet(f"background:{color}; border:1px solid gray;")
        self.refreshTree()
    def showContextMenu(self, pos):
        index = self.ui.treeView.indexAt(pos)
        if not index.isValid():
            return
        item = self.model.itemFromIndex(index)
        menu = self.ui.treeView.createStandardContextMenu()
        editAct = QAction("Edit", self)
        editAct.triggered.connect(lambda: self.showEditPanel(index))
        menu.addAction(editAct)
        menu.exec(self.ui.treeView.viewport().mapToGlobal(pos))
    def fileNew(self):
        bck.fileNew()
        self.refreshTree()
    def fileOpen(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", bck.initDir, "JSON Files (*.json)")
        if path:
            bck.fileOpen(path)
            self.refreshTree()
    def fileSave(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", bck.initDir, "JSON Files (*.json)")
        if path:
            bck.fileSave(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
