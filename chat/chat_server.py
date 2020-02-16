import socket
import select               #importing select allows me to manage multiple connections and removes the problem of the code working on a specific O.S.


#here we define constants that we will use throughout the code here 
HEADER_LENGHT = 10
IP = "127.0.0.1"
PORT = 1234


def socket_server_setup():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #af stands for address family
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #this allows us to reconnect without needing to change the server number
    server_socket.bind((IP, PORT))
    server_socket.listen()
    return server_socket

sockets = socket_server_setup()
sockets_list = [sockets]        #the list fo clients, but we need to bare in mind that here they are sockets 

#here we create a clients dict and we will set it up in a way that they client socket will be the key and the user data will be the value 

clients = {}       

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGHT)

        #this is a case where we didnt get any data, this means the client could have closed the connection 
        
        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {
            "header": message_header,
            "data": client_socket.recv(message_length),
            }

    except:
        return False

#inside this loop we make use of the select function, that function takes in 3 parameters
# 1.) the list we are going to read from
#  2.) the list we are going to write to 
# 3.) sockets that we might have errors on 

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == sockets:
            client_socket, client_address = sockets.accept()

            user = recieve_message(client_socket)

            #if someone just disconnects from the chat 
            if user is False:
                continue
                
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = recieve_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            #here we share the message with everyone 

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]