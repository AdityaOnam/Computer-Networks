import socket
import dns.resolver
import logging

logging.basicConfig(
    filename="dns_queries.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def resolve_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"IP Address of {domain}: {ip}")
        logging.info(f"IP of {domain}: {ip}")
    except Exception as e:
        print("Failed to resolve IP:", e)
        logging.error(f"IP resolution failed for {domain}: {e}")

def get_records(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        print(f"{record_type} records for {domain}:")
        for r in answers:
            print("   ", r.to_text())
            logging.info(f"{record_type} record for {domain}: {r.to_text()}")
    except Exception as e:
        print(f"Failed to fetch {record_type} records:", e)
        logging.error(f"{record_type} lookup failed for {domain}: {e}")

if __name__ == "__main__":
    domain = "www.google.com"

    resolve_ip(domain)
    get_records(domain, "A")
    get_records(domain, "MX")
    get_records(domain, "CNAME")

    print("\nCheck dns_queries.log for saved query results.")
