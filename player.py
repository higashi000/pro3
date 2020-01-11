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
    def create_hand_json(self):
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
        after_delete = []
        self.hand.sort()

        while True:
            if self.hand[0][:2] != self.hand[1][:2]:
                after_delete.append(self.hand.pop(0))
            else:
                self.hand.pop(0)
                self.hand.pop(0)

            if len(self.hand) == 0:
                break

            if len(self.hand) == 1:
                after_delete.append(self.hand.pop(0))
                break

        self.hand = copy.copy(after_delete)

        if len(self.hand) != 0:
            self.create_hand_json()
        else:
            self.hand_json = "\"card\":\"nothing\""


    # カードを引く
    def draw_card(self, draw_card):
        self.update_hand(draw_card)

    # 手札を引かれる
    def drawn_hand(self):
        drawn_card_index = random.randint(0, len(self.hand) - 1)

        drawn_card = self.hand.pop(drawn_card_index)

        if len(self.hand) != 0:
            self.create_hand_json()
        else:
            self.hand_json = "\"card\":\"nothing\""
        return drawn_card

    def check_win(self):
        if len(self.hand) == 0:
            return True
        else:
            return False
