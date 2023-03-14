import os
from dotenv import load_dotenv
from pathlib import PurePath
from ftplib import FTP
import time

load_dotenv()

BASE_PATH = PurePath(os.getenv("BASE_PATH"))

FTP_HOST = os.getenv("FTP_HOST")
FTP_FOLDER = os.getenv("FTP_FOLDER")


def retrieve_file(ftp, file_to_retrieve):
    write_file_path = BASE_PATH.joinpath(file_to_retrieve)

    print(f"[{file_to_retrieve}] Downloading...")

    with open(write_file_path, "wb") as file:
        response = ftp.retrbinary(f"RETR {file_to_retrieve}", file.write)
        print(f"[{file_to_retrieve}] {response}")
        print()


def list_files(ftp):
    lines = []
    ftp.retrlines("LIST", lines.append)

    files = []
    for line in lines:
        if not line.startswith("d"):
            file = line.split()[-1]
            files.append(file)

    return files


if __name__ == "__main__":
    start_time = time.time()

    with FTP(FTP_HOST) as ftp:
        ftp.login()

        ftp.cwd(FTP_FOLDER)

        files = list_files(ftp)
        for file in files:
            retrieve_file(ftp, file)

    duration = time.time() - start_time
    print(f"{duration} seconds")
