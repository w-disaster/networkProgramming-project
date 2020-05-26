#!usr/bin/env python3

from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

#ip and mac of this router
router_ip = "92.10.10.01"
router_mac = "55:04:0A:EF:11:CF"
#ip and mac of the server
server_ip = "195.1.10.10"
server_mac = "52:AB:0A:DF:10:DC"

#arp table
arp_table_socket = {}
arp_table_mac = {}
BUFSIZ = 1024
#socket of the clients side
router_recv = socket(AF_INET, SOCK_STREAM)
router_recv.bind(("localhost", 8100))

#socket of the server side
router_send = socket(AF_INET, SOCK_STREAM)
router_send.bind(("localhost", 8200))

''' this functions once accepted a new client, starts the thread to manage it '''
def accept_client():
    while True:
        #we accept the client and assign to it a new socket
        client, address = router_recv.accept()
        #we start the thread: one foreach client
        Thread(target = manage_client, args = (client,), daemon = False).start()

''' this function connects the router to the server and starts the thread to manage it '''
def accept_server():
    server = ('localhost', 53000)
    #we connect the router to the server
    router_send.connect(server)
    #we start the thread for the server side
    Thread(target = manage_server, args = (router_send,), daemon = False).start()

''' this function manage the single client: we register it in the arp table if
has joined chat, we delete its coordinates if it's leaving, or we
forward the message to the server that is responsible to deliver the messages '''
def manage_client(client):
    while True:
        try:
            message = client.recv(BUFSIZ).decode("utf8")
            client_ip = message[0:11]
            client_mac = message[22:39]
            destination_ip = message[11:22]
            text = message[56:BUFSIZ]

            if text == "join":
                print("client with IP: " + client_ip + " connected to the router 1")
                #memorize the ip and mac of the accepted client
                arp_table_socket[client_ip] = client
                arp_table_mac[client_ip] = client_mac
                #we change the destination values to send the join packet to the server
                send_packet(client_ip, router_mac, server_ip, server_mac, text, router_send)

            elif text == "quit":
                print("client with IP: " + client_ip + " disconnected from the router 1")
                #warning server that this client is exiting the chat
                send_packet(client_ip, router_mac, server_ip, server_mac, text, router_send)
                #I pop the values of the exiting client
                arp_table_socket.pop(client_ip)
                arp_table_mac.pop(client_ip)
                #we close the socket
                client.close()
                return       
            else: 
                #the received packet from this client is a message to send to another user
                send_packet(client_ip, router_mac, destination_ip, server_mac, text, router_send)
        except OSError:
            router_send.close()
            router_recv.close()
            break

''' this function manage the packets from the server: if the destination ip is
in the arp table we forward the message, otherwise we do nothing '''
def manage_server(server):
    while True:
        try:
            msg = server.recv(BUFSIZ).decode("utf8")
            destination_ip = msg[11:22]
            if destination_ip in arp_table_socket:
                send_packet(msg[0:11], router_mac, destination_ip, arp_table_mac[destination_ip], msg[56:BUFSIZ], arp_table_socket[destination_ip])
        except OSError:
            router_send.close()
            router_recv.close()
            break

''' send packet function (same as the client scripts) '''
def send_packet(source_ip, source_mac, destination_ip, destination_mac, msg, socket):
    IP_header = source_ip + destination_ip
    ethernet_header = source_mac + destination_mac
    #making the packet and sending it
    packet = IP_header + ethernet_header + msg
    socket.send(bytes(packet, "utf8"))


if  __name__ == "__main__":
    try:
        #thread relative to the server socket
        server_thread = Thread(target = accept_server, daemon = False)
        server_thread.start()
        server_thread.join()

        #max 3 clients per router
        router_recv.listen(3)
        print("waiting for connections...")
        #starts a thread for each client
        client_thread = Thread(target = accept_client, daemon = False)
        client_thread.start()
        client_thread.join()
    except KeyboardInterrupt:
        router_recv.close()
        router_send.close()
