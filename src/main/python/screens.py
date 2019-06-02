import sys
import PyQt5 as p

class DeckInfoButton(p.QtWidgets.QWidget):
    def __init__(self, deckname, parent=None):
        self.deckname = deckname
        super(DeckInfoButton, self).__init__(parent)
        self.button = p.QtWidgets.QPushButton("Open deck")
        self.button.clicked.connect(self.goToDeckInfo)
        lay = p.QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=p.QtCore.Qt.AlignRight)
        lay.setContentsMargins(2, 2, 2, 2)

    def goToDeckInfo(self):
        self.deck_info = DeckInfoScreen(self.deckname)
        self.deck_info.show()

class StartScreen(p.QtWidgets.QDialog):
    def __init__(self, coll, parent=None):
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

            self.list.setIndexWidget(item.index(), DeckInfoButton(food))

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)

        self.setLayout(main_layout)

        self.showMaximized()

class DeckInfoScreen(p.QtWidgets.QDialog):
    def __init__(self, deckname, parent=None):
        super(DeckInfoScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()
        
        self.setWindowTitle("{0} Info".format(deckname))

        title = p.QtWidgets.QLabel("{0} Subdecks:".format(deckname))
        title.setFont(p.QtGui.QFont("Times", 50))

        top_layout = p.QtWidgets.QVBoxLayout()
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
            'Chocolate whipped cream', # Must be plentiful
        ]

        self.list.setModel(self.model)
        self.list.setMinimumSize(600, 400)

        for food in foods:
            item = p.QtGui.QStandardItem(food)
            item.setFont(p.QtGui.QFont("Times", 25))

            self.model.appendRow(item)

            self.list.setIndexWidget(item.index(), CardInfoButton(food))

        studyNowButton = p.QtWidgets.QPushButton(self)
        studyNowButton.setText('Study Now!')
        studyNowButton.clicked.connect(self.goToStart)
        studyNowButton.setMinimumSize(100, 50)
        top_layout.addWidget(studyNowButton, alignment=p.QtCore.Qt.AlignCenter)
        top_layout.setContentsMargins(1, 1, 1, 1)

        backToStartButton = p.QtWidgets.QPushButton(self)
        backToStartButton.setText('Back to Start')
        backToStartButton.clicked.connect(self.goToStart)
        backToStartButton.setMinimumSize(100, 50)
        top_layout.addWidget(backToStartButton, alignment=p.QtCore.Qt.AlignCenter)
        top_layout.setContentsMargins(1, 1, 1, 1)

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 0, 0)

        self.setLayout(main_layout)

        self.showMaximized()
    
    def goToStart(self):
        self.start = StartScreen()
        self.start.show()

class CardInfoButton(p.QtWidgets.QWidget):
    def __init__(self, deckname, parent=None):
        self.deckname = deckname
        super(CardInfoButton, self).__init__(parent)
        self.button = p.QtWidgets.QPushButton("See Cards")
        self.button.clicked.connect(self.goToCardsInfo)
        lay = p.QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=p.QtCore.Qt.AlignRight)
        lay.setContentsMargins(2, 2, 2, 2)

    def goToCardsInfo(self):
        self.deck_info = CardsScreen(self.deckname)
        self.deck_info.show()

class CardOptionsButton(p.QtWidgets.QWidget):
    def __init__(self, cardname, cardname_answer, parent=None):
        self.cardname = cardname
        self.cardname_answer = cardname_answer
        super(CardOptionsButton, self).__init__(parent)
        self.button = p.QtWidgets.QPushButton("Options")
        self.button.clicked.connect(self.goToCardsOptions)
        lay = p.QtWidgets.QHBoxLayout(self)
        lay.addWidget(self.button, alignment=p.QtCore.Qt.AlignRight)
        lay.setContentsMargins(2, 2, 2, 2)

    def goToCardsOptions(self):
        self.deck_info = CardsOptionsScreen(self.cardname, self.cardname_answer)
        self.deck_info.show()

