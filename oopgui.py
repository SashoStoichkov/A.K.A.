import utils

from appJar import gui
from const import DB_NAME
# from session import Session
from collection import Loader

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
        card.flush()
        
        if card.due == utils.today():
            self.cards.add(card)

        if self.cards:
            self.current_card = self.cards.pop()
        else:
            self.current_card = None

class App:
    def __init__(self):
        self.app = gui('Memorize')
        self.col = Loader(DB_NAME).load()
        self.questions = [f'question {i}' * 5 for i in range(10)]
        self.session = None
        self.current_deck_name = None
        
        self.create_main_menu_window()
        self.create_rename_deck_window()
        self.create_add_deck_window()
        self.create_cards_window()
        self.create_add_card_window()
        self.create_study_deck_window()

    
    ################################################################################
    # main window, showing the decks
    
    def create_main_menu_window(self):
        self.app.setTitle('decks')        
        self.app.addListBox('decks-list-box', self.col.dotted_names_list)

        self.app.startFrame('deck-buttons', row=1, column=0)
        self.app.addButton('cards', self.show_cards, row=0, column=0)
        self.app.addButton('study', self.study_deck, row=0, column=1)
        self.app.addButton('add-deck', self.add_deck, row=0, column=2)
        self.app.setButton('add-deck', 'add')
        self.app.addButton('remove-deck', self.remove_deck, row=0, column=3)
        self.app.setButton('remove-deck', 'remove')
        self.app.addButton('rename-deck', self.rename_deck, row=0, column=4)
        self.app.setButton('rename-deck', 'rename')
        self.app.stopFrame()

    def study_deck(self, button):
        print('study deck')
        deckname = self.app.getListBox('decks-list-box')[0]
        deck = self.col.find_deck(deckname)
        self.session = Session(deck)
        self.session.start()
        self.first_screen()

    def first_screen(self):
        print('first screen')
        card = self.session.current_card
        self.app.emptySubWindow('study-deck-window')
        
        if card is None:
            # the deck has no more due cards for today
            self.app.openSubWindow('study-deck-window')
            self.app.addLabel('no-more-cards', 'No more cards for today',
                              row=0, column=0)
            self.app.stopSubWindow()  
        else:
            self.app.openSubWindow('study-deck-window')
            self.app.addMessage('front-before-show', card.front,
                                row=0, column=0)
            self.app.addButton('show-button', self.show_back,
                               row=1, column=0)
            self.app.setButton('show-button', 'show')
            self.app.stopSubWindow()
            
        self.app.showSubWindow('study-deck-window')

    def show_back(self):
        card = self.session.current_card

        # draw the window
        self.app.emptySubWindow('study-deck-window')
        self.app.openSubWindow('study-deck-window')
        self.app.addMessage('front-after-show', card.front)
        self.app.addMessage('back-after-show', card.back)
        self.app.addFrame('deck-show-buttons')

        for k in range(5):
            self.app.addButton(f'button-{k}', self.take_answer,
                               row=0, column=k)
            self.app.setButton(f'button-{k}', f'{k}')
            
        self.app.stopFrame()
        self.app.stopSubWindow()
        
    def take_answer(self, button):
        answer = int(button.split('-')[1])
        self.session.update(answer)
        self.first_screen()
    
    def create_study_deck_window(self):
        self.app.startSubWindow('study-deck-window')
        self.app.stopSubWindow()
        
    def decks_updated(self):
        # called when decks are added or removed or renamed
        self.app.updateListBox('decks-list-box', self.col.dotted_names_list)

    def show_cards(self, button):
        self.current_deck_name = self.app.getListBox('decks-list-box')[0]
        self.refresh_cards_list()
        self.app.showSubWindow("cards-window")

    def add_deck(self, button):
        self.app.showSubWindow('add-deck-window')
        self.app.setFocus('add-deck-name-entry')
    
    def remove_deck(self, button):
        deck_name = self.app.getListBox('decks-list-box')[0]
        self.col.remove_deck(deck_name)
        self.decks_updated()

    def rename_deck(self, button):
        dotted_name = self.app.getListBox('decks-list-box')[0]
        name = dotted_name.split('::')[-1]
        self.app.setEntry('rename-deck-entry', name)
        self.app.showSubWindow('rename-deck-window')
        self.app.setFocus('rename-deck-entry')

    ################################################################################
    # add deck window
    
    def add_deck_save(self, button):
        deck_name = self.app.getEntry('add-deck-name-entry')
        self.col.create_decks(deck_name)
        self.decks_updated()
        self.app.hideSubWindow('add-deck-window')
    
    def create_add_deck_window(self):
        self.app.startSubWindow('add-deck-window')
        self.app.setTitle('add deck')
        self.app.setSize('300x80')
        self.app.addEntry('add-deck-name-entry')
        self.app.addButton('add-deck-save-button', self.add_deck_save)
        self.app.setButton('add-deck-save-button', 'save')
        self.app.stopSubWindow()

    ################################################################################
    # cards window

    def get_current_card(self):
        front = self.app.getListBox("cards-questions-list")[0]
        deck = self.col.find_deck(self.current_deck_name)
        for i, card in enumerate(deck.cards.values()):
            if card.front == front:
                return card
        raise ValueError('this should not happen')
    
    def delete_card(self, button):
        self.col.remove_card(self.get_current_card())
        self.refresh_cards_list()

    def add_card(self, button):
        self.app.showSubWindow("add-card-window")

    def edit_card(self, button):
        # get the card and show the window
        card = self.get_current_card()
        raise NotImplementedError        
    
    def create_cards_window(self):
        self.app.startSubWindow("cards-window", modal=True)
        self.app.setTitle("cards")

        self.app.startFrame("cards-questions-frame", row=0, column=0)
        self.app.addListBox("cards-questions-list", self.questions)
        self.app.stopFrame()

        self.app.startFrame("cards-buttons", row=0, column=1)

        self.app.addButton("cards-edit-button", self.edit_card)
        self.app.setButton("cards-edit-button", "edit")

        self.app.addButton("cards-delete-button", self.delete_card)
        self.app.setButton("cards-delete-button", "delete")

        self.app.addButton("cards-add-button", self.add_card)
        self.app.setButton("cards-add-button", "add")

        self.app.stopFrame() # card-buttons
        self.app.stopSubWindow() # cards-window

    ################################################################################
    # rename deck window

    def rename_deck_save(self, button):
        dotted_name = self.app.getListBox('decks-list-box')[0]
        current_deck = self.col.find_deck(dotted_name)
        new_name = self.app.getEntry('rename-deck-entry')
        current_deck.name = new_name
        current_deck.flush() # TODO: this should not leak
        self.decks_updated()
        self.app.hideSubWindow('rename-deck-window')    
    
    def create_rename_deck_window(self):
        self.app.startSubWindow('rename-deck-window')
        self.app.setTitle('rename deck')
        self.app.addEntry('rename-deck-entry')
        self.app.addButton('rename-deck-save', self.rename_deck_save)
        self.app.setButton('rename-deck-save', 'save')
        self.app.stopSubWindow()

    ################################################################################
    # add card window

    def add_card_save(self, button):
        new_front = self.app.getTextArea("add-card-front-text")
        new_back = self.app.getTextArea("add-card-back-text")
        self.col.create_card(new_front, new_back, self.current_deck_name)        
        self.refresh_cards_list()
        self.app.clearTextArea('add-card-front-text')
        self.app.clearTextArea('add-card-back-text')

    def refresh_cards_list(self):
        deck = self.col.find_deck(self.current_deck_name)
        cards_list = [card.front for card in deck.cards.values()]
        self.app.updateListBox('cards-questions-list', cards_list)        
        
    def create_add_card_window(self):
        self.app.startSubWindow("add-card-window", modal=True)
        self.app.addTextArea("add-card-front-text", text=None)
        self.app.addTextArea("add-card-back-text", text=None)
        self.app.addButton("add-card-save-button", self.add_card_save)
        self.app.setButton("add-card-save-button", "save")
        self.app.stopSubWindow()

    def go(self):
        self.app.go()

app = App()
app.go()
