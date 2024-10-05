import socket
 

# Define the host port 
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 6969


# socket.AF_INET  -> signfice  the Internet Protocol v4 
# socket.AF_INET6 -> signfice the Internet Protocol v6
# socket.SOCK_STREAM -> it signfice the TCP protocl 
# socket.SOCK_DGRAM  -> socket to use the UDP socket


#? Info: start with IP4 and TCP protocol 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Now we are changing some default behaviour of our server 

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind server with it's resource simply with the computer
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(5)

print(f'Listening on port {SERVER_PORT} ...') 

while True:
    client_socket, client_address = server_socket.accept()

    request = client_socket.recv(1500).decode()

    print(request)


    header = request.split("\n")
    first_header_component = header[0].split()

    if( first_header_component[0] == "GET"):
        content = "<h1> No Content <h1>"
        if (first_header_component[1] == "/"):
            content = open("one.html", "r").read()
        else: 
            break 
 
        response = 'HTTP/1.1 200 OK\n\n' + content
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'



    client_socket.sendall(response.encode())


    client_socket.close()


server_socket.close()
    