class Decks:
    def __init__(self, deck_number):
        # card value and how many of this card
        self.number_of_same_card = 4 * deck_number
        self.cards_to_number_map = {
            "A": self.number_of_same_card,
            "2": self.number_of_same_card,
            "3": self.number_of_same_card,
            "4": self.number_of_same_card,
            "5": self.number_of_same_card,
            "6": self.number_of_same_card,
            "7": self.number_of_same_card,
            "8": self.number_of_same_card,
            "9": self.number_of_same_card,
            "10": self.number_of_same_card,
            "J": self.number_of_same_card,
            "Q": self.number_of_same_card,
            "K": self.number_of_same_card,
        }

    def mark_cards_popped(self, cards):
        for card in cards:
            self.cards_to_number_map[card] -= 1

    def mark_card_popped(self, card):
        self.cards_to_number_map[card] -= 1
        if self.cards_to_number_map[card] < 0:
            raise Exception("number of same card is below 0, impossible!")

    def unmark_cards_popped(self, cards):
        for card in cards:
            self.unmark_card_popped(card)

    def unmark_card_popped(self, card):
        self.cards_to_number_map[card] += 1
        if self.cards_to_number_map[card] > self.number_of_same_card:
            raise Exception("number of same card is bigger than max, impossible!")

    def get_remaining_cards_in_map(self):
        return self.cards_to_number_map

    def get_remaining_cards_in_list(self):
        cards_list = []
        for key, value in self.cards_to_number_map.items():
            for i in range(0, value):
                cards_list.append(key)
        return cards_list
