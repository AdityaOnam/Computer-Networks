import requests
import logging

logging.basicConfig(
    filename="http_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def show_response(r):
    print("Status:", r.status_code)
    print("Headers:", dict(r.headers))
    print("Body:", r.text)
    logging.info(f"Response {r.status_code}: {r.text[:200]}")

def get_request(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        show_response(r)
    except Exception as e:
        logging.error(f"GET {url} failed: {e}")
        print("GET failed:", e)

def post_request(url, data=None):
    try:
        r = requests.post(url, json=data, timeout=10)
        show_response(r)
    except Exception as e:
        logging.error(f"POST {url} failed: {e}")
        print("POST failed:", e)

if __name__ == "__main__":
    base_url = "http://192.xxx.xx.129:5000"

    print("\n--- Sending GET Request ---")
    get_request(f"{base_url}/get", {"name": "Aditya", "task": "http-client"})

    print("\n--- Sending POST Request ---")
    post_request(f"{base_url}/post", {"objective": "application layer", "date": "29-08-2025"})
