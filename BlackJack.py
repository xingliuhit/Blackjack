from Decks import Decks
from RuleUtil import get_all_possible_points, will_dealer_continue, who_win, get_blackjack_point


def calculate_result(dealer_win_times, player_win_times, push_times):
    total = dealer_win_times + player_win_times + push_times
    print(f"Dealer wins: {dealer_win_times}, chance: {100 * dealer_win_times / total}%")
    print(f"Player wins: {player_win_times}, chance: {100 * player_win_times / total}%")
    print(f"Push times: {push_times}, chance: {100 * push_times / total}%")
    return [dealer_win_times / total, player_win_times / total, push_times / total]


class BlackJack:
    def __init__(self, stand_on_soft_17):
        self.stand_on_soft_17 = stand_on_soft_17
        # 1副扑克牌
        self.cards = Decks(1)

    # player choose to stand
    def player_stand(self, dealer_cards, player_cards):
        # print("player choose to Stand")
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)

        # dfs 列出 dealer 的所有可能性
        dealer_all_possibility = []
        self.dfs_all_dealer_possibility(dealer_cards, dealer_all_possibility)
        who_win_list = []
        for dealer_one_possible in dealer_all_possibility:
            # print(dealer_one_possible)
            who_win_list.append(who_win(dealer_one_possible, player_cards))

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
        return calculate_result(dealer_win_times, player_win_times, push_times)

    # player choose to Hit. 这个概率算起来比较复杂，因为 player 的选择是不固定的.
    # 但有个好处，player 如果第一下选择了 Hit, 那也就不存在 double bet，split 的情况了
    def player_hit(self, dealer_cards, player_cards):
        # print("player choose to Hit")
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)

        # player hit, find all possibilities with only adding 1 card
        player_all_possibility = []
        remaining_cards = self.cards.get_remaining_cards_in_list()
        for card in remaining_cards:
            player_cards.append(card)
            player_all_possibility.append(list(player_cards))
            player_cards.pop()

        player_bust_probability = 0.0
        dealer_win_probability = 0.0
        player_win_probability = 0.0
        push_probability = 0.0

        # if player choose to stand
        for next_player_cards in player_all_possibility:
        [next_dealer_win_probability, next_player_win_probability, next_push_probility] = self

        # if palyer choose to Hit




    def dfs_all_dealer_possibility(self, dealer_cards, dealer_all_possibility):
        if not will_dealer_continue(dealer_cards, self.stand_on_soft_17):
            dealer_all_possibility.append(list(dealer_cards))
            # print(dealer_cards)
            return
        remaining_cards = self.cards.get_remaining_cards_in_list()
        for next_card in remaining_cards:
            dealer_cards.append(next_card)
            self.cards.mark_card_popped(next_card)
            self.dfs_all_dealer_possibility(dealer_cards, dealer_all_possibility)
            self.cards.unmark_card_popped(next_card)
            dealer_cards.pop()