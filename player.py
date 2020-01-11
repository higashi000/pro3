from websocket_server import WebsocketServer
import copy
import random

class Player:
    hand = []
    hand_json = ""
    my_client = ""
    next_user = ""
    previous_user = ""

    def __init__(self, hand, my_client, next_user, previous_user):
        self.hand = hand
        self.my_client = my_client
        self.previous_user = previous_user
        self.next_user = next_user
        self.hand_delete()

    # 手札アップデート
    def update_hand(self, card):
        self.hand.append(card)
        self.hand_delete()

    # 手札のjson文字列作成
    def creat_hand_json(self):
        self.hand_json = "\"card\":["

        cnt = 0
        for i in self.hand:
            self.hand_json += "\"" + i + "\""
            if cnt < len(self.hand) - 1:
                self.hand_json += ','
            cnt += 1

        self.hand_json += "]"


    # 手札の重複を確認、捨てる
    def hand_delete(self):
        self.hand.sort()
        new_hand = []

        for i in range(0, len(self.hand) - 1):
            first_hand = self.hand[i]
            second_hand = self.hand[i + 1]
            if first_hand[:2] != second_hand[:2]:
                new_hand.append(self.hand[i])

        self.hand = copy.copy(new_hand)
        self.creat_hand_json()


    # カードを引く
    def draw_card(self, draw_card):
        self.update_hand(draw_card)

    # 手札を引かれる
    def drawn_hand(self):
        drawn_card_index = random.randint(0, len(self.hand) - 1)

        drawn_card = self.hand.pop(drawn_card_index)

        self.creat_hand_json()
        return drawn_card

    def check_win(self):
        if len(self.hand) == 0:
            return True
        else:
            return False
