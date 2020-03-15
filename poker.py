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
hands_dict = {"Royal Flush": 0, "Straight Flush": 0, "Four of a Kind": 0, "Full House": 0, "Flush": 0, "Straight": 0,
              "Three of a Kind": 0, "Two Pair": 0, "Pair": 0, "High Card": 0}

while simulations < 10000:
    new_deck = Deck()
    new_deck.shuffle()
    new_hand = Hand(new_deck)

    if new_hand.is_royal_flush():
        hands_dict["Royal Flush"] += 1
    if new_hand.is_straight_flush():
        hands_dict["Straight Flush"] += 1
    if new_hand.is_four_of_kind():
        hands_dict["Four of a Kind"] += 1
    if new_hand.is_full_house():
        hands_dict["Full House"] += 1
    if new_hand.is_flush():
        hands_dict["Flush"] += 1
    if new_hand.is_straight():
        hands_dict["Straight"] += 1
    if new_hand.is_three_of_kind():
        hands_dict["Three of a Kind"] += 1
    if new_hand.is_two_pair():
        hands_dict["Two Pair"] += 1
    if new_hand.is_pair():
        hands_dict["Pair"] += 1
    if new_hand.is_high_card():
        hands_dict["High Card"] += 1
    simulations += 1

total_hands = 0
for value in hands_dict.values():
    total_hands += value

probabilities = {"Royal Flush": 0, "Straight Flush": 0, "Four of a Kind": 0, "Full House": 0, "Flush": 0, "Straight": 0,
                 "Three of a Kind": 0, "Two Pair": 0, "Pair": 0, "High Card": 0}
for h in hands_dict:
    probabilities[h] = round((hands_dict[h]/total_hands)*100, 2)

max_prob_hand = list(probabilities.keys())[list(probabilities.values()).index(max(probabilities.values()))]
min_prob_hand = list(probabilities.keys())[list(probabilities.values()).index(min(probabilities.values()))]

print("Total of hands:", total_hands)
for h in hands_dict:
    print(h + ": " + str(hands_dict[h]) + " -> Probability of appearance in 10K hands: " + str(probabilities[h]) + "%")

print("The hand that appeared the most is:", max_prob_hand)
print("The hand that appeared the least is:", min_prob_hand)
