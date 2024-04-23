#Starter Code Taken from Lab 2 Tutorial

import socket

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      
            if data != b"":
                print(data)     
                client.sendall(data) 
    except: 
        print("Closing socket")
        client.close()
        s.close()    