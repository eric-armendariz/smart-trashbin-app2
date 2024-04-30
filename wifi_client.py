#Starter Code Taken from Lab 2 Tutorial
import socket

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send("BIN_STATUS".encode()) 

    data = s.recv(1024).decode()
    print("Trash can status", data)
