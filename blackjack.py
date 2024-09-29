from decimal import *
import random
import sys
import time

class Player:

    money = 0

    bet = 0

    hand = []

    _score = 0

    @classmethod
    def get_bet(cls, text):
        while True:
            value = get_dec(text)
            if value <= (cls.money + cls.bet):
                cls.money += cls.bet
                cls.bet = value
                cls.money -= cls.bet
                break
            else:
                print(f"You cannot bet more than ${cls.money + cls.bet:.2f}.")

    @classmethod
    def score(cls):
        cls._score = Deck.calculate_hand(cls.hand)
        return cls._score

    @classmethod
    def hit(cls):
        while True:
            print(f"\nYour cards: ", end="")
            for c in cls.hand:
                print(c, end="")
            print("\n")
            pause()
            if cls.score() > 21:
                Dealer.money += cls.bet
                print(f"You busted!\nYou lost ${Player.bet:.2f}.")
                cls.bet = 0
                end()
                break
            elif cls.score() == 21:
                print("Blackjack!")
                break
            elif cls.score() < 21:
                hors = ""
                while True:
                    hors = input("Hit or stay? (h/s): ").strip().lower()
                    if hors in ["h", "hit"]:
                        cls.hand.append(Deck.give_card())
                        break
                    elif hors in ["s", "stay"]:
                        return
                    else:
                        print("Type either 'hit' or 'stay'.")

class Dealer:

    hand = []

    money = 0

    _score = 0

    @classmethod
    def score(cls):
        cls._score = Deck.calculate_hand(cls.hand)
        return cls._score

    @classmethod
    def hit(cls):
        print(f"\nDealer's cards: ", end="")
        for c in cls.hand:
            print(c, end="")
        print(f"\n")
        pause()
        if cls.score() < 17:
            print("The dealer hit.")
            cls.hand.append(Deck.give_card())
            cls.hit()
        elif cls.score() > 21:
            print("The dealer busted!")
            if Player.score() < 21:
                Player.money += Player.bet
                Dealer.money -= Player.bet
                print(f"You earned: ${Player.bet:.2f}.")
            else:
                Player.money += (Player.bet * Decimal("1.5")).quantize(Decimal("0.01"))
                cls.money -= (Player.bet * Decimal("1.5")).quantize(Decimal("0.01"))
                print(f"You earned: ${Player.bet * Decimal("1.5"):.2f}.")
        elif Player.score() > cls.score():
            print("Your score is greater than the dealer's.")
            if Player.score() < 21:
                Player.money += Player.bet
                cls.money -= Player.bet
                print(f"You earned: ${Player.bet:.2f}.")
            else:
                Player.money += (Player.bet * Decimal("1.5")).quantize(Decimal("0.01"))
                cls.money -= (Player.bet * Decimal("1.5")).quantize(Decimal("0.01"))
                print(f"You earned: ${Player.bet * Decimal("1.5"):.2f}.")
        elif cls.score() == Player.score():
            print(f"It's a push!\nYou earned nothing.")
        else:
            print(f"Your score is lower than the dealer's.\nYou lost ${Player.bet:.2f}.")
            cls.money += Player.bet
            Player.bet = 0

class Deck:

    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    suits = ["♠️", "♥️", "♦️", "♣️"]

    cards = []

    @classmethod
    def initialize_cards(cls):
        cls.cards = [rank + suit for rank in cls.ranks for suit in cls.suits]
        random.shuffle(cls.cards)

    @classmethod
    def give_card(cls):
        return cls.cards.pop()

    @classmethod
    def calculate_hand(cls, hand):
        if hand == []:
            return 0
        hand = [c[:-2] for c in hand]
        hand = ["10" if c in ["J", "Q", "K"] else c for c in hand]
        ace_count = hand.count("A")
        non_aces = [c for c in hand if c != "A"]
        non_ace_sum = sum(list(map(int, non_aces)))
        if ace_count == 0:
            return non_ace_sum
        elif non_ace_sum + 11 + (ace_count-1) <= 21:
            return non_ace_sum + 11 + (ace_count-1)
        else:
            return non_ace_sum + ace_count

    @classmethod
    def clear(cls):
        Player.hand = []
        Dealer.hand = []
        cls.initialize_cards()

