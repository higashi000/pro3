def hand_delete(hand):
    new_hand = []
    hand.sort()

    first_hand = ""
    second_hand = ""
    first_hand = hand.pop()
    second_hand = hand.pop()

    while len(hand) > 0:
        if first_hand != second_hand:
            new_hand.append(first_hand)
            first_hand = second_hand
            second_hand = hand.pop()
        else:
            first_hand = hand.pop()
            second_hand = hand.pop()

    return new_hand