class CardsScreen(p.QtWidgets.QDialog):
    def __init__(self, deckname, parent=None):
        super(CardsScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()

        self.setWindowTitle("{0} Cards".format(deckname))

        title = p.QtWidgets.QLabel("{0} Cards:".format(deckname))
        title.setFont(p.QtGui.QFont("Times", 20))

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

            self.list.setIndexWidget(item.index(), CardOptionsButton(food, food))

        addCardButton = p.QtWidgets.QPushButton(self)
        addCardButton.setText('Add Card')
        addCardButton.clicked.connect(self.addCard)
        addCardButton.setMinimumSize(100, 50)
        top_layout.addWidget(addCardButton, alignment=p.QtCore.Qt.AlignCenter)
        top_layout.setContentsMargins(1, 1, 1, 1)

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)

        self.setLayout(main_layout)

        self.showMaximized()

    def goToStart(self):
        self.start = StartScreen()
        self.start.show()

    def addCard(self):
        text, okPressed = p.QtWidgets.QInputDialog.getText(self, "Question", "Add Question:", p.QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)

        text, okPressed = p.QtWidgets.QInputDialog.getText(self, "Answer", "Add Answer:", p.QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)

class CardsOptionsScreen(p.QtWidgets.QDialog):
    def __init__(self, cardname, cardname_answer, parent=None):
        super(CardsOptionsScreen, self).__init__(parent)

        self.originalPalette = p.QtWidgets.QApplication.palette()

        self.cardname = cardname
        self.cardname_answer = cardname + " answer"

        self.setWindowTitle("{0} Options".format(cardname))

        question = p.QtWidgets.QLabel("Question: {0}".format(cardname))
        question.setFont(p.QtGui.QFont("Times", 50))

        answer = p.QtWidgets.QLabel("Answer: {0}".format(cardname_answer))
        answer.setFont(p.QtGui.QFont("Times", 50))

        top_layout = p.QtWidgets.QVBoxLayout()
        top_layout.addWidget(question)
        top_layout.addWidget(answer)

        editCardButton = p.QtWidgets.QPushButton(self)
        editCardButton.setText('Edit Card')
        editCardButton.clicked.connect(self.editCard)
        editCardButton.setMinimumSize(100, 50)
        top_layout.addWidget(editCardButton, alignment=p.QtCore.Qt.AlignCenter)
        top_layout.setContentsMargins(1, 1, 1, 1)

        deleteCardButton = p.QtWidgets.QPushButton(self)
        deleteCardButton.setText('Delete Card')
        deleteCardButton.clicked.connect(self.deleteCard)
        deleteCardButton.setMinimumSize(100, 50)
        top_layout.addWidget(deleteCardButton, alignment=p.QtCore.Qt.AlignCenter)
        top_layout.setContentsMargins(1, 1, 1, 1)

        main_layout = p.QtWidgets.QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 1)

        self.setLayout(main_layout)

        self.showMaximized()

    def goToStart(self):
        self.start = StartScreen()
        self.start.show()

    def editCard(self):
        text, okPressed = p.QtWidgets.QInputDialog.getText(self, "Question", "Edit Question:", p.QtWidgets.QLineEdit.Normal, self.cardname)
        if okPressed and text != '':
            self.cardname = text

            text, okPressed = p.QtWidgets.QInputDialog.getText(self, "Answer", "Edit Answer:", p.QtWidgets.QLineEdit.Normal, self.cardname_answer)
            if okPressed and text != '':
                self.cardname_answer = text
        

    def deleteCard(self):
        self.choice = p.QtWidgets.QMessageBox.question(self, "Delete Card!", "Are you sure you want to delete a Card?", p.QtWidgets.QMessageBox.Yes | p.QtWidgets.QMessageBox.No)

        if self.choice == p.QtWidgets.QMessageBox.Yes:
            print("Deleted!")
        else:
            print("You keep it... for now!")
            
