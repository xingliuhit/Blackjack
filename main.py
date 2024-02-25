from RuleUtil import get_points, will_dealer_continue, who_win
from BlackJack import BlackJack

def unit_test():
    print("unit_test: ")
    # RuleUtil
    # print(get_points(["A", "3"]))
    # print(get_points(["3", "7", "10"]))
    # print(get_points(["3", "A", "10"]))
    # print(get_points(["3", "A", "10", "A"]))
    # print(get_points(["3", "A", "J", "A"]))
    # print(should_dealer_continue(["7", "8"], True))
    # print(should_dealer_continue(["7", "J"], True))
    # print(should_dealer_continue(["2", "3"], True))
    # print(should_dealer_continue(["8", "10"], True))
    # print(should_dealer_continue(["7", "A"], True))
    # print(should_dealer_continue(["A", "3"], True))
    # print(should_dealer_continue(["6", "A"], True))
    # print(should_dealer_continue(["3", "3", "A"], True))
    # print(should_dealer_continue(["6", "A"], False))
    # print(should_dealer_continue(["3", "3", "A"], False))
    print(who_win(['2', '7', '3', '2', '3'], ["7", "10"]))


def play_blackkack():
    blackjack = BlackJack(False)
    dealer_cards = ["10"]
    player_cards = ["2", "10"]
    blackjack.stand_after_setup(dealer_cards, player_cards)


if __name__ == '__main__':
    # unit_test()
    play_blackkack()
