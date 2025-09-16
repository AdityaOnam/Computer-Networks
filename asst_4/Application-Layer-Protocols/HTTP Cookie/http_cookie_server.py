import socket

HOST = "127.0.0.1"
PORT = 8081

def handle_client(conn):
    request = conn.recv(1024).decode()
    print("=== Client Request ===")
    print(request)

    if "Cookie:" in request:
        cookie_line = [line for line in request.split("\r\n") if line.startswith("Cookie:")][0]
        cookie_value = cookie_line.split(":", 1)[1].strip()

        response_body = f"<html><body><h1>Welcome back, {cookie_value}!</h1></body></html>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n"
            f"{response_body}"
        )
    else:
        cookie_value = "User123"
        response_body = f"<html><body><h1>Hello, new visitor! Your session: {cookie_value}</h1></body></html>"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Set-Cookie: session={cookie_value}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n"
            f"{response_body}"
        )

    conn.sendall(response.encode())
    conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Serving on http://{HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(conn)


if __name__ == "__main__":
    start_server()
