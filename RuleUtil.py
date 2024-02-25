map_card_to_value = {
    "A": [1, 11],
    "2": [2],
    "3": [3],
    "4": [4],
    "5": [5],
    "6": [6],
    "7": [7],
    "8": [8],
    "9": [9],
    "10": [10],
    "J": [10],
    "Q": [10],
    "K": [10],
}


def is_point_bust(point):
    return point > 21

def is_cards_bust(cards):
    points = get_all_possible_points(cards)
    if points[0] > 21:
        return True
    return False

def who_win(dealer_cards, player_cards):
    dealer_points = get_all_possible_points(dealer_cards)
    player_points = get_all_possible_points(player_cards)
    dealer_point = get_blackjack_point(dealer_cards)
    player_point = get_blackjack_point(player_cards)
    if dealer_point > player_point:
        return "Dealer"
    elif dealer_point < player_point:
        return "Player"
    else:
        return "Push"


def get_blackjack_point(cards):
    blackjack_point = -1
    points = get_all_possible_points(cards)
    for point in points:
        if not is_point_bust(point):
            blackjack_point = max(blackjack_point, point)
    return blackjack_point


def get_all_possible_points(cards):
    result = []
    __dfs_cards_get_to_points(cards, result, 0, 0)
    return result


def will_dealer_continue(cards, stand_on_soft_17):
    if len(cards) == 1:
        return True
    if "A" in cards:
        # 如果有两张 A, 那第二张必然是 1 点
        # 是一个以 10 为差的等差数列
        points = get_all_possible_points(cards)
        points.sort()
        if points[1] >= 18:
            return False
        elif points[1] == 17:
            if stand_on_soft_17:
                return False
            else:
                return True
        else:
            return True
    else:
        point = get_all_possible_points(cards)[0]
        if point <= 16:
            return True
        else:
            return False


def __dfs_cards_get_to_points(cards, result, i, cur_point):
    if i == len(cards):
        result.append(cur_point)
        return
    card = cards[i]
    if card not in map_card_to_value:
        Exception('invalid card')
    if card == "A":
        for value in map_card_to_value[card]:
            cur_point += value
            __dfs_cards_get_to_points(cards, result, i + 1, cur_point)
            cur_point -= value
    else:
        __dfs_cards_get_to_points(cards, result, i + 1, cur_point + map_card_to_value[card][0])
