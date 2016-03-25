__author__ = 's1039137'


class Deck(object):
    def __init__(self, name, supplement, deck, active=None, active_size=5):
        self.name = name
        self.supplement = supplement
        self.deck = deck
        if active is None:
            self.active = []
        self.active_size = active_size

    def generate_central_line(self):
        for i in range(0, self.active_size):
            card = self.deck.pop()
            self.active.append(card)

    def print_cards(self):
        print "Available Cards"
        for card in self.active:
            print card
        print "Supplement"
        if len(self.supplement) > 0:
            print self.supplement[0]
