#!/usr/bin/env python

import argparse
import pathlib
import re
import os
import requests
from urllib.parse import ParseResult, urljoin, urlparse
from urllib import robotparser
from bs4 import BeautifulSoup, ResultSet
from typing import Optional


DEFAULT_DEPTH = 5
DEFAULT_PATH = "./data"
EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
USER_AGENT = "42SpiderBot"

total_downloads: int = 0


class color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Images Spider")
    parser.add_argument("URL", type=str, help="URL to extract all the images")
    parser.add_argument(
        "-r",
        "--recursive",
        help="Recursively download images in URL",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        help="Indicates the max depth level in the seach (default 5)",
        dest="depth",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        help="Path to store the images (default ./data/)",
        default="./data/",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose mode",
    )
    args: argparse.Namespace = parser.parse_args()
    if args.depth is None:
        if args.recursive:
            args.depth = DEFAULT_DEPTH
        else:
            args.depth = 1
    elif args.depth and not args.recursive:
        parser.error("argument -l | --level: expect -r | --recursive argument.")
    args.current_depth = 0
    return args


def print_args(args: argparse.Namespace):
    def format_line(text: str) -> str:
        ansi_len = (text.count(color.INFO) + text.count(color.RESET)) * len(color.INFO)
        return f"*{text:^{77 + (ansi_len)}}*"

    print("{:*^80}".format(""))
    print(format_line(f"URL: {color.INFO}{args.URL}{color.RESET}"))
    if args.recursive:
        print(
            format_line(
                f"Scraping recursively to depth level: {color.INFO}{args.depth}{color.RESET}"
            )
        )
    print(
        format_line(
            f"Saving images to directory: {color.INFO}{str(args.path)}{color.RESET}"
        )
    )
    print("{:*^80}".format(""))


def check_url(url: str) -> None:
    result: ParseResult = urlparse(url)
    if not result.scheme:
        raise Exception("URL must have a scheme such as http or https")
    if not result.netloc:
        raise Exception("no network location for URL")
    if result.scheme != "https" and result.scheme != "http":
        raise Exception("URL scheme must be http or https")


def validate_url(args: argparse.Namespace) -> None:
    try:
        check_url(args.URL)
    except Exception as e:
        if not re.match("^[a-z]*://", args.URL):
            args.URL = "http://" + args.URL
            validate_url(args)
        else:
            raise Exception(f"{args.URL}: invalid URL: {e}")


def check_robots(url: str, verbose: bool = False) -> None:
    path_to_check: str = urlparse(url).path
    base_url: str = urlparse(url).scheme + "://" + urlparse(url).netloc
    robots_url: str = base_url + "/robots.txt"
    parser: robotparser.RobotFileParser = robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception as e:
        raise Exception(f"Error reading {robots_url}: {e}")
    fetchable: bool = parser.can_fetch(USER_AGENT, path_to_check)
    if not fetchable:
        raise Exception(robots_url + " forbids path: " + path_to_check)
    if verbose:
        print(f"{color.SUCCESS}URL robots.txt OK: {robots_url}{color.RESET}")


def get_content(url: str, verbose: bool = False) -> bytes:
    check_robots(url, verbose)
    res: requests.Response = requests.get(
        url, headers={"User-Agent": USER_AGENT}, timeout=5
    )
    res.raise_for_status()
    if verbose:
        print(f"{color.SUCCESS}URL OK ({res.status_code} response): {url}{color.RESET}")
    return res.content


def url_connection(args: argparse.Namespace):
    validate_url(args)
    get_content(args.URL, True)


def create_storage_dir(args: argparse.Namespace) -> None:
    if not os.path.exists(args.path):
        print(f"Creating directory: {args.path.resolve()}")
        os.makedirs(args.path)
    elif not os.path.isdir(args.path):
        raise Exception(args.path.name + ": not a directory.")
    elif not os.access(args.path, os.W_OK) or not os.access(args.path, os.X_OK):
        raise Exception(args.path.name + ": Permision denied.")
    print(f"{color.SUCCESS}Save directory OK: {args.path.resolve()}{color.RESET}")


def print_visiting_header(url: str, depth: int) -> None:
    print("{:*^80}".format(""))
    print(
        f"[Depth: {color.INFO}{depth}{color.RESET}] Visiting URL: {color.INFO}{url}{color.RESET}"
    )
    print("{:*^80}".format(""))


