import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 5858))

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 5858))
    s.listen(5)
    while True:
        # accept connections from outside
        (clientsocket, address) = s.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a threaded server
        print(address)
