import logging
from ftplib import FTP, error_perm

# Configure logging
logging.basicConfig(
    filename="ftp_client.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ftp_client():
    host = "192.xxx.xx.129"
    user = "ftpxxxx"
    passwd = "Aaaaaa@xxxx"

    try:
        ftp = FTP(host)
        ftp.login(user=user, passwd=passwd)
        print("Connected to FTP server")
        logging.info("Connected to FTP server at %s", host)

        # List directory
        print("\nDirectory Listing:")
        ftp.retrlines("LIST")
        logging.info("Listed directory contents")

        # Upload a file
        with open("upload.txt", "w") as f:
            f.write("Hello FTP, test from Windows client.")
        with open("upload.txt", "rb") as f:
            ftp.storbinary("STOR upload/upload.txt", f)
        print("\nFile uploaded successfully")
        logging.info("File 'upload.txt' uploaded to 'upload/upload.txt'")

        # Download a file
        with open("downloaded.txt", "wb") as f:
            ftp.retrbinary("RETR upload/serverfile.txt", f.write)
        print("File downloaded successfully (saved as downloaded.txt)")
        logging.info("File 'upload/serverfile.txt' downloaded as 'downloaded.txt'")

        ftp.quit()
        logging.info("Connection closed")

    except error_perm as e:
        print("FTP permission error:", e)
        logging.error("FTP permission error: %s", e)

    except Exception as e:
        print("FTP client error:", e)
        logging.error("FTP client error: %s", e)

if __name__ == "__main__":
    ftp_client()
