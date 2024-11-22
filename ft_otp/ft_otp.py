#! /usr/bin/env python3

import argparse
import os
import time

import hashlib
import base64
import hmac
from cryptography.fernet import Fernet
import qrcode

# from PIL import Image

Args = argparse.Namespace
Parser = argparse.ArgumentParser

default_key_file = "ft_otp.key"
time_step = 30
issuer = "ft_otp"
email = "ft_otp@example.com"


class Color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


HEADER = """
@@@@@@@@  @@@@@@@                  @@@@@@   @@@@@@@   @@@@@@@  
@@@@@@@@  @@@@@@@                 @@@@@@@@  @@@@@@@@  @@@@@@@  
@@!         @@!                   @@!  @@@  @@!  @@@    @@!    
!@!         !@!                   !@!  @!@  !@!  @!@    !@!    
@!!!:!      @!!                   @!@  !@!  @!@@!@!     @!!    
!!!!!:      !!!                   !@!  !!!  !!@!!!      !!!    
!!:         !!:                   !!:  !!!  !!:         !!:    
:!:         :!:                   :!:  !:!  :!:         :!:    
 ::          ::    :::::::::::::  ::::: ::   ::          ::    
 :           :     :::::::::::::   : :  :    :           :     
                                                               
"""


def parse_args() -> Args:
    parser: Parser = argparse.ArgumentParser(
        prog="pt_otp",
        description="Generates a one time password that expires after 30 secs from a 64 hex key",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--generate",
        type=str,
        metavar="HEX FILE",
        help="generates a .key file from a 64 hex string",
    )
    group.add_argument(
        "-k",
        "--key",
        type=str,
        metavar="KEY FILE",
        help="Generate a one time password that expires after 30 secs from a .key file",
    )
    parser.add_argument(
        "-q",
        "--qrcode",
        action="store_true",
        help="Generates a QR code for the key, compatible with Google Authenticator",
    )
    group.required = True
    return parser.parse_args()


def validate(key: str) -> None:
    try:
        if len(key) < 64:
            raise ValueError("key lenght is less than 64 characters")
        int(key, 16)
    except ValueError as e:
        raise Exception(f"{e}")
    except Exception as e:
        raise Exception(f"key must be 64 hexadecimal characters. {e}")


def get_master_key(key_file="master.key"):
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        master_key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(master_key)
        print(f"Master key was generated and saved in {key_file}")
        return master_key


def generate_secret_key(key_file):
    try:
        with open(key_file, "r") as file:
            content = file.read().strip()
        validate(content)
        seed = get_master_key()
        fernet = Fernet(seed)
        encrypted_key = fernet.encrypt(content.encode())
        encoded = base64.b32encode(encrypted_key).decode()
        with open(default_key_file, "w") as file:
            file.write(encoded)
        print("Key was saved in ft_opt.key")
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}{Color.RESET}")


def generate_otp(key_file):
    try:
        with open(key_file, "r") as file:
            secret = file.read()
        seed = get_master_key()
        fernet = Fernet(seed)
        secret_decoded = base64.b32decode(secret)
        secret_decrypted = fernet.decrypt(secret_decoded).decode()
        secret = bytes.fromhex(secret_decrypted)

        timestamp = time.time()
        N = int(timestamp // time_step)
        time_key = N.to_bytes(8, "big")

        hmac_sha1 = hmac.new(secret, time_key, hashlib.sha1)
        hmac_sha1_bytes = hmac_sha1.digest()
        offset = hmac_sha1_bytes[-1] & 0xF
        chosen_bytes = hmac_sha1_bytes[offset : offset + 4]
        new_bin_value = (
            ((chosen_bytes[0] & 0x7F) << 24)
            + ((chosen_bytes[1] & 0xFF) << 16)
            + ((chosen_bytes[2] & 0xFF) << 8)
            + ((chosen_bytes[3] & 0xFF))
        )
        token = new_bin_value % 10**6
        token = f"{token:0>6}"
        print(f"OPT: [{token}]")
    except Exception as e:
        print(f"Error: {e}")


def generate_qr_code(key_file, label=f"totp:{email}", issuer=f"{issuer}"):
    try:
        with open(key_file, "r") as file:
            secret = file.read()
        seed = get_master_key()
        fernet = Fernet(seed)
        secret_decoded = base64.b32decode(secret)
        secret_decrypted = fernet.decrypt(secret_decoded).decode()
        secret_bytes = bytes.fromhex(secret_decrypted)
        base32_secret = base64.b32encode(secret_bytes).decode("utf-8")

        uri = f"otpauth://totp/{label}?secret={base32_secret}&issuer={issuer}"
        qr = qrcode.QRCode()
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.show()
        print("QR Code generated and displayed. Scan it with Google Authenticator.")
    except Exception as e:
        print(f"Error generating QR Code: {e}")


def main():
    args: Args = parse_args()
    try:
        if args.generate is not None:
            generate_secret_key(args.generate)
        if args.key is not None:
            generate_otp(args.key)
            if args.qrcode:
                generate_qr_code(args.key)
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}")


if __name__ == "__main__":
    main()
