class Decks:
    def __init__(self, deck_number):
        # card value and how many of this card
        number_of_same_card = 4 * deck_number
        self.cards_number_map = {
            "A": number_of_same_card,
            "2": number_of_same_card,
            "3": number_of_same_card,
            "4": number_of_same_card,
            "5": number_of_same_card,
            "6": number_of_same_card,
            "7": number_of_same_card,
            "8": number_of_same_card,
            "9": number_of_same_card,
            "10": number_of_same_card,
            "J": number_of_same_card,
            "Q": number_of_same_card,
            "K": number_of_same_card,
        }

    def mark_cards_popped(self, cards):
        for card_number in cards:
            self.cards_number_map[card_number] -= 1

    def mark_card_popped(self, card_number):
        self.cards_number_map[card_number] -= 1

    def unmark_card_popped(self, card_number):
        self.cards_number_map[card_number] += 1

    def get_remaining_cards_in_map(self):
        return self.cards_number_map

    def get_remaining_cards_in_list(self):
        cards_list = []
        for key, value in self.cards_number_map.items():
            for i in range(0, value):
                cards_list.append(key)
        return cards_list
