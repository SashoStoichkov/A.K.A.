import sys

import PyQt5 as p
from fbs_runtime.application_context import ApplicationContext

class StartScreen(p.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StartScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()

        title = p.QtWidgets.QLabel("Decks:")
        title.setFont(p.QtGui.QFont("Times", 50))

        list_of_decks = p.QtWidgets.QListView()
        list_of_decks.setMinimumSize(600, 400)

        list_model = p.QtGui.QStandardItemModel(list_of_decks)

        foods = [
            'Cookie dough', # Must be store-bought
            'Hummus', # Must be homemade
            'Spaghetti', # Must be saucy
            'Dal makhani', # Must be spicy
            'Chocolate whipped cream' # Must be plentiful
        ]

        for food in foods:
            item = p.QtGui.QStandardItem(food)
        
            # Add the item to the model
            list_model.appendRow(item)

        list_of_decks.setModel(list_model)

        top_layout = p.QtWidgets.QHBoxLayout()
        top_layout.addWidget(title)

        mid_layout = p.QtWidgets.QHBoxLayout()
        mid_layout.addWidget(list_of_decks)

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)
        main_layout.addLayout(mid_layout, 0, 1, 0, 2)

        self.setLayout(main_layout)

        self.showMaximized()

if __name__ == "__main__":
    app = ApplicationContext()
    s = StartScreen()
    s.show()
    sys.exit(app.app.exec_())