#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#ip and mac of the server
server_ip = "195.1.10.10"
server_mac = "52:AB:0A:DF:10:DC"

BUFSIZ = 1024
#dictionary for connected routers and clients respectively
routers_mac = {}
connected_clients = {}

''' this function accept a new router and starts a thread relative to it '''
def accept_router():
    while True:
        #we accept the connection for incoming router
        router, router_addr = server.accept()
        print("connection with router %s:%s estabilished" % router_addr)
        routers_mac[router] = ""
        #we start the thread: one for each router
        Thread(target = manage_router, args = (router,)).start()

''' once a router is accepted, this function registers its socket and mac (we will 
need them to broadcast a message), then, according to the packet type, we register/
delete the client to/from the dictionary, or we forward the message broadcasting
it to all the connected routers, that delivers it if the recipient is connected
on to its network.  '''
def manage_router(router):
    while True:
        message = router.recv(BUFSIZ).decode("utf8")
        client_ip = message[0:11]
        destination_ip = message[11:22]
        router_mac = message[22:39]
        text = message[56:BUFSIZ]
        
        #we memorize the router mac to build the ethernet header if will be necessary to send a packet to it
        if routers_mac[router] == "":
            routers_mac[router] = router_mac
        
        #we check the content of the packet
        if text == "join":
            connected_clients[client_ip] = "active"
            print("client with ip: " + client_ip +" joined the chat")
        elif text == "quit":
            connected_clients[client_ip] = "disconnected"
            print("client with ip: " + client_ip + " has left the chat")
        else:
            #this is a message to send to another user: if it is active we send it, otherwise we advise the sender that has left the chat
            if destination_ip in connected_clients and connected_clients[destination_ip] == "active":
                IP_header = client_ip + destination_ip
                broadcast(IP_header, text)
            else:
                #server advise the sender that the client is inactive
                IP_header = server_ip + client_ip
                text = "user with IP: {ip_address} is not online".format(ip_address = destination_ip)
                broadcast(IP_header, text)


''' this function sends a message to all the routers connected to the server '''
def broadcast(IP_header, text):
    for router in routers_mac:
        ethernet_header = server_mac + routers_mac[router]
        packet = IP_header + ethernet_header + text
        router.send(bytes(packet, "utf8"))


if __name__ == "__main__":
    #we define the server socket and its port
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('localhost', 53000))

    #the server can manage 2 routers
    server.listen(2)
    print("waiting for connections...")
    server_thread = Thread(target = accept_router, daemon = False)
    server_thread.start()
    server_thread.join()

    server.close()