round = 0

def main():

    print_special(welcome)

    Player.money = get_dec("How much do you want to deposit? ")

    while True:

        global round
        round += 1

        if round == 1:
            Player.get_bet("How much do you want to bet? ")
        else:
            print(f"\nYour balance is: ${Player.money + Player.bet:.2f}.")
            Player.get_bet("New bet: ")

        Deck.clear()

        Player.hand.append(Deck.give_card())
        Player.hand.append(Deck.give_card())

        Dealer.hand.append(Deck.give_card())
        Dealer.hand.append(Deck.give_card())

        print(f"\nDealer's faceup card: " + Dealer.hand[0])

        pause()

        Player.hit()

        if Player.score() > 21:
            continue

        Dealer.hit()

        end()

def end():
    pause()
    if (Player.money + Player.bet) > 0:
        while True:
            again = input(f"\nDo you want to play again? (y/n): ").strip().lower()
            if not again in ["y", "yes", "n", "no"]:
                print("Type 'yes' or 'no'.")
            else:
                break
    else:
        again = "n"
    if again in ["n", "no"]:
        print_special(results)
        pause()
        if round == 1:
            print(f"- You played 1 round in total.\n")
        else:
            print(f"- You played {round} rounds in total.\n")
        pause()
        print(f"- Your final balance is ${Player.money + Player.bet:.2f}.\n")
        pause()
        if Dealer.money > 0:
            print(f"- You lost ${Dealer.money:.2f}.")
            print_special(loser)
        elif Dealer.money < 0:
            print(f"- You earned ${abs(Dealer.money):.2f}.")
            print_special(lucky)
        else:
            print(f"- You neither earned nor lost anything.")
            print_special(the_end)
        sys.exit()

def get_dec(text):
    while True:
        try:
            n = Decimal(input(text).strip())
            getcontext().rounding = ROUND_HALF_UP
            if n <= 0:
                print("Please, type a positive number.")
            else:
                return n.quantize(Decimal("0.01"))
        except InvalidOperation:
                print("Please, type a valid number (no dollar sign).")

def pause():
    time.sleep(2)

def print_special(txt):
    for line in txt.split(f"\n"):
        print(line)
        time.sleep(0.3)

welcome = f"""\n\n\n|░█░|      ░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗  ████████╗░█████╗░	          |░█░|
|░█░|      ░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝  ╚══██╔══╝██╔══██╗	          |░█░|
|░█░|      ░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░  ░░░██║░░░██║░░██║	          |░█░|
|░█░|      ░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░  ░░░██║░░░██║░░██║	          |░█░|
|░█░|      ░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗  ░░░██║░░░╚█████╔╝	          |░█░|
|░█░|      ░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝  ░░░╚═╝░░░░╚════╝░	          |░█░|
|░█░|   												  |░█░|
|░█░|   ███╗░░░███╗░█████╗░██╗██╗░░██╗███████╗██╗░██████╗  ░█████╗░░█████╗░░██████╗██╗███╗░░██╗░█████╗░   |░█░|
|░█░|   ████╗░████║██╔══██╗██║██║░██╔╝██╔════╝╚█║██╔════╝  ██╔══██╗██╔══██╗██╔════╝██║████╗░██║██╔══██╗   |░█░|
|░█░|   ██╔████╔██║███████║██║█████═╝░█████╗░░░╚╝╚█████╗░  ██║░░╚═╝███████║╚█████╗░██║██╔██╗██║██║░░██║   |░█░|
|░█░|   ██║╚██╔╝██║██╔══██║██║██╔═██╗░██╔══╝░░░░░░╚═══██╗  ██║░░██╗██╔══██║░╚═══██╗██║██║╚████║██║░░██║   |░█░|
|░█░|   ██║░╚═╝░██║██║░░██║██║██║░╚██╗███████╗░░░██████╔╝  ╚█████╔╝██║░░██║██████╔╝██║██║░╚███║╚█████╔╝   |░█░|
|░█░|   ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚═╝╚══════╝░░░╚═════╝░  ░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝░╚════╝░   |░█░|\n\n\n"""

