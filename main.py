__author__ = 's1039137'

import itertools
from card import *
from player import *
from deck import *


class Game(object):
    def __init__(self):
        self.player_decks = [8 * [Card('Serf', (0, 1), 0)],     # Human player's deck
                             2 * [Card('Squire', (1, 0), 0)]]
        self.pod = list(itertools.chain.from_iterable(self.player_decks))  # Put the starting cards into the deck.
        self.human = Player('human', self.pod)
        self.computer = Player('computer', self.pod)
        self.main_deck = [4 * [Card('Archer', (3, 0), 2)], 4 * [Card('Baker', (0, 3), 2)],
                          3 * [Card('Swordsman', (4, 0), 3)], 2 * [Card('Knight', (6, 0), 5)],
                          3 * [Card('Tailor', (0, 4), 3)], 3 * [Card('Crossbowman', (4, 0), 3)],
                          3 * [Card('Merchant', (0, 5), 4)], 4 * [Card('Thug', (2, 0), 1)],
                          4 * [Card('Thief', (1, 1), 1)], 2 * [Card('Catapult', (7, 0), 6)],
                          2 * [Card('Caravan', (1, 5), 5)], 2 * [Card('Assassin', (5, 0), 4)]]
        self.deck = list(itertools.chain.from_iterable(self.main_deck))  # Shuffle the main deck.
        random.shuffle(self.deck)
        self.supplement = 10 * [Card('Levy', (1, 2), 2)]
        self.central = Deck('central', self.supplement, self.deck)
        self.central.generate_central_line()
        self.current_player = self.human
        opponent_type = raw_input("Do you want an aggressive opponent? Type A if yes, anything else if no.")
        self.computer.aggressive = (opponent_type == 'A')
        self.game_ongoing = True
        self.human.draw_hand()
        self.computer.draw_hand()

    def reset_game(self):
        self.player_decks = [8 * [Card('Serf', (0, 1), 0)],  # Human player's deck
                             2 * [Card('Squire', (1, 0), 0)]]
        self.pod = list(itertools.chain.from_iterable(self.player_decks))  # Put the starting cards into the deck.
        self.human = Player('human', self.pod)
        self.computer = Player('computer', self.pod)
        self.main_deck = [4 * [Card('Archer', (3, 0), 2)], 4 * [Card('Baker', (0, 3), 2)],
                          3 * [Card('Swordsman', (4, 0), 3)], 2 * [Card('Knight', (6, 0), 5)],
                          3 * [Card('Tailor', (0, 4), 3)], 3 * [Card('Crossbowman', (4, 0), 3)],
                          3 * [Card('Merchant', (0, 5), 4)], 4 * [Card('Thug', (2, 0), 1)],
                          4 * [Card('Thief', (1, 1), 1)], 2 * [Card('Catapult', (7, 0), 6)],
                          2 * [Card('Caravan', (1, 5), 5)], 2 * [Card('Assassin', (5, 0), 4)]]
        self.deck = list(itertools.chain.from_iterable(self.main_deck))  # Shuffle the main deck.
        random.shuffle(self.deck)
        self.supplement = 10 * [Card('Levy', (1, 2), 2)]
        self.central = Deck('central', self.supplement, self.deck)
        self.central.generate_central_line()
        self.current_player = self.human
        opponent_type = raw_input("Do you want an aggressive (A) opponent? Type A if yes, anything else if no.")
        self.computer.aggressive = (opponent_type == 'A')
        self.game_ongoing = True
        self.human.draw_hand()
        self.computer.draw_hand()
        self.game_engine()

    def play_again(self):
        play_game = raw_input("\nDo you want to play another game? Type 'Y' if yes, anything else if no:")
        if play_game == 'Y':
            self.reset_game()
        else:
            exit()

    def start_turn(self, player):
        while self.current_player == player:
            print "%s's turn:" % player.name
            self.print_vitals()
            self.central.print_cards()
            if player.name == "human":
                player.print_values()
                self.human.print_hand()
                self.present_actions()
            else:
                self.computer.play_all()
                self.computer.attack_opponent(self.human)
                self.print_vitals()
                self.computer_buying_phase(self.computer.aggressive)
                self.end_turn(self.computer)
                print "Computer turn ending"

    def game_engine(self):
        while self.game_ongoing:
            self.check_winner()
            self.start_turn(self.current_player)

    def check_main_deck(self):
        if self.central.active_size == 0:
            print "No more cards available"
            if self.human.health > self.computer.health:
                print "Human wins on health"
            elif self.human.health < self.computer.health:
                print "Computer Wins on health"
            elif self.human.eval_card_strength() > self.computer.eval_card_strength():
                print "Human Wins on Card Strength"
            elif self.human.eval_card_strength() < self.computer.eval_card_strength():
                print "Computer wins on card strength"
            else:
                print "Draw"
            self.game_ongoing = False
            self.play_again()

    def check_winner(self):
        if self.human.health <= 0:
            print "Computer wins"
            self.game_ongoing = False
            self.play_again()
        elif self.computer.health <= 0:
            print 'Player Wins'
            self.game_ongoing = False
            self.play_again()
        else:
            self.check_main_deck()

    def print_game_info(self, player):
        self.print_vitals()
        self.human.print_hand()
        player.print_values()

    def print_vitals(self):
        print "\nPlayer Health %s" % self.human.health
        print "Computer Health %s" % self.computer.health

    def present_actions(self):
        print "\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"
        act = raw_input("Enter Action: ")
        print act
        if act == 'P':
            if len(self.human.hand) > 0:
                self.human.play_all()
                self.human.print_hand()
                self.print_active_cards()
                self.human.print_values()
            else:
                print "\nNo cards in the hand!"
                self.present_actions()
        elif act.isdigit():
            if len(self.human.hand) > int(act):
                self.human.play_card(int(act))
                self.human.print_hand()
                self.print_active_cards()
                self.human.print_values()
            else:
                print "\nNo card with index %s in the hand!" % act
                self.present_actions()
        elif act == 'B':
            if self.human.money > 0:
                self.present_shop_actions()
            else:
                print "\nNo money to buy anything!"
                self.present_actions()

        elif act == 'A':
            if self.human.attack > 0:
                self.human.attack_opponent(self.computer)
            else:
                print "\nCannot attack with 0 attack!"
                self.present_actions()
        elif act == 'E':
            self.end_turn(self.human)

    def end_turn(self, player):
        player.discard_hand()
        player.discard_active()
        player.draw_hand()
        player.attack = 0
        player.money = 0
        self.current_player = self.get_opponent(player)

    def get_opponent(self, player):
        if player.name == 'human':
            return self.computer
        else:
            return self.human

    def print_active_cards(self):
        print "\nYour Active Cards"
        for card in self.human.active:
            print card

    def print_shop(self):
        print "Available Cards"
        index = 0
        for card in self.central.active:
            print "[%s] %s" % (index, card)
            index += 1
        if len(self.central.supplement) > 0:
            print "[%s] %s" % ("S", self.central.supplement[0])
        print "You have %s Money. " % self.human.money
        print "Choose a card to buy [0-n], S for supplement, E to end buying"

    def present_shop_actions(self):
        self.print_shop()
        while self.human.money > 0:
            action = raw_input("Choose option: ")
            if action == 'S':
                self.buy_supplement(self.human)
            elif action == 'E':
                break
            elif action.isdigit():
                index = int(action)
                self.buy_card(self.human, index)
                self.print_shop()
            else:
                print "Enter a valid option"

    def buy_supplement(self, player):
        if len(self.central.supplement) > 0:
            if player.money >= self.central.supplement[0].cost:
                player.money -= self.central.supplement[0].cost
                player.discard.append(self.central.supplement.pop())
                print "Supplement Bought by %s" % player.name
                self.print_shop()
            else:
                print "insufficient money to buy"
        else:
            print "no supplements left"

    def add_to_shop(self):
        if len(self.central.deck) > 0:
            card = self.central.deck.pop()
            self.central.active.append(card)
        else:
            self.central.active_size -= 1
            if self.central.active_size == 0:
                self.check_winner()

    def buy_card(self, player, index):
        if index < len(self.central.active):
            if player.money >= self.central.active[index].cost:
                player.money -= self.central.active[index].cost
                card = self.central.active.pop(index)
                player.discard.append(card)
                self.add_to_shop()
                print "Card %s bought by player %s" % (card.name, player.name)
            else:
                print "%s has insufficient money to buy any card" % player.name
        else:
            print "enter a valid index number"

    def buy_aggressive(self):
        prev_attack = 0
        prev_money = 0
        can_afford = True
        while can_afford:
            secondary_index = -1
            choice_index = -1
            for i in range(0, 5):
                if self.computer.money >= self.central.active[i].cost:
                    curr_attack = self.central.active[i].get_attack()
                    curr_money = self.central.active[i].get_money()
                    if curr_attack > prev_attack:
                        choice_index = i
                        prev_attack = curr_attack
                    elif curr_money > prev_money:
                        secondary_index = i
                        prev_money = curr_money
            if choice_index > -1:
                self.buy_card(self.computer, choice_index)
                can_afford = True
            elif secondary_index > -1:
                self.buy_card(self.computer, secondary_index)
                can_afford = True
            else:
                can_afford = False
        while self.computer.money >= self.supplement[0].cost & len(self.supplement) > 0:
            self.buy_supplement(self.computer)

    def buy_acquisitive(self):
        prev_money = 0
        prev_attack = 0
        can_afford = True
        while can_afford:
            secondary_index = -1
            choice_index = -1
            for i in range(0, 5):
                if self.computer.money >= self.central.active[i].cost:
                    curr_attack = self.central.active[i].get_attack()
                    curr_money = self.central.active[i].get_money()
                    if curr_money > prev_money:
                        choice_index = i
                        prev_money = curr_money
                    elif curr_attack > prev_attack:
                        secondary_index = i
                        prev_attack = curr_attack
            if choice_index > -1:
                self.buy_card(self.computer, choice_index)
                can_afford = True
            elif secondary_index > -1:
                self.buy_card(self.computer, secondary_index)
                can_afford = True
            else:
                can_afford = False
        while self.computer.money >= self.supplement[0].cost & len(self.supplement) > 0:
            self.buy_supplement(self.computer)

    def computer_buying_phase(self, aggressive):
        print "Computer buying"
        if self.computer.money > 0:
            if aggressive:
                self.buy_aggressive()
            else:
                self.buy_acquisitive()
        self.end_turn(self.computer)


def main():
    game = Game()
    game.game_engine()

if __name__ == '__main__':
    main()
