import collection
import const

class LearningSession:
    def __init__(self, deckname, collection):
        self.col = collection

    def start(self):
        pass


if __name__ == "__main__":
    collection = collection.Loader(const.DB_NAME)
    