def get_full_url(base_url: str, path: str) -> str:
    parse: ParseResult = urlparse(path)
    if not parse.netloc:
        return urljoin(base_url, parse.path)
    elif not parse.scheme:
        return "http://" + parse.netloc + parse.path
    return parse.scheme + "://" + parse.netloc + parse.path


def download_image(image_url: str, storage_dir: str) -> int:
    global total_downloads
    image_name: str = os.path.basename(image_url)
    save_path: str = os.path.join(storage_dir, image_name)
    try:
        if os.path.exists(save_path):
            raise Exception(f"The image already exist in {storage_dir} directory.")
        content: bytes = get_content(image_url)
        with open(save_path, "wb") as f:
            f.write(content)
            total_downloads += 1
            print(f"{color.SUCCESS}Downloaded image: {save_path}{color.RESET}")
            return 1
    except Exception as e:
        print(f"{color.WARNING}Skipping: {image_name}: {e}.{color.RESET}")
        return 0


def get_images_from_tag(
    args: argparse.Namespace, url: str, soup: BeautifulSoup
) -> None:
    image_count: int = 0
    download_count: int = 0
    image_tags: ResultSet = soup.find_all("img")
    for image_tag in image_tags:
        image_path: str = image_tag.get("src")
        image_ext: str = os.path.splitext(image_path)[-1]
        if image_ext.lower() not in EXTENSIONS:
            continue
        image_count += 1
        image_url: str = get_full_url(url, image_path)
        if args.verbose:
            print(f"Downloading: {image_url}...")
        download_count += download_image(image_url, args.path)
    print(
        f"Downloaded {color.INFO}{download_count}{color.RESET} of {color.INFO}{image_count}{color.RESET} images from {color.INFO}{url}{color.RESET}"
    )


def get_link_from_href(base_url: str, href: str, urls: set[str]) -> Optional[str]:
    if not href:
        return None
    link: str = get_full_url(base_url, href)
    if link in urls or link == base_url:
        return None
    parse_base_url: ParseResult = urlparse(base_url)
    parse_link_url: ParseResult = urlparse(link)
    if parse_base_url.netloc != parse_link_url.netloc:
        return None
    return link


def get_links(url: str, soup: BeautifulSoup) -> set[str]:
    urls: set[str] = set()
    hrefs: ResultSet = soup.find_all("a")
    for h in hrefs:
        href: str = h.get("href")
        link: str | None = get_link_from_href(url, href, urls)
        if not link or link is None:
            continue
        else:
            urls.add(link)
    return urls


def scrape_images(
    args: argparse.Namespace,
    url: str,
    visited_urls: set = set(),
    current_depth: int = 0,
    download_count: int = 0,
) -> None:
    if current_depth >= args.depth:
        return
    if url in visited_urls:
        return
    visited_urls.add(url)
    print_visiting_header(url, current_depth)
    try:
        content: bytes = get_content(url)
        soup: BeautifulSoup = BeautifulSoup(content, "html.parser")
        get_images_from_tag(args, url, soup)
        if current_depth + 1 < args.depth:
            links: set[str] = get_links(url, soup)
            print(f"Discovered {color.INFO}{len(links)}{color.RESET} links in URL")
            for link in links:
                scrape_images(
                    args, link, visited_urls, current_depth + 1, download_count
                )
    except Exception as e:
        print(f"{color.ERROR}Skipping URL: {e}{color.RESET}")


def print_result(args: argparse.Namespace) -> None:
    global total_downloads
    print("")
    print("{:*^80}".format(""))
    print(
        "TOTAL:{:>83}".format(
            f"{color.INFO}{total_downloads}{color.RESET} images downloaded"
        )
    )
    print("SAVE DIR:{:>80}".format(f"{color.INFO}{args.path.resolve()}{color.RESET}"))
    print("{:*^80}".format(""))


def spider(args: argparse.Namespace) -> None:
    try:
        url_connection(args)
        create_storage_dir(args)
        scrape_images(args, args.URL)
        print_result(args)
    except KeyboardInterrupt:
        print_result(args)
        exit(130)
    except Exception as e:
        print(f"{color.ERROR}spider.py: error: {e}{color.RESET}")
        print_result(args)


# parse arguments
# check url and permissions
def main() -> None:
    args: argparse.Namespace = parse_args()
    print_args(args)
    spider(args)


if __name__ == "__main__":
    main()
