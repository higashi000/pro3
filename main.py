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

def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")


def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))

PORT=9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
