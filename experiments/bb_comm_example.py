import socket

# if __name__ == '__main__':
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(('localhost', 5858))

if __name__ == '__main__':
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('localhost', 5858))
    # s.listen(5)
    # while VoteActive:
    #     # accept connections from outside
    #     (clientsocket, address) = s.accept()
    #     # now do something with the clientsocket
    #     # in this case, we'll pretend this is a threaded server
    #     print(address)

    # Wait For EB to make it self visible
    me = 'bb'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    waitingForVoteStart = True
    while waitingForVoteStart:
        try:
            s.connect(('localhost', 5858))
            waitingForVoteStart = False
        except socket.error:
            continue
    x = s.recv(4096)
    print('rec' + x)
    s.close()
