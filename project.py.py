import socket
import re

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Set of sites to block
blocked_sites = {'www.youtube.com', 'www.facebook.com'}

# Cache of responses
response_cache = {}

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        request = b''
        while True:
            data = connection.recv(16)
            request += data
            if len(data) < 16:
                break

        # Parse the request to get the hostname
        hostname = re.search(b'Host: (.*?)\r', request).group(1).decode()
        print('request for hostname:', hostname)

        # Check if the hostname is in the blocked sites set
        if hostname in blocked_sites:
            print('access to', hostname, 'is blocked')
            connection.close()
            continue

        # Check if we have a cached response for this hostname
        if hostname in response_cache:
            print('serving cached response for', hostname)
            connection.sendall(response_cache[hostname])
            continue

        # Forward the request to the destination server
        destination_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_sock.connect((hostname, 80))
        destination_sock.sendall(request)

        # Receive the response from the destination server
        response = b''
        while True:
            data = destination_sock.recv(16)
            response += data
            if len(data) < 16:
                break

        # Cache the response
        response_cache[hostname] = response

        # Return the response to the client
        connection.sendall(response)

    finally:
        # Clean up the connection
        connection.close()
