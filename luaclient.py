import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))

while True:
    message = raw_input('lua> ')
    sock.send(message)
    a = sock.recv(4096)
    print(a)


sock.close()
