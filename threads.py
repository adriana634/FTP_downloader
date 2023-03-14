import os
from dotenv import load_dotenv
from pathlib import PurePath
from ftplib import FTP
import concurrent.futures
import time

load_dotenv()

MAX_WORKERS = 5
BASE_PATH = PurePath(os.getenv('BASE_PATH'))

FTP_HOST = os.getenv('FTP_HOST')
FTP_FOLDER = os.getenv('FTP_FOLDER')

def list_files():
    with FTP(FTP_HOST) as ftp:
        ftp.login()

        ftp.cwd(FTP_FOLDER)

        lines = []
        ftp.retrlines("LIST", lines.append)

        files = []
        for line in lines:
            if not line.startswith("d"):
                file = line.split()[-1]
                files.append(file)
        return files


def retrieve_file(file_to_retrieve):
    with FTP(FTP_HOST) as ftp:
        ftp.login()

        ftp.cwd(FTP_FOLDER)

        write_file_path = BASE_PATH.joinpath(file_to_retrieve)

        print(f"[{file_to_retrieve}] Downloading...")

        with open(write_file_path, "wb") as file:
            response = ftp.retrbinary(f"RETR {file_to_retrieve}", file.write)
            print(f"[{file_to_retrieve}] {response}")
            print()


def retrieve_files(files):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(retrieve_file, files)


if __name__ == "__main__":
    start_time = time.time()

    files = list_files()
    retrieve_files(files)

    duration = time.time() - start_time
    print(f"{duration} seconds")
