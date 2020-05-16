#!/usr/bin/env python3

from socket import *
from threading import Thread
import tkinter as tkt
from sys import *

#ip and mac of this client
client_ip = "92.10.10.15"
client_mac = "32:04:0A:EF:19:CF"
#ip and mac of the router
router_ip = "92.10.10.1"
router_mac = "55:04:0A:EF:11:CF"

def join():
    message = "join"
    destination_ip = router_ip
    send()
    print("hi socket {socket}, welcome to the chat!\n".format(socket = client_socket.fileno()) 
    chat()

def chat():
    while True:
        IP_header = ""
        ethernet_header = ""
        message = input("Enter the message to send, or write quit to exit")
        if message != "quit": 
            destination_ip = input("Enter the IP of the client to send the message to:\n1. 92.10.10.15\n2. 92.10.10.20\n3. 92.10.10.25\n4. 1.5.10.15\n5. 1.5.10.20\n6. 1.5.10.30\n")
        else: 
            destination_ip = router_ip
        send()        
        try:
            #ricezione pacchetti dal router: messaggio da parte di un utente o da parte del server che comunica l'impossibiltà di invio di un messaggio all'ip specificato
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
        except OSError:  
            break

def send():
    #here we build the header of the packet
    IP_header = IP_header + client_ip + destination_ip
    ethernet_header = ethernet_header + client_mac + router_mac
    #packet is composed of the header + the data to send
    packet = IP_header + ethernet_header + message
    #we send the packet to the router
    client_socket.send(bytes(packet, "utf8")) 


BUFSIZ = 1024
#connection to the router
router = ('localhost', 12000)
#making the socket relative of this client
client_socket = socket(AF_INET, SOCK_STREAM)
#connects it to the router
client_socket.connect(router)

#the thread starts once the connection is estabilished
receive_thread = Thread(target = join)
receive_thread.start()

