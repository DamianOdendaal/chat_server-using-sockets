import socket
import select 
import errno      #this will be used in the code so that we can get detailed errors so that we know exactly what is wrong when something is wrong 
import sys


HEADER_LENGHT = 10

IP = "127.0.0.1"
PORT = 1234

def get_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    return client_socket

def get_username():
    my_username = input("Username: ")
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGHT}}".encode('utf-8')
    client_socket = get_client_socket()
    client_socket.send(username_header + username)


    #here we are going to be sending messages
    while True:
        message = input(f"{my_username} > ")

        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGHT}}".encode('utf-8')
            client_socket.send(message_header + message)
            
            #here we are going to be recieving things until we hit an error
        try:
            while True:
                
                username_header = client_socket.recv(HEADER_LENGHT)
                #if we didnt recieve any message at all
                
                if not len(username_header):
                    print("connection closed by the server")
                    sys.exit()

                #here we want to convert the username header to an int 
                username_lenght = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_lenght).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGHT)
                message_lenght = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_lenght).decode('utf-8')
                
                print(f"{username} > {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != e.errno.EWOULDBLOCK:
                print('Reading error',str(e))
                sys.exit()
            continue


        except Exception as e:
            print('General error', str(e) )
            sys.exit()
get_username()

#dont forget to call the function later in your code 
