import socket
from comm_test import Comm


# import socket               # Import socket module

# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# port = 12345                # Reserve a port for your service.

# s.connect((host, port))
# print s.recv(1024)
# s.close                     # Close the socket when done

# if __name__ == '__main__':
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(('localhost', 5858))




if __name__ == '__main__':


    # send first msg in handshake


    # msg = json.dumps({ ''})
    print s.recv(4096)
    s.close()
