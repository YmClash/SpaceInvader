import socket
import threading


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)


server =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

print(ADDR)

def handle_client(conn,addr):
    print(f" New Connexion {addr} connected")

    connected = True
    while connected:
        msg = conn.recv()

    pass

def start():
    server.listen()
    while True:
        conn,addr = server.accept()
        thread = threading.Thread
    pass


def stop():
    pass



