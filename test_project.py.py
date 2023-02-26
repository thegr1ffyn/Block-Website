import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send an HTTP request to the proxy server
    request = 'GET http://www.youtube.com/ HTTP/1.1\r\nHost: www.youtube.com\r\n\r\n'
    sock.sendall(request.encode())

    # Receive the response from the proxy server
    response = b''
    while True:
        data = sock.recv(16)
        response += data
        if len(data) < 16:
            break

finally:
    # Clean up the connection
    sock.close()

# Print the response
print(response.decode())
