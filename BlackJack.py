from Decks import Decks
from RuleUtil import get_points, will_dealer_continue, who_win


class BlackJack:
    def __init__(self, stand_on_soft_17):
        self.stand_on_soft_17 = stand_on_soft_17
        # 1副扑克牌
        self.cards = Decks(1)

    # after set up, player 2 cards >= 17 without "A"
    def stand_after_setup(self, dealer_cards, player_cards):
        player_point = get_points(player_cards)
        # 先不算 double bet，不算 split，只算如果 H 赢的概率，如果 s 赢的概率
        if player_point[0] < 17:
            Exception("This function is handle points >= 17")
        # player - Stand. dfs 列出 dealer 的所有可能性
        self.cards.mark_cards_popped(dealer_cards)
        self.cards.mark_cards_popped(player_cards)
        dealer_all_possibility = []
        self.dfs_all_dealer_possibility(dealer_cards, dealer_all_possibility)
        who_win_list = []
        for dealer_one_possible in dealer_all_possibility:
            # print(dealer_one_possible)
            who_win_list.append(who_win(dealer_one_possible, player_cards))

        # calculate results and print
        player_win_times = 0
        dealer_win_times = 0
        push_times = 0
        for res in who_win_list:
            if res == "Dealer":
                dealer_win_times += 1
            elif res == "Player":
                player_win_times += 1
            elif res == "Push":
                push_times += 1
        total = dealer_win_times + player_win_times + push_times
        print(f"Dealer wins: {dealer_win_times}, chance: {dealer_win_times / total}")
        print(f"Player wins: {player_win_times}, chance: {player_win_times / total}")
        print(f"Push times: {push_times}, chance: {push_times / total}")


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