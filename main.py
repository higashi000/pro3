from websocket_server import WebsocketServer
import random
import json
import player

users = []
finish_user = []
client_list = []
rank_cnt = 1
now_player = ""

card = ["01c", "02c", "03c", "04c", "05c", "06c", "07c", "08c", "09c", "10c", "11c", "12c", "13c",
        "01s", "02s", "03s", "04s", "05s", "06s", "07s", "08s", "09s", "10s", "11s", "12s", "13s",
        "01d", "02d", "03d", "04d", "05d", "06d", "07d", "08d", "09d", "10d", "11d", "12d", "13d",
        "01h", "02h", "03h", "04h", "05h", "06h", "07h", "08h", "09h", "10h", "11h", "12h", "13h",
        "00j"]

def separate_card():
    random.shuffle(card)
    handover_card = [card[0:13], card[13:26], card[26:39], card[39:]]
    random.shuffle(handover_card)

    users.append(player.Player(handover_card[0], client_list[0], client_list[1], client_list[3]))
    users.append(player.Player(handover_card[1], client_list[1], client_list[2], client_list[0]))
    users.append(player.Player(handover_card[2], client_list[2], client_list[3], client_list[1]))
    users.append(player.Player(handover_card[3], client_list[3], client_list[0], client_list[2]))

def game_start(server):
    global now_player
    now_player = users[0].my_client

    for i in users:
        print("{\"status\":\"true\",\"message\":\"game start\"," + i.hand_json + "}")
        server.send_message(i.my_client, "{\"status\":\"true\",\"message\":\"game start\"," + i.hand_json + "}")


def check_order(client):
    if client == now_player:
        return True
    else:
        return False

def update_order():
    global now_player
    for i in users:
        if i.my_client == now_player:
            now_player = i.next_user
            return

def new_client(client, server):
    if len(client_list) < 4:
        client_list.append(client)
        server.send_message(client, "{\"status\":\"true\",\"message\":\"successful connect\",\"id\":\"" + str(client['id']) + "\"}")
        print("Join new user")
    else:
        print("over capacity")
        server.send_message(client, "{\"status\":\"false\",\"message\":\"Sorry over capacity\"}")
        return

    if len(client_list) == 4:
        separate_card()
        game_start(server)

def message_received(client, server, message):
    receive_data = json.loads(message)

    if receive_data["request"] == "draw":
        print(receive_data)
        if check_order(client) == True:
            draw_card(server, client)
        else:
            server.send_message(client, "{\"status\":\"false\",\"message\":\"There is not it in order of you\"}")


# 勝ちならそのユーザーを順番から除外する
def check_win(user):
    global users
    global finish_user
    win = False
    if user.check_win():
        win = True
        for i in range(len(users)):
            if users[i].my_client == user.previous_user:
                users[i].next_user = user.next_user
                break
        for i in range(len(users)):
            if users[i].my_client == user.next_user:
                users[i].previous_user = user.previous_user
                break

        for i in range(len(users)):
            if users[i] == user:
                finish_user.append(users[i])
                break

    return win

# カードを引いた結果をクライアントに渡す
def send_result(server, draw_client, drawn_client, card):
    global finish_user

    if check_win(drawn_client):
        server.send_message(drawn_client.my_client, "{\"status\":\"true\",\"message\":\"You win\",\"draw_card\":\"" + card + "\"}")
    else:
        server.send_message(drawn_client.my_client, "{\"status\":\"true\",\"message\":\"drawn card\"," + drawn_client.hand_json + ",\"draw_card\":\"" + card +"\"}")

    if check_win(draw_client):
        server.send_message(draw_client.my_client, "{\"status\":\"true\",\"message\":\"You win\",\"draw_card\":\"" + card + "\"}")
    else:
        server.send_message(draw_client.my_client, "{\"status\":\"true\",\"message\":\"draw card\"," + draw_client.hand_json + ",\"draw_card\":\"" + card +"\"}")

    if len(finish_user) == 3:
        for i in users:
            for j in finish_user:
                if i.my_client['id'] == j.my_client['id']:
                    continue
            finish_user.append(i)
            break

        for i in range(len(finish_user)):
            print("rank %d : %d" % (i + 1, finish_user[i].my_client['id']))

        rankingStr = "[" + str(finish_user[0].my_client['id']) + "," + str(finish_user[1].my_client['id']) + "," + str(finish_user[2].my_client['id']) + "," + str(finish_user[3].my_client['id']) + "]"

        server.send_message_to_all("{\
                                        \"status\":\"true\",\
                                        \"message\":\"game finish\",\
                                        \"ranking\":" + rankingStr + "\
                                    }")
        return

    update_order()

def draw_card(server, client):
    for i in users:
        if i.my_client == client:
            draw_user = i

    for i in users:
        if draw_user.next_user == i.my_client:
            drawn_user = i

    draw_card = drawn_user.drawn_hand()
    draw_user.update_hand(draw_card)

    send_result(server, draw_user, drawn_user, draw_card)


def client_left(client, server):
    print("lient(%d), disconnected" % client['id'])

PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
