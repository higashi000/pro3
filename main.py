from websocket_server import WebsocketServer
import random
import json
import player

users = []
client_list = []
now_player = ""

card = ["01a", "02a", "03a", "04a", "05a", "06a", "07a", "08a", "09a", "10a", "11a", "12a", "13a",
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
    now_player = users[0].my_client['id']

    for i in users:
        print("{\"status\":\"true\",\"message\":\"game start\"," + i.hand_json + "}")
        server.send_message(i.my_client, "{\"status\":\"true\",\"message\":\"game start\"," + i.hand_json + "}")


def check_order(client):
    print("now_player = %d" % now_player)
    if client['id'] == now_player:
        return True
    else:
        return False

def update_order():
    global now_player
    for i in users:
        if i.my_client['id'] == now_player:
            now_player = i.next_user['id']
            return

def new_client(client, server):
    if len(client_list) < 4:
        client_list.append(client)
        server.send_message(client, "{\"status\":\"true\",\"message\":\"successful connect\"}")
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
            draw_card(client)
            update_order()
        else:
            server.send_message(client, "{\"status\":\"false\",\"message\":\"There is not it in order of you\"}")

def draw_card(client):
    for i in users:
        if i.my_client == client:
            draw_user = i

    for i in users:
        if draw_user.next_user == i.my_client:
            drawn_user = i

    draw_card = drawn_user.drawn_hand()
    draw_user.draw_card(draw_card)


def client_left(client, server):
    print("lient(%d), disconnected" % client['id'])

PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
