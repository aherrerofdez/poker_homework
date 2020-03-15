import random
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)  # return self.rank + self.suit (Same result)

    def __lt__(self, other):
        if self.get_rank() in ranks < other.get_rank() in ranks:
            return True
        else:
            return False


class Deck(object):
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        deck = ""
        for i in range(52):
            deck += str(self.cards[i]) + " "
        return deck

    def take_one(self):
        return self.cards.pop(0)


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        for i in range(5):
            self.cards.append(deck.take_one())

    def __str__(self):
        hand = ""
        for i in range(5):
            hand += str(self.cards[i]) + " "
        return hand

    def check_same_suit(self):
        suit = self.cards[0].get_suit()
        for i in range(1, 5):
            if self.cards[i].get_suit() != suit:
                return False
        return True

    def order_ranks(self):
        hand_ranks = []
        ranks_dict = {"J": 11, "Q": 12, "K": 13, "A": 14}
        for i in range(5):
            if self.cards[i].get_rank() not in ranks_dict.keys():
                hand_ranks.append(int(self.cards[i].get_rank()))
            else:
                hand_ranks.append(ranks_dict.get(self.cards[i].get_rank()))
        hand_ranks.sort()
        return hand_ranks

    def is_royal_flush(self):
        if not self.check_same_suit():
            return False
        royal_ranks = ranks[-5:]
        for i in range(5):
            if self.cards[i].get_rank() not in royal_ranks:
                return False
        return True

    def is_straight_flush(self):
        if not self.check_same_suit():
            return False
        hand_ranks = self.order_ranks()
        if 14 in hand_ranks:
            return False
        for i in range(4):
            if (hand_ranks[i] + 1) != hand_ranks[i + 1]:
                return False
        return True

    def is_four_of_kind(self):
        if self.check_same_suit():
            return False
        hand_ranks = self.order_ranks()
        counter = 0
        for i in range(1, 5):
            if hand_ranks[0] == hand_ranks[i]:
                counter += 1
        if counter == 0:
            for i in range(4):
                if hand_ranks[4] == hand_ranks[i]:
                    counter += 1
        if counter == 3:
            return True
        return False

    def is_full_house(self):
        if self.check_same_suit():
            return False
        hand_ranks = self.order_ranks()
        counter_a = 0
        for i in range(1, 5):
            if hand_ranks[0] == hand_ranks[i]:
                counter_a += 1
        counter_b = 0
        for i in range(0, 4):
            if hand_ranks[4] == hand_ranks[i]:
                counter_b += 1
        if (counter_a != 1 and counter_a != 2) or (counter_b != 1 and counter_b != 2) or ((counter_a + counter_b) != 3):
            return False
        return True

    def is_flush(self):
        if self.check_same_suit() and not self.is_straight_flush() and not self.is_royal_flush():
            return True
        return False

    def is_straight(self):
        if self.check_same_suit():
            return False
        hand_ranks = self.order_ranks()
        for i in range(4):
            if (hand_ranks[i] + 1) != hand_ranks[i + 1]:
                return False
        return True

    def is_three_of_kind(self):
        if self.check_same_suit() or self.is_full_house():
            return False
        hand_ranks = self.order_ranks()
        counter = 0
        for i in range(1, 5):
            if hand_ranks[0] == hand_ranks[i]:
                counter += 1
        if counter == 0:
            for i in range(4):
                if hand_ranks[4] == hand_ranks[i]:
                    counter += 1
        if counter == 0:
            for i in range(2, 5):
                if hand_ranks[1] == hand_ranks[i]:
                    counter += 1
        if counter != 2:
            return False
        return True

    def is_two_pair(self):
        if self.check_same_suit() or self.is_four_of_kind() or self.is_full_house():
            return False
        hand_ranks = self.order_ranks()
        # 2-2-1  2-1-2  1-2-2
        if ((hand_ranks[0] == hand_ranks[1]) and (hand_ranks[2] == hand_ranks[3])) or \
                ((hand_ranks[0] == hand_ranks[1]) and (hand_ranks[3] == hand_ranks[4])) or \
                ((hand_ranks[1] == hand_ranks[2]) and (hand_ranks[3] == hand_ranks[4])):
            return True
        return False

    def is_pair(self):
        if self.check_same_suit():
            return False
        hand_ranks = self.order_ranks()
        counter = 0
        for i in range(4):
            if hand_ranks[i] == hand_ranks[i + 1]:
                counter += 1
        if counter != 1:
            return False
        return True

    def is_high_card(self):
        if (not self.is_royal_flush() and not self.is_straight_flush() and not self.is_four_of_kind() and
                not self.is_full_house() and not self.is_flush() and not self.is_straight() and
                not self.is_three_of_kind() and not self.is_two_pair() and not self.is_pair()):
            return True
        return False


simulations = 0
royal_flush = 0
straight_flush = 0
four_of_kind = 0
full_house = 0
flush = 0
straight = 0
three_of_kind = 0
two_pair = 0
pair = 0
high_card = 0

while simulations < 1000000:
    new_deck = Deck()
    new_deck.shuffle()
    new_hand = Hand(new_deck)

    if new_hand.is_royal_flush():
        royal_flush += 1
    if new_hand.is_straight_flush():
        straight_flush += 1
    if new_hand.is_four_of_kind():
        four_of_kind += 1
    if new_hand.is_full_house():
        full_house += 1
    if new_hand.is_flush():
        flush += 1
    if new_hand.is_straight():
        straight += 1
    if new_hand.is_three_of_kind():
        three_of_kind += 1
    if new_hand.is_two_pair():
        two_pair += 1
    if new_hand.is_pair():
        pair += 1
    if new_hand.is_high_card():
        high_card += 1
    simulations += 1


print(royal_flush)
print(straight_flush)
print(four_of_kind)
print(full_house)
print(flush)
print(straight)
print(three_of_kind)
print(two_pair)
print(pair)
print(high_card)
print(royal_flush + straight_flush + four_of_kind + full_house + flush + straight + three_of_kind +
      two_pair + pair + high_card)
