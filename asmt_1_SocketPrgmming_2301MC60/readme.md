🔌 Socket Programming in Python

📌 Overview

This project demonstrates basic socket programming in Python using the TCP protocol
It contains two main scripts

server.py → Runs a TCP server that waits for client connections

client.py → Runs a client that connects to the server and exchanges data

Both sides send their name and a number between 1 and 100 then calculate the sum

📂 Project Structure
socket-programming/
│
├── client.py       # Client side script
├── server.py       # Server side script
└── README.md       # Documentation

🚀 How It Works
Server Flow

1 Starts a TCP socket and listens on a chosen IP and port
2 Waits for a client connection
3 Receives client name and number
4 Prompts the server user to enter a number
5 Sends server name and number to client
6 Prints exchange details

Client Flow

1 Connects to server via TCP
2 Sends client name and number
3 Receives server name and number
4 Prints exchange details and the sum
5 Option to continue or exit

▶️ Usage
1 Start the Server

Run the server script on one machine

python server.py


Output

Server is listening on port 9999
Connected by ('10.xx.x.xxx', 54321)

2 Start the Client

Run the client script on the same network

python client.py


Client input

Enter a number between 1 and 100: 25


Server input

Enter a number between 1 and 100: 40

Example Client Output
Client Name: Onam
Server Name: ABC
Client Number: 25
Server Number: 40
Sum: 65

⚠️ Notes

Replace 10.xx.x.xxx in both scripts with the actual server IP

Both devices must be connected to the same network

The port 9999 must be available and open

Entering an invalid number outside 1 to 100 will close the connection

🛠️ Requirements

Python 3.x

Works on Windows Linux Mac