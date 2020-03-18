from tkinter import *
import poker


class GUI:
    def __init__(self, window):
        self.window = window
        bg_color = "#00338D"
        title = "This program will deal 5 cards and tell you what hand you have got"

        # Adding Title and Size
        window.title("Poker Game")
        window.geometry("1450x700")
        window.resizable(0, 0)

        # Creating a Frame
        self.frame = Frame(master=window, bg=bg_color)
        self.frame.pack_propagate(0)  # Do not allow widgets inside to determine the frame's dimensions
        self.frame.pack(fill=BOTH, expand=1)  # Expand the frame to fill the root window

        # Create a Canvas
        self.cards_frame = Frame(master=self.frame)
        self.canvas = []
        for i in range(5):
            self.canvas.append(Canvas(master=self.cards_frame, width=250, height=500, bg="#7AA52B", highlightthickness=0))
            self.canvas[i].grid(row=0, column=i)
        self.cards_frame.grid(row=1, rowspan=3, padx=20)

        self.label = Label(self.frame, text="", bg=bg_color, fg="white")
        self.label.grid(row=5)
        self.label.config(font=("Segoe UI", 44))
        label2 = Label(self.frame, text=title, bg=bg_color, fg="white")
        label2.grid(row=0, columnspan=2)
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
        new_deck = poker.Deck()
        new_deck.shuffle()
        hand = poker.Hand(new_deck)
        poker.Hand.print_canvas(poker.Hand(new_deck), self.canvas)
        self.label.config(text=hand.rank_hand())

    def get_premium(self):
        while True:
            new_deck = poker.Deck()
            new_deck.shuffle()
            hand = poker.Hand(new_deck)

            if hand.is_royal_flush() or hand.is_straight_flush() or hand.is_four_of_kind() or hand.is_full_house() \
                    or hand.is_flush():
                poker.Hand.print_canvas(poker.Hand(new_deck), self.canvas)
                break
        self.label.config(text=hand.rank_hand())

    def exit_game(self):
        exit(0)


# Creating a Window
window = Tk()
poker_game = GUI(window)
window.mainloop()
