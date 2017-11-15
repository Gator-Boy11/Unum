#import net_scanner as netscan
_VERSION_ = "1.0.2"
import socket
from time import sleep
import os

os.system("color 0A")
print("Welcome to the Unum Client Version " + _VERSION_ + ", enter a server address to begin.")

server_addr = input("IP Address: ")

master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master.connect((server_addr, 4242))

print("Connected")

while True:
    command_type = master.recv(2)
    if command_type == b'\0m':
        message = ""
        char = master.recv(1)
        while char != b'\0':
            message = message + char.decode("ascii")
            char = master.recv(1)
        print(message)
        sleep(0.01)
        master.send(("\0"*64).encode("ascii"))
    elif command_type == b'\0a':
        message = input(":")
        if message == "":
            message = "\0b"
        master.send(message.encode("ascii"))
    else:
        print(command_type)
    
