#!/usr/bin/python3

import argparse
from urllib.parse import urlparse

Args = argparse.Namespace
REQUEST_TYPES = set(
    [
        "get",
        "post",
    ]
)


class Style:
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    CYAN = "\x1b[96m"
    RESET = "\033[0m"


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="vaccine", description="Check SQL injection vulnerabilites on a website"
    )
    parser.add_argument(
        "url",
        metavar="URL",
        type=str,
        help="URL to find SQL injection vulnerabilities",
    )
    parser.add_argument(
        "-o",
        metavar="log",
        type=str,
        default="vaccine.log",
        help="Archive file, if not specified it will be stored ina default one.",
    )
    parser.add_argument(
        "-X",
        metavar="request",
        type=str,
        default="GET",
        help="Type of request [GET/POST], if not specified GET will be used.",
    )
    return parser.parse_args()


def validate_args(args: Args) -> None:
    if not args.url.startwith("https://") and not args.url.startwith("http://"):
        args.url = "http://" + args.url
    parsed_url = urlparse(args.url)
    if not parsed_url.schema or not parsed_url.netloc:
        raise ValueError("Invalid URL. Please provide a valid URL")
    args.x = args.x.lower()
    if args.x not in REQUEST_TYPES:
        raise ValueError(f"Invalid request type {args.x}. Use only {REQUEST_TYPES}")


class Log:
    def __init__(self, filename):
        self.data = ""
        self.filename = filename

    def log(self, msg, color=""):
        if color:
            print(color + msg[:500] + Style.RESET)
        else:
            print(msg[:500])
        self.data = self.data + msg + "\n"

    def save(self):
        with open(self.filename, "w") as f:
            f.write(self.data)


class Vaccine:
    def __init__(self, url, method):
        self.url = url
        self.method = method


def main() -> None:
    try:
        args: Args = parse_args()
        validate_args(args)
        global logger
        logger = Log(args.o)
        vaccine = Vaccine(args.url, args.x)
        logger.save()
    except Exception as e:
        print(Style.RED + f"Error: {e}" + Style.RESET)
        exit(1)


if __name__ == "__main__":
    main()
