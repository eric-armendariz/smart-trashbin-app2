#Starter Code Taken from Lab 2 Tutorial

import socket
from main import *

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          


def is_trashcan_full():
    # Check if the bin is consistently full (over 10 checks)
    info = [distance_bin_level() < 10 for _ in range(10)]
    return all(info)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("Server received from:", client_info)
            data = client.recv(1024).decode()
            if data == "BIN_STATUS":
                # Determine if the bin is full
                status = "FULL" if is_trashcan_full() else "NOT FULL YET"
                client.sendall(status.encode()) 
            client.close()
                
    except: 
        print("Closing socket")
        client.close()
        s.close()    
