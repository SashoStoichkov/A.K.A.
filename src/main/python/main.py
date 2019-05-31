import sys

import PyQt5 as p
from fbs_runtime.application_context import ApplicationContext

class CustomWidget(p.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.button = p.QtWidgets.QPushButton("Open deck")
        lay = p.QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=p.QtCore.Qt.AlignRight)
        lay.setContentsMargins(2, 2, 2, 2)

class StartScreen(p.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StartScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()

        title = p.QtWidgets.QLabel("Decks:")
        title.setFont(p.QtGui.QFont("Times", 50))

        top_layout = p.QtWidgets.QHBoxLayout()
        top_layout.addWidget(title)

        self.list = p.QtWidgets.QListView(self)
        top_layout.addWidget(self.list)
        self.model = p.QtGui.QStandardItemModel(self.list)

        foods = [
            'Cookie dough', # Must be store-bought
            'Hummus', # Must be homemade
            'Spaghetti', # Must be saucy
            'Dal makhani', # Must be spicy
            'Chocolate whipped cream' # Must be plentiful
        ]

        self.list.setModel(self.model)
        self.list.setMinimumSize(600, 400)

        for food in foods:
            item = p.QtGui.QStandardItem(food)

            self.model.appendRow(item)

            self.list.setIndexWidget(item.index(), CustomWidget())

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)

        self.setLayout(main_layout)

        self.showMaximized()

if __name__ == "__main__":
    app = ApplicationContext()
    s = StartScreen()
    s.show()
    sys.exit(app.app.exec_())