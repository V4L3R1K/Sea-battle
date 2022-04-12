# what client can do in network
import network
import threading
import time

SERVER_ADDR = "192.168.1.9"
SERVER_PORT = 60000

s = network.socket.socket()
s.settimeout(network.DISCONNECT_TIMEOUT)
alive = False


def keepAlive():
    while alive:
        network.sendCode(s, network.KEEP_ALIVE)
        time.sleep(network.DISCONNECT_TIMEOUT-1)


def connect(addr=SERVER_ADDR, port=SERVER_PORT):
    global alive
    alive = True
    s.connect((addr, port))
    keepAliveThread.start()
    return network.OK


def disconnect():
    global alive
    alive = True
    keepAliveThread.join()
    s.close()
    return network.OK


def signUp(login, password):
    network.sendCode(s, network.SIGN_UP)
    network.send(s, login)
    network.send(s, password)
    code = network.recvCode(s)
    return code


def signIn(login, password):
    network.sendCode(s, network.SIGN_IN)
    network.send(s, login)
    network.send(s, password)
    code = network.recvCode(s)
    return code


def signOut():
    network.sendCode(s, network.SIGN_OUT)
    code = network.recvCode(s)
    return code


keepAliveThread = threading.Thread(target=keepAlive())
