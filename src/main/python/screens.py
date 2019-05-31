import sys
import PyQt5 as p

class DeckInfoButton(p.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DeckInfoButton, self).__init__(parent)
        self.button = p.QtWidgets.QPushButton("Open deck")
        self.button.clicked.connect(self.goToDeckInfo)
        lay = p.QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=p.QtCore.Qt.AlignRight)
        lay.setContentsMargins(2, 2, 2, 2)

    def goToDeckInfo(self):
        self.deck_info = DeckInfoScreen()
        self.deck_info.show()

class StartScreen(p.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StartScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()

        self.setWindowTitle("Welcome to Auswendiglernen!")

        title = p.QtWidgets.QLabel("Decks:")
        title.setFont(p.QtGui.QFont("Times", 50))

        top_layout = p.QtWidgets.QHBoxLayout()
        top_layout.addWidget(title)

        self.list = p.QtWidgets.QListView(self)
        top_layout.addWidget(self.list)
        self.model = p.QtGui.QStandardItemModel(self.list)

        # dummy data
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
            item.setFont(p.QtGui.QFont("Times", 25))

            self.model.appendRow(item)

            self.list.setIndexWidget(item.index(), DeckInfoButton())

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)

        self.setLayout(main_layout)

        self.showMaximized()

class DeckInfoScreen(p.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DeckInfoScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()
        
        self.setWindowTitle("Deck Info")

        layoutV = p.QtWidgets.QVBoxLayout()
        self.pushButton = p.QtWidgets.QPushButton(self)
        self.pushButton.setText('Back to Start!')
        self.pushButton.clicked.connect(self.goToStart)
        layoutV.addWidget(self.pushButton)

        self.showMaximized()

    def goToStart(self):
        self.start = StartScreen()
        self.start.show()