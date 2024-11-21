#!/usr/bin/env python3

import argparse
import pathlib
import os
import requests
from urllib.parse import urljoin, urlparse
from urllib import robotparser
from bs4 import BeautifulSoup
from typing import Set
from tqdm import tqdm  # For progress visualization

# Constants
DEFAULT_DEPTH = 5
DEFAULT_PATH = "./data"
EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
USER_AGENT = "42SpiderBot"
MAX_IMAGE_SIZE_MB = 5  # Skip images larger than 5MB

HEADER = """
 @@@@@@   @@@@@@@   @@@  @@@@@@@   @@@@@@@@  @@@@@@@   
@@@@@@@   @@@@@@@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
!@@       @@!  @@@  @@!  @@!  @@@  @@!       @@!  @@@  
!@!       !@!  @!@  !@!  !@!  @!@  !@!       !@!  @!@  
!!@@!!    @!@@!@!   !!@  @!@  !@!  @!!!:!    @!@!!@!   
 !!@!!!   !!@!!!    !!!  !@!  !!!  !!!!!:    !!@!@!    
     !:!  !!:       !!:  !!:  !!!  !!:       !!: :!!   
    !:!   :!:       :!:  :!:  !:!  :!:       :!:  !:!  
:::: ::    ::        ::   :::: ::   :: ::::  ::   :::  
:: : :     :        :    :: :  :   : :: ::    :   : :  
                                                       
"""

# Global variables
total_downloads: int = 0


# Colors for terminal output
class Color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


def print_header() -> None:
    for line in HEADER.splitlines():
        print(Color.HEADER + "{:^70}".format(line) + Color.RESET)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Images Spider")
    parser.add_argument("URL", type=str, help="URL to extract images from")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recursively download images"
    )
    parser.add_argument(
        "-l", "--level", default=5, type=int, help="Max depth for recursive search (default 5)"
    )
    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        default="./data",
        help="Directory to save images",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def validate_url(url: str) -> str:
    """Ensure URL is valid and has a scheme."""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid URL: Missing domain or IP address.")
    return url


def validate_save_path(path: pathlib.Path) -> None:
    """Ensure the save directory is valid."""
    if path.exists() and not path.is_dir():
        raise ValueError(f"{path} exists but is not a directory.")
    path.mkdir(parents=True, exist_ok=True)


def check_robots_txt(url: str) -> None:
    """Check the site's robots.txt for permissions."""
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    robots_url = f"{base_url}/robots.txt"
    parser = robotparser.RobotFileParser()
    parser.set_url(robots_url)
    parser.read()
    if not parser.can_fetch(USER_AGENT, url):
        raise PermissionError(f"Access to {url} is disallowed by robots.txt")


def fetch_content(url: str) -> bytes:
    """Fetch content from a URL."""
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.content


def save_image(url: str, save_dir: pathlib.Path) -> bool:
    """Download and save an image."""
    global total_downloads
    image_name = os.path.basename(urlparse(url).path)
    save_path = save_dir / image_name

    if save_path.exists():
        print(f"{Color.WARNING}Image already exists: {save_path}{Color.RESET}")
        return False

    try:
        content = fetch_content(url)
        size_mb = len(content) / (1024 * 1024)
        if size_mb > MAX_IMAGE_SIZE_MB:
            print(
                f"{Color.WARNING}Skipping large image ({size_mb:.2f} MB): {url}{Color.RESET}"
            )
            return False

        with open(save_path, "wb") as file:
            file.write(content)
        total_downloads += 1
        print(f"{Color.SUCCESS}Image downloaded: {save_path}{Color.RESET}")
        return True
    except Exception as e:
        print(f"{Color.ERROR}Failed to download {url}: {e}{Color.RESET}")
        return False


def extract_images(url: str, soup: BeautifulSoup, save_dir: pathlib.Path) -> int:
    """Extract and download images from a page."""
    images = soup.find_all("img")
    download_count = 0

    for img in tqdm(images, desc="Processing Img"):
        src = img.get("src")
        if not src:
            continue
        full_url = urljoin(url, src)
        ext = os.path.splitext(full_url)[-1].lower()
        if ext in EXTENSIONS:
            if save_image(full_url, save_dir):
                download_count += 1

    return download_count


def extract_links(url: str, soup: BeautifulSoup, visited: Set[str]) -> Set[str]:
    """Extract unique links from a page."""
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = urljoin(url, a_tag["href"])
        if href not in visited and urlparse(href).netloc == urlparse(url).netloc:
            links.add(href)
    return links


def scrape(
    url: str, depth: int, save_dir: pathlib.Path, visited: Set[str], verbose: bool
) -> None:
    """Recursively scrape a website for images."""
    if depth < 0 or url in visited:
        return
    visited.add(url)

    try:
        print(f"{Color.INFO}Scraping: {url}{Color.RESET}")
        content = fetch_content(url)
        soup = BeautifulSoup(content, "html.parser")

        download_count = extract_images(url, soup, save_dir)
        print(f"{Color.INFO}Downloaded {download_count} images from {url}{Color.RESET}")

        if depth > 0:
            links = extract_links(url, soup, visited)
            for link in tqdm(links, desc="Processing links"):
                scrape(link, depth - 1, save_dir, visited, verbose)

    except Exception as e:
        print(f"{Color.ERROR}Error scraping {url}: {e}{Color.RESET}")


def main():
    print_header()
    try:
        args = parse_arguments()
        args.URL = validate_url(args.URL)
        check_robots_txt(args.URL)
        validate_save_path(args.path)
        scrape(
            url=args.URL,
            depth=args.level if args.recursive else 0,
            save_dir=args.path,
            visited=set(),
            verbose=args.verbose,
        )
    except KeyboardInterrupt:
        print(f"{Color.WARNING}\nInterrupted by user.{Color.RESET}")
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}{Color.RESET}")
    finally:
        print(f"{Color.SUCCESS}Total images downloaded: {total_downloads}{Color.RESET}")


if __name__ == "__main__":
    main()
