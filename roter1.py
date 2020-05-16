#!usr/bin/env python3

from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

router_ip = "92.10.10.1"
router_mac = "55:04:0A:EF:11:CF"

server_ip = "195.1.10.10"
server_mac = "52:AB:0A:DF:10:DC"

arp_table_ip = {}
arp_table_mac = {}
BUFSIZ = 1024
#socket of the clients side
router_recv = socket(AF_INET, SOCK_STREAM)
router_recv.bind(("localhost", 8100))

#socket of the server side
router_send = socket(AF_INET, SOCK_STREAM)
router_send.bind(("localhost", 8200))

#this functions once that accept a new client, sends its coorinates (ip and mac address) to the server, warning it that a new client joined the chat
def accept_client():
    while True:
        #setting strings for join packet directed to server
        IP_header = ""
        ethernet_header = ""

        #we accept the client and assign to it a new socket
        client, address = router_recv.accept()
        #wait the ip and mac of the accepted client
        message = client.recv(BUFSIZ).decode("utf8")
        #memorize the ip and mac of the accepted client
        client_ip = message[0:11]
        client_mac = message[22:39]
        arp_table_ip[client] = client_ip
        arp_table_mac[client] = client_mac

        #we change the destination values to send the join packet to the server
        send_packet(client_ip, client_mac, server_ip, server_mac, message[57:BUFSIZ], router_send)

        #we start the thread: one foreach client
        Thread(target = manage_client, args = (client,)).start()

#this function manage the single client: now that it is connected to the router and registered in the server it can send messages to another user or quit the chat
def manage_client(client):
    
    message = client.recv(BUFSIZ).decode("utf8")
    if message[57:BUFSIZ] == "quit":
        #warning server that this client is exiting the chat
        send_packet(arp_table_ip[client], arp_table_mac[client], server_ip, server_mac, message[57:BUFSIZ])
        #we close the socket
        client.close()
   else:


def send_packet(source_ip, source_mac, destination_ip, destination_mac, msg, socket):
    IP_header = source_ip + destination_ip
    ethernet_header = source_mac + destination_mac
    #making the packet and sending it
    packet = IP_header + ethernet_header + msg
    socket.send(bytes(packet, "utf8"))



if  __name__ == "__main__":
    server_thread = Thread(target = connect_server)
    server_thread.start()
    server_thread.join()


    router_recv.listen(3)
    print("waiting for connections...")
    client_thread = Thread(target = accept_client)
    client_thread.start()
    client_thread.join()
    
    router_recv.close()
    router_send.close()
