import socket

# -----------------------------
# This is a simple server program
# It listens for a client connection on a specific port
# Once a client connects it receives the clients name and number
# Then it asks the server user to enter a number
# After that it sends the server name and number back to the client
# Finally it prints the details of the exchange
# -----------------------------

# Name that the server will use when talking to the client
name = "XYZ"

# Create a socket for the server
# socket.AF_INET means IPv4 addressing
# socket.SOCK_STREAM means TCP protocol which is connection based
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the socket to be reused quickly after program restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server socket to a specific IP address and port number
server_socket.bind(('10.xx.x.xxx', 9999))

# Start listening for incoming client connections
server_socket.listen()

print("Server is listening on port 9999")

while True:
    # Accept a client connection
    # conn represents the connection object
    # addr represents the client address
    conn, addr = server_socket.accept()
    print(f"\nConnected by {addr}")

    # Wrap the connection in a file like object so that we can read line by line
    connfile = conn.makefile('r', encoding='utf-8')

    # Read the client name sent by the client
    cname = connfile.readline().strip()

    # Read the client number sent as text and strip newline
    line = connfile.readline().strip()
    try:
        # Convert the client number into an integer
        cval = int(line)
    except:
        # If conversion fails use an invalid number
        cval = -1

    # Check if the received number is valid
    # If not then close everything and stop the server
    if not (1 <= cval <= 100):
        print("Invalid number received Closing server")
        connfile.close()
        conn.close()
        server_socket.close()
        break

    # Ask the server user to enter a number
    # Keep asking until a valid number is entered
    val = 0
    while True:
        num = int(input("Enter a number between 1 and 100: "))
        val = num
        if 1 <= num <= 100:
            break

    # Print details of the exchange
    print(f"Client Name: {cname}")
    print(f"Server Name: {name}")
    print(f"Client Number: {cval}")
    print(f"Server Number: {val}")
    print(f"Sum: {cval + val}")

    # Send the server name to the client
    conn.sendall((name + "\n").encode())

    # Send the server number to the client
    conn.sendall((str(val) + "\n").encode())

    # Close the file like object and the client connection
    connfile.close()
    conn.close()
