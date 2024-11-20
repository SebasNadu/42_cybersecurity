#! /usr/bin/env python3

import argparse

# import time
# import hashlib
# import base64
# import qrcode
# import hmac
# import struct

Args = argparse.Namespace
Parser = argparse.ArgumentParser


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


def main():
    args: Args = parse_args()
    try:
        if args.g is not None:
            pass
        if args.k is not None:
            pass
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}")


if __name__ == "__main__":
    main()
