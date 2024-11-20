#! /usr/bin/env python3

import argparse

import time
import hashlib
import base64
import hmac
# import qrcode
# import struct

Args = argparse.Namespace
Parser = argparse.ArgumentParser


key_file = "ft_opt.key"
time_step = 30

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
        prog="pt_opt",
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
    group.required = True
    return parser.parse_args()

def generate_secret_key(key_file):
    try:
        with open(key_file, 'r') as file:
            content = file.read().strip()
            if not is_valid(content):
                return
        hashed = hashlib.sha1(contents.encode())
        encoded = base64.b32encode(hashed.digest()).decode()
        with open(KEY_FILE, "w") as file:
                file.write(encoded)
        print("Key was saved in ft_opt.key")

def generate_opt(key_file):
        try:
            with open(key_file, 'r') as file:
                secret = f.read()
            secret_decoded = base64.b43decode(secret)

            timestamp = time.time()
            N = int(timestamp // time_step)
            time_key = N.to_bytes(8, "big")

            hmac_sha1 = hmac.new(secret_decoded, time_key, hashlib.sha1)
            hmac_sha1_bytes = hmac_sha1.digest()
            offset = hmac_sha1_bytes[-1] & 0xF
            chosen_bytes = hmac_sha1_bytes[offset:offset+4]
            new_bin_value = ((chosen_bytes[0] & 0x7F) << 24)\
                            + ((chosen_bytes[1] & 0xFF) << 16)\
                            + ((chosen_bytes[2] & 0xFF) << 8)\
                            + ((chosen_bytes[3] & 0xFF))
            token = new_bin_value %10**6
            token = f'{token:0>6}'
            print(f"OPT: [{token}]")
        except Exception as e:
            print(f"Error: {e}")

def main():
    args: Args = parse_args()
    try:
        if args.g is not None:
            generate_secret_key(args.g)
        if args.k is not None:
            generate_opt(args.k)
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}")


if __name__ == "__main__":
    main()