results = f"""\n\n\n══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                          ██████╗░███████╗░██████╗██╗░░░██╗██╗░░░░░████████╗░██████╗
                          ██╔══██╗██╔════╝██╔════╝██║░░░██║██║░░░░░╚══██╔══╝██╔════╝
                          ██████╔╝█████╗░░╚█████╗░██║░░░██║██║░░░░░░░░██║░░░╚█████╗░
                          ██╔══██╗██╔══╝░░░╚═══██╗██║░░░██║██║░░░░░░░░██║░░░░╚═══██╗
                          ██║░░██║███████╗██████╔╝╚██████╔╝███████╗░░░██║░░░██████╔╝
                          ╚═╝░░╚═╝╚══════╝╚═════╝░░╚═════╝░╚══════╝░░░╚═╝░░░╚═════╝░

══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════\n\n\n"""

loser = f"""\n\n\n══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════

   ██████╗░██╗░░░██╗███████╗░░░░░░██████╗░██╗░░░██╗███████╗░░░  ██╗░░░░░░█████╗░░██████╗███████╗██████╗░██╗
   ██╔══██╗╚██╗░██╔╝██╔════╝░░░░░░██╔══██╗╚██╗░██╔╝██╔════╝░░░  ██║░░░░░██╔══██╗██╔════╝██╔════╝██╔══██╗██║
   ██████╦╝░╚████╔╝░█████╗░░█████╗██████╦╝░╚████╔╝░█████╗░░░░░  ██║░░░░░██║░░██║╚█████╗░█████╗░░██████╔╝██║
   ██╔══██╗░░╚██╔╝░░██╔══╝░░╚════╝██╔══██╗░░╚██╔╝░░██╔══╝░░██╗  ██║░░░░░██║░░██║░╚═══██╗██╔══╝░░██╔══██╗╚═╝
   ██████╦╝░░░██║░░░███████╗░░░░░░██████╦╝░░░██║░░░███████╗╚█║  ███████╗╚█████╔╝██████╔╝███████╗██║░░██║██╗
   ╚═════╝░░░░╚═╝░░░╚══════╝░░░░░░╚═════╝░░░░╚═╝░░░╚══════╝░╚╝  ╚══════╝░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝

══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════"""

the_end = f"""\n\n\n══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                             ████████╗██╗░░██╗███████╗  ███████╗███╗░░██╗██████╗░
                             ╚══██╔══╝██║░░██║██╔════╝  ██╔════╝████╗░██║██╔══██╗
                             ░░░██║░░░███████║█████╗░░  █████╗░░██╔██╗██║██║░░██║
                             ░░░██║░░░██╔══██║██╔══╝░░  ██╔══╝░░██║╚████║██║░░██║
                             ░░░██║░░░██║░░██║███████╗  ███████╗██║░╚███║██████╔╝
                             ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚══════╝╚═╝░░╚══╝╚═════╝░

══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════"""

lucky = f"""\n\n\n══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                    ██╗░░░░░██╗░░░██╗░█████╗░██╗░░██╗██╗░░░██╗  ██╗░░░██╗░█████╗░██╗░░░██╗
                    ██║░░░░░██║░░░██║██╔══██╗██║░██╔╝╚██╗░██╔╝  ╚██╗░██╔╝██╔══██╗██║░░░██║
                    ██║░░░░░██║░░░██║██║░░╚═╝█████═╝░░╚████╔╝░  ░╚████╔╝░██║░░██║██║░░░██║
                    ██║░░░░░██║░░░██║██║░░██╗██╔═██╗░░░╚██╔╝░░  ░░╚██╔╝░░██║░░██║██║░░░██║
                    ███████╗╚██████╔╝╚█████╔╝██║░╚██╗░░░██║░░░  ░░░██║░░░╚█████╔╝╚██████╔╝
                    ╚══════╝░╚═════╝░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░░╚════╝░░╚═════╝░

══════════════════════════════════════════════════════════════════════════════════════════════════════════════
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
══════════════════════════════════════════════════════════════════════════════════════════════════════════════"""

if __name__ == "__main__":
    main()
