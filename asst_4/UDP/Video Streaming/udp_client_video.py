import cv2
import socket
import numpy as np
import signal
import sys

CLIENT_IP = "192.168.xx.xxx"  
CLIENT_PORT = 9999
ADDR = (CLIENT_IP, CLIENT_PORT)
CHUNK_SIZE = 1400    


def signal_handler(sig, frame):
    print("\nClient stopped by user.")
    sock.close()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)

print(f"Client listening on {CLIENT_IP}:{CLIENT_PORT}")

frame_buffer = bytearray()

while True:
    try:
        packet, _ = sock.recvfrom(CHUNK_SIZE + 1)
    except KeyboardInterrupt:
        signal_handler(None, None)

    if not packet:
        continue


    marker = packet[0]
    chunk = packet[1:]
    frame_buffer.extend(chunk)

    if marker == 1: 
        try:
            np_data = np.frombuffer(frame_buffer, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

            if frame is not None:
                cv2.imshow("UDP Video Stream", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                print("Frame decode failed, skipping...")

        except Exception as e:
            print(f"Error decoding frame: {e}")

        frame_buffer = bytearray()

sock.close()
cv2.destroyAllWindows()
print("Client stopped.")
