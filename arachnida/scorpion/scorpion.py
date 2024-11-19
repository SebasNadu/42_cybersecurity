import argparse
import pathlib
from PIL import Image, ExifTags
import humanize
import time
import stat
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

HEADER = """
 @@@@@@    @@@@@@@   @@@@@@   @@@@@@@   @@@@@@@   @@@   @@@@@@   @@@  @@@  
@@@@@@@   @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@@@@@@  @@@@ @@@  
!@@       !@@       @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@!  @@@  @@!@!@@@  
!@!       !@!       !@!  @!@  !@!  @!@  !@!  @!@  !@!  !@!  @!@  !@!!@!@!  
!!@@!!    !@!       @!@  !@!  @!@!!@!   @!@@!@!   !!@  @!@  !@!  @!@ !!@!  
 !!@!!!   !!!       !@!  !!!  !!@!@!    !!@!!!    !!!  !@!  !!!  !@!  !!!  
     !:!  :!!       !!:  !!!  !!: :!!   !!:       !!:  !!:  !!!  !!:  !!!  
    !:!   :!:       :!:  !:!  :!:  !:!  :!:       :!:  :!:  !:!  :!:  !:!  
:::: ::    ::: :::  ::::: ::  ::   :::   ::        ::  ::::: ::   ::   ::  
:: : :     :: :: :   : :  :    :   : :   :        :     : :  :   ::    :   
                                                                           
"""
SEPARATOR = "-" * 80


class Color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


def print_header() -> None:
    for line in HEADER.splitlines():
        print(Color.HEADER + "{:^80}".format(line) + Color.RESET)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image metadata viewer and editor")
    parser.add_argument("image", type=pathlib.Path, nargs="+", help="Images to process")
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete all EXIF metadata"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    return parser.parse_args()


def build_stripped_file_name(image_path: pathlib.Path) -> pathlib.Path:
    return image_path.with_name(image_path.stem + ".stripped" + image_path.suffix)


def strip_image_metadata(image_path: pathlib.Path, verbose: bool) -> None:
    try:
        with Image.open(image_path) as source:
            stripped = Image.new(source.mode, source.size)
            stripped.putdata(list(source.getdata()))
            save_path = build_stripped_file_name(image_path)
            stripped.save(save_path)
            if verbose:
                logging.info(
                    f"Stripped metadata from {Color.SUCCESS}{image_path} -> {save_path}{Color.RESET}"
                )
    except Exception as e:
        logging.warning(
            f"{Color.ERROR}Failed to process {image_path}: {e}{Color.RESET}"
        )


def extract_basic_file_info(image_path: pathlib.Path) -> dict:
    if not image_path.exists():
        raise FileNotFoundError("File does not exist")
    stats = image_path.stat()
    return {
        "Filename": image_path.name,
        "Size": humanize.naturalsize(stats.st_size, binary=True),
        "Creation Date": time.ctime(stats.st_ctime),
        "Modification Date": time.ctime(stats.st_mtime),
        "Permissions": stat.filemode(stats.st_mode),
    }


def extract_image_metadata(image_path: pathlib.Path, verbose: bool) -> dict:
    metadata = {}
    try:
        metadata = extract_basic_file_info(image_path)
        with Image.open(image_path) as img:
            metadata.update(
                {
                    "Format": img.format,
                    "Mode": img.mode,
                    "Image Width": img.width,
                    "Image Height": img.height,
                }
            )
            exif_data = img.getexif()
            metadata["EXIF"] = {
                ExifTags.TAGS.get(tag, tag): value
                for tag, value in exif_data.items()
                if isinstance(value, str) or verbose
            }
    except Exception as e:
        logging.warning(
            f"{Color.ERROR}Could not read metadata from {image_path}: {e}{Color.RESET}"
        )
    return metadata


def print_metadata(metadata: dict) -> None:
    for key, value in metadata.items():
        if key == "EXIF":
            print(f"{key}:")
            for exif_key, exif_value in value.items():
                print(f"  {exif_key:30}: {exif_value}")
        else:
            print(f"{key:30}: {value}")


def process_images(args: argparse.Namespace) -> None:
    if args.delete:
        print(SEPARATOR)
        print(f"{Color.WARNING}Deleting metadata{Color.RESET}")
        print(SEPARATOR)
    for image_path in tqdm(args.image, desc="Processing images"):
        if args.delete:
            strip_image_metadata(image_path, args.verbose)
        else:
            metadata = extract_image_metadata(image_path, args.verbose)
            if not metadata:
                continue
            print(SEPARATOR)
            print(f"Metadata for {Color.SUCCESS}{image_path}{Color.RESET}:")
            print(SEPARATOR)
            print_metadata(metadata)
            print(SEPARATOR)


def main() -> None:
    print_header()
    args = parse_args()
    process_images(args)


if __name__ == "__main__":
    main()
