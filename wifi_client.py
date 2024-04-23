#Starter Code Taken from Lab 2 Tutorial
import socket

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        text = input("Enter your message: ")
        if text == "quit":
            break
        s.send(text.encode()) 

        data = s.recv(1024)
        print("from server: ", data)