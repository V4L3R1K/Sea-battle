# main server file
import hashlib
import time
import threading

import network

SERVER_ADDR = network.socket.gethostbyname(network.socket.gethostname())
SERVER_PORT = 60000

alive = True

clientsAlive = {}
users = []


def generatePasswordHash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def handleClient(conn, addr):
    global clientsAlive
    global users
    userLogin = None
    print(addr[0]+":"+str(addr[1])+" connected")
    while clientsAlive[addr]-time.time() > 0:
        code = network.recvCode(conn)
        if code != 0:
            if code == network.SIGN_UP:
                login = network.recv(conn)
                passwordHash = generatePasswordHash(network.recv(conn))
                ok = True
                for user in users:
                    if user["login"] == login:
                        network.sendCode(conn, network.USER_ALREADY_EXISTS)
                        ok = False
                        break
                if ok:
                    users.append(
                        {"login": login, "passwordHash": passwordHash, "online": True})
                    userLogin = login
                    network.sendCode(conn, network.OK)
                    print(addr[0]+":"+str(addr[1]) +
                          " "+userLogin+" signed up")
            elif code == network.SIGN_IN:
                login = network.recv(conn)
                passwordHash = generatePasswordHash(network.recv(conn))
                ok = False
                for user in users:
                    if user["login"] == login and user["passwordHash"] == passwordHash:
                        ok = True
                        if user["online"] == True:
                            network.sendCode(
                                conn, network.USER_ALREADY_SIGNED_IN)
                        else:
                            user["online"] = True
                            userLogin = login
                            network.sendCode(conn, network.OK)
                            print(addr[0]+":"+str(addr[1]) +
                                  " "+userLogin+" signed in")
                        break
                if not ok:
                    network.sendCode(conn, network.WRONG_PASSWORD)
            elif code == network.SIGN_OUT:
                if userLogin != None:
                    for user in users:
                        if user["login"] == userLogin:
                            user["online"] = False
                            userLogin = None
                            network.sendCode(conn, network.OK)
                            print(addr[0]+":"+str(addr[1]) +
                                  " "+user["login"]+" signed out")
            clientsAlive[addr] = time.time()+network.DISCONNECT_TIMEOUT
    for user in users:
        if user["login"] == userLogin:
            user["online"] = False
            network.sendCode(conn, network.OK)
            print(addr[0]+":"+str(addr[1]) +
                  " "+userLogin+" signed out")
    print(addr[0]+":"+str(addr[1])+" disconnected")


s = network.socket.socket(network.socket.AF_INET, network.socket.SOCK_STREAM)
s.bind((SERVER_ADDR, SERVER_PORT))
s.listen()

print("Server started at "+str(SERVER_ADDR)+":"+str(SERVER_PORT))
while alive:
    conn, addr = s.accept()
    clientsAlive.update({addr: time.time()+network.DISCONNECT_TIMEOUT})
    clientThread = threading.Thread(target=handleClient(conn, addr))
    clientThread.start()
