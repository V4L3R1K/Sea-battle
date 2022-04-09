# main server file
import hashlib
import time
import threading

import network

SERVER_ADDR = network.socket.gethostbyname(network.socket.gethostname())
SERVER_PORT = 60000

DISCONNECT_TIMEOUT = 5  # seconds

alive = True

clientsAlive = {}


def handleClient(conn, addr):
    print(addr[0]+":"+str(addr[1])+" connected")
    while clientsAlive[addr]-time.time() > 0:
        code = network.recvCode(conn)
        if code != 0:
            print(addr, code)
            clientsAlive[addr] = time.time()+DISCONNECT_TIMEOUT
    print(addr[0]+":"+str(addr[1])+" disconnected")


s = network.socket.socket(network.socket.AF_INET, network.socket.SOCK_STREAM)
s.bind((SERVER_ADDR, SERVER_PORT))
s.listen()

print("Server started at "+str(SERVER_ADDR)+":"+str(SERVER_PORT))
while alive:
    conn, addr = s.accept()
    clientsAlive.update({addr: time.time()+DISCONNECT_TIMEOUT})
    clientThread = threading.Thread(target=handleClient(conn, addr))
    clientThread.start()
