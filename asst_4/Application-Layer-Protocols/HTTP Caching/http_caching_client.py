import http.client

HOST = "localhost"
PORT = 8080
PATH = "index.html"

def fetch_resource(etag=None, last_modified=None):
    conn = http.client.HTTPConnection(HOST, PORT)
    
    headers = {}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified

    conn.request("GET", PATH, headers=headers)
    response = conn.getresponse()

    print(f"Status: {response.status} {response.reason}")
    for header, value in response.getheaders():
        print(f"{header}: {value}")
    print()

    if response.status == 200:
        body = response.read().decode()
        print("Body received:")
        print(body)
        return dict(response.getheaders())
    else:
        return dict(response.getheaders())

# First request (no cache headers → should return 200 OK with file)
print("=== First Request ===")
headers = fetch_resource()

# Second request (send ETag + Last-Modified → should return 304 Not Modified)
print("=== Second Request with caching headers ===")
fetch_resource(
    etag=headers.get("ETag"),
    last_modified=headers.get("Last-Modified")
)
