import cv2
import socket
import time
import math

CLIENT_IP = "192.168.xx.xxx"
CLIENT_PORT = 9999
ADDR = (CLIENT_IP, CLIENT_PORT)

VIDEO_SOURCE = 0

CHUNK_SIZE = 1400

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


cap = cv2.VideoCapture(VIDEO_SOURCE)
if not cap.isOpened():
    print(f"Warning: failed to open VIDEO_SOURCE={VIDEO_SOURCE}. Trying webcam (0).")
    cap = cv2.VideoCapture(0) # Webcam

if not cap.isOpened():
    raise RuntimeError("ERROR: Could not open any video source (file or webcam).")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0 or math.isnan(fps):
    fps = 25.0
frame_interval = 1.0 / fps

print(f"Streaming to {CLIENT_IP}:{CLIENT_PORT} (CHUNK_SIZE={CHUNK_SIZE}) -- FPS={fps:.2f}")


frame_count = 0
try:
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("End of video / failed to read frame. Stopping.")
            break

        frame = cv2.resize(frame, (640, 480))

        success, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not success:
            print("Warning: frame encoding failed, skipping this frame.")
            continue
        data = encoded.tobytes()

        num_chunks = math.ceil(len(data) / CHUNK_SIZE)
        if num_chunks == 0:
            continue

        for i in range(num_chunks):
            start = i * CHUNK_SIZE
            end = start + CHUNK_SIZE
            chunk = data[start:end]
            marker = 1 if i == num_chunks - 1 else 0
            packet = marker.to_bytes(1, "big") + chunk

            try:
                sock.sendto(packet, ADDR)
            except OSError as e:
                print(f"Send error: {e}. Continuing...")

        frame_count += 1
        
        if frame_count % 30 == 0:
            print(f"Sent frames: {frame_count}  (last frame size: {len(data)} bytes split in {num_chunks})")

        elapsed = time.time() - start_time
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nInterrupted by user. Stopping stream...")

finally:
    cap.release()
    sock.close()
    print("Streaming stopped. Resources released.")
