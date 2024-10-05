from fudu_server.httpserver import HTTPServer

if __name__ == "__main__":
    server = HTTPServer(None, 4).work()


    while True:
        client_socket, client_address = server.accept()

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