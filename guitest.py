import random

from appJar import gui
import collection
from const import DB_NAME

class Session:
    """
    * attributes
    - self.deck
    - self.current_card
    - self.cards    
    """

    def __init__(self, deck):
        self.deck = deck
        self.cards = set(deck.due_cards)
        self.current_card = None

    def start(self):
        if self.cards:
            self.current_card = self.cards.pop()

    def update(self, answer):
        card = self.current_card
        card.reschedule(answer)
        
        if card.due == utils.today():
            self.cards.add(card)

        if self.cards:
            self.current_card = self.cards.pop()
        else:
            self.current_card = None

app = gui()
col = collection.Loader(DB_NAME).load()
questions = [f'question {i}' for i in range(10)]
session = None

################################################################################
# main window, showing the decks

def decks_updated():
    # called when decks are added or removed or renamed
    app.updateListBox('decks-list-box', col.dotted_names_list)
    
def study_deck(button):
    # create the session
    # check if there are cards to study in the deck    
    # open the window in state 1

    
    deckname = app.getListBox('decks-list-box')
    deck = col.find_deck(deckname)    
    session = Session(deck)
    session.start()
    first_screen()
    
    
def first_screen():
    if session.current_card is None:
        # show empty window

def answer_button(button):
    answer = # extract the answer from the string button
    newcard = session.update(answer)
    first_screen(newcard)
    
def add_deck(button):
    app.showSubWindow('add-deck-window')
    app.setFocus('add-deck-name-entry')

def remove_deck(button):
    deck_name = app.getListBox('decks-list-box')[0]
    col.remove_deck(deck_name)
    decks_updated()

def rename_deck(button):
    dotted_name = app.getListBox('decks-list-box')[0]
    name = dotted_name.split('::')[-1]
    app.setEntry('rename-deck-entry', name)
    app.showSubWindow('rename-deck-window')
    app.setFocus('rename-deck-entry')

def show_cards(button):
    app.showSubWindow("cards-window")

def study_deck(button):
    pass
    
app.setTitle('decks')
    
# drop down menu
app.addListBox('decks-list-box', col.dotted_names_list)

app.startFrame('deck-buttons', row=1, column=0)
app.addButton('cards', show_cards, row=0, column=0)
app.addButton('study', study_deck, row=0, column=1)
app.addButton('add-deck', add_deck, row=0, column=2)
app.setButton('add-deck', 'add')
app.addButton('remove-deck', remove_deck, row=0, column=3)
app.setButton('remove-deck', 'remove')
app.addButton('rename-deck', rename_deck, row=0, column=4)
app.setButton('rename-deck', 'rename')
app.stopFrame()

################################################################################
# add deck window

def add_deck_save(button):
    deck_name = app.getEntry('add-deck-name-entry')
    col.create_decks(deck_name)
    decks_updated()
    app.hideSubWindow('add-deck-window')

app.startSubWindow('add-deck-window')
app.setTitle('add deck')
app.setSize('300x80')
app.addEntry('add-deck-name-entry')
app.addButton('add-deck-save-button', add_deck_save)
app.setButton('add-deck-save-button', 'save')
app.stopSubWindow()

################################################################################
# cards window

def delete_card(button):
    chosen = app.getListBox("cards-questions-list")
    app.removeListItem("cards-questions-list", chosen)

def add_card(button):
    app.showSubWindow("add-card-window")

def edit_card(button):
    pass

app.startSubWindow("cards-window", modal=True)
app.setTitle("cards")

app.startFrame("cards-questions-frame", row=0, column=0)
app.addListBox("cards-questions-list", questions)
app.stopFrame()

app.startFrame("cards-buttons", row=0, column=1)

app.addButton("cards-edit-button", edit_card)
app.setButton("cards-edit-button", "edit")

app.addButton("cards-delete-button", delete_card)
app.setButton("cards-delete-button", "delete")

app.addButton("cards-add-button", add_card)
app.setButton("cards-add-button", "add")

app.stopFrame() # card-buttons
app.stopSubWindow() # cards-window

################################################################################
# rename deck window

def rename_deck_save(button):
    dotted_name = app.getListBox('decks-list-box')[0]
    current_deck = col.find_deck(dotted_name)
    new_name = app.getEntry('rename-deck-entry')
    current_deck.name = new_name
    current_deck.flush() # TODO: this should not leak
    decks_updated()
    app.hideSubWindow('rename-deck-window')    

app.startSubWindow('rename-deck-window')
app.setTitle('rename deck')
app.addEntry('rename-deck-entry')
app.addButton('rename-deck-save', rename_deck_save)
app.setButton('rename-deck-save', 'save')
app.stopSubWindow()

################################################################################
# add card window

def add_card_save(button):
    newQ = app.getTextArea("add-card-front-text")
    questions.append(newQ)
    app.updateListBox("cards-questions-list", questions)

app.startSubWindow("add-card-window", modal=True)
app.addTextArea("add-card-front-text", text=None)
app.addTextArea("add-card-back-text", text=None)
app.addButton("add-card-save-button", add_card_save)
app.setButton("add-card-save-button", "save")
app.stopSubWindow()

app.go()

################################################################################
# study window

def show_answer(button):
    pass

