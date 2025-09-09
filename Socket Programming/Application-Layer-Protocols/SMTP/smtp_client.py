import smtplib
import logging
from email.message import EmailMessage

logging.basicConfig(
    filename="smtp_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_email(smtp_host, smtp_port, sender, recipient, username=None, password=None, use_tls=True):
    msg = EmailMessage()
    msg["Subject"] = "SMTP Test Email"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content("This is a test email sent via Python SMTP program.")

    try:
        logging.info(f"Connecting to SMTP server {smtp_host}:{smtp_port}")
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=20)
        server.set_debuglevel(1) 

        if use_tls:
            server.starttls()
            logging.info("Started TLS encryption")

        if username and password:
            server.login(username, password)
            logging.info("Logged in successfully")

        server.send_message(msg)
        logging.info("Email sent successfully")
        print("Email sent successfully")
        server.quit()

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print("Error:", e)

if __name__ == "__main__":
    send_email(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        sender="aditya308989@gmail.com",
        recipient="abc@gmail.com",
        username="xyzabc@gmail.com",
        password="uswp xxxx xxxx xxxx",
        use_tls=True
    )
    print("\nCheck smtp_activity.log for details.")
