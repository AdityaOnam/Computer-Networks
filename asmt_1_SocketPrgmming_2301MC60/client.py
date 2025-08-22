import socket

# -----------------------------
# This is a simple client program
# It connects to a server and sends a name and a number
# Then it receives the servers name and number
# Finally it prints the sum of both numbers
# -----------------------------

# Name that this client will use when talking to the server
client_name = "Onam"

while True:
    try:
        # Ask the user for a number between 1 and 100
        # We use int to make sure the input is stored as a number not as text
        number = int(input("Enter a number between 1 and 100: "))

        # Check if the number is valid
        # If it is less than or equal to 1 or greater than or equal to 100
        # we stop the program because the rules are not followed
        if number <= 1 or number >= 100:
            print("Invalid number Connection closed")
            break

        # Create a socket to connect to the server
        # socket.AF_INET means we are using IPv4
        # socket.SOCK_STREAM means we are using TCP protocol which is connection based
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server at the given IP address and port number
        client_socket.connect(('10.xx.x.xxx', 9999))
        print("Connected to server on port 9999")

        # Send the clients name first
        # We add a newline character so that the server can know where the line ends
        # encode is used to convert text into bytes which is required for sending
        client_socket.sendall((client_name + "\n").encode())

        # Send the chosen number to the server
        client_socket.sendall((str(number) + "\n").encode())

        # Now we will read the response sent back by the server
        # makefile allows us to treat the socket like a file so we can read line by line
        sockfile = client_socket.makefile('r', encoding='utf-8')

        # First line from server is the servers name
        server_name = sockfile.readline().strip()

        # Second line from server is the servers chosen number converted from text to integer
        server_number = int(sockfile.readline().strip())

        # Show the details of the exchange in a clear format
        print("\n--- Exchange Details ---")
        print(f"Client Name: {client_name}")
        print(f"Server Name: {server_name}")
        print(f"Your Number: {number}")
        print(f"Server Number: {server_number}")
        print(f"Sum: {number + server_number}")
        print("---------------------------\n")

        # Close the file like object and the socket connection
        sockfile.close()
        client_socket.close()

        # Ask the user if they want to continue and send another number
        again = input("Do you want to continue (y/n): ").strip().lower()

        # If the answer is not y then end the program
        if again != "y":
            print("Session ended Goodbye")
            break
        else:
            # If user wants to continue just print a line for clarity
            print("\n")

    except ValueError:
        # If the user typed something that cannot be converted to an integer
        # Show this message and let them try again
        print("Please enter a valid integer")
