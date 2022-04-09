# socket operations
import socket

# codes
# request
SIGN_IN = 0
SIGN_UP = 1
SIGN_OUT = 2
KEEP_ALIVE = 3
# response
OK = 4
FAILED_TO_CONNECT = 5
BAD_PASSWORD = 6
USER_ALREADY_SIGNED_IN = 7
USER_ALREADY_EXISTS = 8

HEADER = 4  # bytes


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
