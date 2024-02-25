from Decks import Decks
from RuleUtil import get_all_possible_points, will_dealer_continue, who_win, get_blackjack_point, is_cards_bust


def calculate_result(dealer_win_times, player_win_times, push_times):
    total = dealer_win_times + player_win_times + push_times
    # print(f"Dealer wins: {dealer_win_times}, chance: {100 * dealer_win_times / total}%")
    # print(f"Player wins: {player_win_times}, chance: {100 * player_win_times / total}%")
    # print(f"Push times: {push_times}, chance: {100 * push_times / total}%")
    return [dealer_win_times / total, player_win_times / total, push_times / total]


def get_player_expected_income(probabilities):
    # probabilities sum should be 1
    dealer_win_probability = probabilities[0]
    player_win_probability = probabilities[1]
    push_probability = probabilities[2]
    return 2*player_win_probability - dealer_win_probability + push_probability


class BlackJack:
    def __init__(self, stand_on_soft_17):
        self.dealer_all_possibility = []
        self.stand_on_soft_17 = stand_on_soft_17
        # 1 副扑克牌
        self.cards = Decks(1)

    # just after setup
    def play(self, dealer_cards, player_cards):
        print(f"dealer_cards: {dealer_cards}")
        print(f"player_cards: {player_cards}")
        # 严格来说，这个 self.dealer_all_possibility 是不准的，但可以近似，应该对最终结果影响不大
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)
        find_dealer_all_possibility = []
        self.dfs_all_dealer_possibility(dealer_cards, find_dealer_all_possibility)
        self.dealer_all_possibility = find_dealer_all_possibility
        self.cards.unmark_cards_popped(dealer_cards)
        self.cards.unmark_cards_popped(player_cards)

        # 成本是 1， 收益是在 [0, 2].
        print(f"Stand, Expected Income: {self.player_stand(dealer_cards, player_cards)}")
        # print(f"Hit, Expected Income: {self.player_hit(dealer_cards, player_cards)}")
        print(f"Double Down, Expected Income: {self.player_double_down(dealer_cards, player_cards)}")
        print(f"Surrender, Expected Income: {self.player_surrender()}")

    # player choose to stand
    def player_stand(self, dealer_cards, player_cards):
        # print("player choose to Stand")
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)

        who_win_list = []
        for dealer_one_possible in self.dealer_all_possibility:
            who_win_list.append(who_win(dealer_one_possible, player_cards))

        self.cards.unmark_cards_popped(dealer_cards)
        self.cards.unmark_cards_popped(player_cards)

        # calculate results and print
        dealer_win_times = 0
        player_win_times = 0
        push_times = 0
        for res in who_win_list:
            if res == "Dealer":
                dealer_win_times += 1
            elif res == "Player":
                player_win_times += 1
            elif res == "Push":
                push_times += 1
        return get_player_expected_income(calculate_result(dealer_win_times, player_win_times, push_times))

    # player choose to Hit. 这个概率算起来比较复杂，因为 player 的选择是不固定的.
    # 但有个好处，player 如果第一下选择了 Hit, 那也就不存在 double bet，split 的情况了
    # player_cards 是手上已经有的牌，下一把 Hit 的预期收益
    def player_hit(self, dealer_cards, player_cards):
        # print("player choose to Hit")
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)

        expected_income = 0

        # player hit, find all possibilities with only adding 1 card
        player_all_possibility = []
        remaining_cards = self.cards.get_remaining_cards_in_list()
        for card in remaining_cards:
            player_cards.append(card)
            player_all_possibility.append(list(player_cards))
            player_cards.pop()

        player_all_possibility_no_bust = []
        for next_player_cards in player_all_possibility:
            if is_cards_bust(next_player_cards):
                expected_income -= (1 / len(player_all_possibility))
            else:
                player_all_possibility_no_bust.append(next_player_cards)

        for next_player_cards in player_all_possibility_no_bust:
            # if player choose to stand. 有个问题，我并不知道再一次，player stand 的概率. 所以还是应该是拿到牌
            next_stand_expected_income = self.player_stand(dealer_cards, next_player_cards)
            # if player choose to Hit
            next_hit_expected_income = self.player_hit(dealer_cards, next_player_cards)
            expected_income += max(next_stand_expected_income, next_hit_expected_income) * (1 / len(player_all_possibility))

        self.cards.unmark_cards_popped(dealer_cards)
        self.cards.unmark_cards_popped(player_cards)
        return expected_income

    # only happen after the setup, and player only get 1 more card
    def player_double_down(self, dealer_cards, player_cards):
        # print("player choose to Double Down")
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)

        expected_income = 0

        # player hit, find all possibilities with only adding 1 card
        player_all_possibility = []
        remaining_cards = self.cards.get_remaining_cards_in_list()
        for card in remaining_cards:
            player_cards.append(card)
            player_all_possibility.append(list(player_cards))
            player_cards.pop()

        player_all_possibility_no_bust = []
        for next_player_cards in player_all_possibility:
            if is_cards_bust(next_player_cards):
                expected_income -= (1 / len(player_all_possibility))
            else:
                player_all_possibility_no_bust.append(next_player_cards)

        for next_player_cards in player_all_possibility_no_bust:
            next_stand_expected_income = self.player_stand(dealer_cards, next_player_cards)
            expected_income += next_stand_expected_income * (1 / len(player_all_possibility))

        self.cards.unmark_cards_popped(dealer_cards)
        self.cards.unmark_cards_popped(player_cards)
        return expected_income

    # only happen after the setup (after you have seen your first two cards)
    def player_surrender(self):
        return 0.5

    def dfs_all_dealer_possibility(self, dealer_cards, find_dealer_all_possibility):
        if not will_dealer_continue(dealer_cards, self.stand_on_soft_17):
            find_dealer_all_possibility.append(list(dealer_cards))
            return
        remaining_cards = self.cards.get_remaining_cards_in_list()
        for next_card in remaining_cards:
            dealer_cards.append(next_card)
            self.cards.mark_card_popped(next_card)
            self.dfs_all_dealer_possibility(dealer_cards, find_dealer_all_possibility)
            self.cards.unmark_card_popped(next_card)
            dealer_cards.pop()
