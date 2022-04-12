# socket operations
import socket

# codes
# request
SIGN_IN = 1
SIGN_UP = 2
SIGN_OUT = 3
KEEP_ALIVE = 4
# response
OK = 5
FAILED_TO_CONNECT = 6
WRONG_PASSWORD = 7
USER_ALREADY_SIGNED_IN = 8
USER_ALREADY_EXISTS = 9

HEADER = 4  # bytes

DISCONNECT_TIMEOUT = 5  # seconds


def send(conn: socket, data: str):
    conn.send(len(data).to_bytes(HEADER, "big"))  # how many bytes are in data
    conn.send(str(data).encode())  # the data itself


def recv(conn: socket) -> str:
    l = int.from_bytes(conn.recv(HEADER), "big")  # how many bytes are in data
    return conn.recv(l).decode()  # the data itself


def sendCode(conn: socket, code: int):
    conn.send(code.to_bytes(HEADER, "big"))


def recvCode(conn: socket) -> int:
    return int.from_bytes(conn.recv(HEADER), "big")
