import random
from tkinter import *
from PIL import ImageTk, Image  # used to load a JPG file

suits = ["S", "H", "D", "C"]
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

    def print_canvas(self, canvas):
        size = 175, 500
        for i in range(5):
            card_name = self.cards[i].get_rank() + self.cards[i].get_suit() + ".png"
            im = Image.open("PNG/" + card_name)
            im.thumbnail(size)
            canvas[i].image = ImageTk.PhotoImage(im)
            canvas[i].create_image(20, 50, image=canvas[i].image, anchor='nw')

    def rank_hand(self):
        output = "This is a {} hand"
        if self.is_royal_flush():
            return output.format("Royal Flush")
        if self.is_straight_flush():
            return output.format("Straight Flush")
        if self.is_four_of_kind():
            return output.format("Four of a Kind")
        if self.is_full_house():
            return output.format("Full House")
        if self.is_flush():
            return output.format("Flush")
        if self.is_straight():
            return output.format("Straight")
        if self.is_three_of_kind():
            return output.format("Three of a Kind")
        if self.is_two_pair():
            return output.format("Two Pair")
        if self.is_pair():
            return output.format("Pair")
        return output.format("High Card")


stats_on = False
if stats_on:
    simulations = 0
    hands_dict = {"Royal Flush": 0, "Straight Flush": 0, "Four of a Kind": 0, "Full House": 0, "Flush": 0,
                  "Straight": 0, "Three of a Kind": 0, "Two Pair": 0, "Pair": 0, "High Card": 0}

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

    probabilities = {"Royal Flush": 0, "Straight Flush": 0, "Four of a Kind": 0, "Full House": 0, "Flush": 0,
                     "Straight": 0, "Three of a Kind": 0, "Two Pair": 0, "Pair": 0, "High Card": 0}
    for h in hands_dict:
        probabilities[h] = round((hands_dict[h]/total_hands)*100, 2)

    max_prob_hand = list(probabilities.keys())[list(probabilities.values()).index(max(probabilities.values()))]
    min_prob_hand = list(probabilities.keys())[list(probabilities.values()).index(min(probabilities.values()))]

    print("Total of hands:", total_hands)
    for h in hands_dict:
        print(h + ": " + str(hands_dict[h]) + " -> Probability of appearance in 10K hands: " +
              str(probabilities[h]) + "%")

    print("The hand that appeared the most is:", max_prob_hand)
    print("The hand that appeared the least is:", min_prob_hand)


class GUI:
    def __init__(self, w):
        self.window = w
        bg_color = "#00338D"
        title = "This program will deal 5 cards and tell you what hand you have got"

        # Adding Title and Size
        self.window.title("Poker Game")
        self.window.geometry("1275x600")
        self.window.resizable(0, 0)

        # Creating a Frame
        self.frame = Frame(master=window, bg=bg_color)
        self.frame.pack_propagate(0)  # Do not allow widgets inside to determine the frame's dimensions
        self.frame.pack(fill=BOTH, expand=1)  # Expand the frame to fill the root window

        # Create a Canvas
        self.cards_frame = Frame(master=self.frame)
        self.canvas = []
        for i in range(5):
            self.canvas.append(Canvas(master=self.cards_frame, width=215, height=375, bg="#7AA52B", highlightthickness=0))
            self.canvas[i].grid(row=0, column=i)
        self.cards_frame.grid(row=1, rowspan=3, padx=20)

        self.label = Label(self.frame, text="", bg=bg_color, fg="white")
        self.label.grid(row=5)
        self.label.config(font=("Segoe UI", 44))
        label2 = Label(self.frame, text=title, bg=bg_color, fg="white")
        label2.grid(row=0, columnspan=2, pady=20)
        label2.config(font=("Segoe UI", 20))

        self.bt1 = Button(self.frame, text="Play", command=self.deal, bg="#7AA52B", fg="white")
        self.bt1.config(font=("Segoe UI", 15))
        self.bt1.grid(row=2, column=1, columnspan=2)
        self.bt3 = Button(self.frame, text="Get Premium", command=self.get_premium)
        self.bt3.config(font=("Segoe UI", 15))
        self.bt3.grid(row=1, column=1, columnspan=2)
        self.bt2 = Button(self.frame, text="Exit Game", command=self.exit_game, bg="black", fg="yellow")
        self.bt2.config(font=("Segoe UI", 15))
        self.bt2.grid(row=3, column=2)

    def deal(self):
        new_deck = Deck()
        new_deck.shuffle()
        hand = Hand(new_deck)
        hand.print_canvas(self.canvas)
        self.label.config(text=hand.rank_hand())

    def get_premium(self):
        while True:
            new_deck = Deck()
            new_deck.shuffle()
            hand = Hand(new_deck)

            if hand.is_straight() or hand.is_flush():
                hand.print_canvas(self.canvas)
                break
        self.label.config(text=hand.rank_hand())

    @staticmethod
    def exit_game():
        exit(0)


# Creating a Window
window = Tk()
poker_game = GUI(window)
window.mainloop()
