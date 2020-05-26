#!/usr/bin/env python3

from socket import *
from threading import Thread
import tkinter as tkt
import sys

#ip and mac of this client
client_ip = "01.05.10.30"
client_mac = "44:BF:5B:DA:11:AC"
#ip and mac of the router
router_ip = "01.05.10.01"
router_mac = "32:03:0A:DA:11:DC"

BUFSIZ = 1024
#connection to the router
router = ('localhost', 8300)
#making the socket relative of this client
client_socket = socket(AF_INET, SOCK_STREAM)
#connects it to the router
client_socket.connect(router)

''' the purpose of this function is to register the client to the specified router.
The latter will record its ip and mac and forwards the information to the server,
that keeps track of the online/offline clients '''
def join():
    message = "join"
    destination_ip = router_ip
    send_packet(client_ip, client_mac, destination_ip, router_mac, message)
    msg_list.insert(tkt.END, "hi IP: " + client_ip + ", welcome to the chat!")
    ''' once the client is connected, we start the thread responsible of the
    chat reception side '''
    Thread(target = chat_receive, daemon = False).start()


''' once pressed the enter button, this function reads the text of the textbox
and: sends the message to the specified client ip or quits the chat if we want to
close the window, advising the router that the same as before forwards the
information to the server '''
def chat_send():
    message = my_msg.get()
    if message != "quit": 
        destination_ip = variable.get()
        msg_list.insert(tkt.END, "to [" + destination_ip + "]: " + message) 
        send_packet(client_ip, client_mac, destination_ip, router_mac, message)
    else:
        destination_ip = router_ip
        send_packet(client_ip, client_mac, destination_ip, router_mac, message)        
        client_socket.close()
        window.quit()


''' each message arrives from:
- another user
- the server that advise the client the inability to deliver the message to the
specified ip '''
def chat_receive():
    while True:
        try:
            message = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END, message[0:11] + ": " + message[56:BUFSIZ])
        except RuntimeError:  
            break

''' this function builds the packet (header + message) and sends it to the router '''
def send_packet(source_ip, source_mac, destination_ip, destination_mac, msg):
    #we build the header of the packet
    IP_header = source_ip + destination_ip
    ethernet_header = source_mac + router_mac
    #packet is composed of the header + the data to send
    packet = IP_header + ethernet_header + msg
    #we send the packet to the router
    client_socket.send(bytes(packet, "utf8")) 

def on_closing(event=None):
    my_msg.set("quit")
    chat_send()

''' GUI '''
window = tkt.Tk()
window.title("Chat")

#frame that will contain the messages
messages_frame = tkt.Frame(window)

#variable of string type to send messages
my_msg = tkt.StringVar()
#we denote where the user must type the messages
my_msg.set("Write here your messages")
#scrollbar to navigate through the messages
scrollbar = tkt.Scrollbar(messages_frame)

#the following section contains the messages
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

OptionList = [ "92.10.10.15", 
        "92.10.10.20", 
        "92.10.10.25", 
        "01.05.10.15", 
        "01.05.10.20", 
        "01.05.10.30" ]

variable = tkt.StringVar()
#we set the default ip
variable.set(OptionList[0])

#option menu
opt = tkt.OptionMenu(window, variable, *OptionList)
#we integrate it into the packet
opt.pack()

#input field, tying it to the string variable
entry_field = tkt.Entry(window, textvariable = my_msg)
#we tie the chat_send function to the return key
entry_field.bind("<Return>", chat_send)

entry_field.pack()
#send button, connecting it to the chat_send function
send_button = tkt.Button(window, text = "Enter", command = chat_send)
#we integrate the key to the packet
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

#the thread starts once the connection is estabilished and the GUI appears
receive_thread = Thread(target = join, daemon = False)
receive_thread.start()
tkt.mainloop()
