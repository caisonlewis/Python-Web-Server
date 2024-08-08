import re
import socket
from pathlib import Path

# 1 or more of ANY character, a dot, followed by a file extension
html_file_pattern = re.compile(r'^.+\.(html|htm|css)$', re.ASCII | re.IGNORECASE)


def do_get_file_resource(resource:str):
    '''
    The purpose of this method is to make sure the file requested is valid and return it as a response
    :param resource: the name of the file being requested by the client
    :return: on HTTP response containing the file, or an error
    '''
    # resource should be something like: /hacker.html
    # or: /
    if resource == "/":
        filename = "index.html"
    else:
        filename = resource[1:]


    if html_file_pattern.match(filename):
        path = Path(filename)
        if path.is_file():
            with open(path) as infile:
                html_data = infile.read()
                return  "HTTP/1.0 200 OK\n\n" + html_data



    pass

# resource should be something like /hacker.html
def handle_get(resource:str):
    return do_get_file_resource(resource)


HOST = '127.0.0.1'  # '0.0.0.0'
PORT = 9999

def main():
    # Create a new socket that by default uses TCP/IP
    with socket.socket() as s:
        # Tells the OS to reuse the socket if we restart the program
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print("Listening at:", s.getsockname())

        while True:
            # Wait for clients to connect
            client_connection, client_address = s.accept()
            print("Client address:", client_address)

            # Get the client request
            request = client_connection.recv(1024)

            # default encoding used is utf-8
            print(request.decode())
            # GET /hacker.html HTTP/1.1

            lines = request.splitlines() # creates list of each line from the string
            #lines[0] = GET /hacker.html HTTP/1.1

            # check for empty set
            if lines == [] or len(lines[0].split()) != 3:
                response = "HTTP/1.0 404 Skill Issue\n\n"
            else:
                # Request-line = Method, resource, http ver.
                request_line = lines[0]
                method, resource, protocol = request_line.split()

                #all webservers should handle GET and HEAD
                if method == "GET":
                    response = handle_get(resource)
                else:
                    response = "HTTP/1.0 501 Seeking Top\n\n"

            # Send HTTP response
            # 1) Status Line
            # 2) Headers (optional)
            # 3) Empty Line
            # 4) Response body (optional)
            # status_line = "HTTP/1.0 200 OK\n\n"
            # body = "Hello to you! Your IP is " + str(client_address[0])
            # response = status_line + body

            # default encoding used is utf-8
            client_connection.sendall(response.encode())
            client_connection.close()



if __name__ == "__main__":
    main()