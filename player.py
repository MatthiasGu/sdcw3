__author__ = 's1039137'

import random


class Player(object):
    def __init__(self, name, deck, hand=None, hand_size=5, health=30, money=0, attack=0, active=None, discard=None,
                 aggressive=False):
        self.name = name
        self.health = health
        self.hand_size = hand_size
        self.deck = deck
        self.money = money
        self.attack = attack
        if hand is None:
            self.hand = []
        if active is None:
            self.active = []
        if discard is None:
            self.discard = []
        self.aggressive = aggressive

    def draw_hand(self):
        for x in range(0, self.hand_size):  # Draw a new hand
            if len(self.deck) == 0:     # If the deck is empty, shuffle the discard pile and make it the new deck.
                random.shuffle(self.discard)
                self.deck = self.discard
                self.discard = []
            else:
                random.shuffle(self.deck)
            card = self.deck.pop()
            self.hand.append(card)

    def discard_hand(self):
        if len(self.hand) > 0:
            for x in range(0, len(self.hand)):
                self.discard.append(self.hand.pop())

    def discard_active(self):
        if len(self.active) > 0:
            for x in range(0, len(self.active)):
                self.discard.append(self.active.pop())

    def get_health(self):
        return self.health

    def get_hand(self):
        return self.hand

    def print_hand(self):
        print "\nYour Hand"
        index = 0
        for card in self.hand:
            print "[%s] %s" % (index, card)
            index += 1

    def print_values(self):
        print "\n%s Values" % self.name
        print "Money %s, Attack %s" % (self.money, self.attack)

    def add_values(self, card):
        self.money += card.get_money()
        self.attack += card.get_attack()

    def play_card(self, card_no):
        if card_no < len(self.hand):
            card = self.hand.pop(card_no)
            self.active.append(card)
            self.add_values(card)

    def play_all(self):
        if len(self.hand) > 0:
            for x in range(0, len(self.hand)):
                card = self.hand.pop()
                self.active.append(card)
                self.add_values(card)
        if self.name == "computer":
            print "Computer has %s attack and %s money" % (self.attack, self.money)

    def attack_opponent(self, opponent):
        opponent.health -= self.attack
        if self.name == "computer":
            print " Computer attacking with strength %s" % self.attack
        self.attack = 0

    def eval_card_strength(self):
        strength = 0
        for card in self.deck:
            strength += card.get_attack()
        for card in self.discard:
            strength += card.get_attack()
        for card in self.hand:
            strength += card.get_attack()
        return strength
