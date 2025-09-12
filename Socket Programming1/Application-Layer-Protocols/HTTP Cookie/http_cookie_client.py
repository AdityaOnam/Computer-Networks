import socket

HOST = "127.0.0.1"
PORT = 8081

def send_request(cookie=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        request = "GET / HTTP/1.1\r\n"
        request += f"Host: {HOST}\r\n"
        if cookie:
            request += f"Cookie: {cookie}\r\n"
        request += "Connection: close\r\n\r\n"

        client_socket.sendall(request.encode())
        response = client_socket.recv(4096).decode()

    print("=== Server Response ===")
    print(response)
    print()
    return response


def main():
    # First request (no cookie)
    response1 = send_request()

    cookie = None
    for line in response1.split("\r\n"):
        if line.startswith("Set-Cookie:"):
            cookie = line.split(":", 1)[1].strip()
            break

    # Second request (with cookie)
    if cookie:
        print("=== Sending second request with stored cookie ===")
        send_request(cookie)


if __name__ == "__main__":
    main()
