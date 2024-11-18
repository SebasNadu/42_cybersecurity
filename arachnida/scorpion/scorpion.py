import argparse
import pathlib
from PIL import Image, ExifTags
import os
import typing
import humanize
import time
import stat


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
SEPARATOR = "{:70}".format("-------")


class color:
    HEADER = "\033[36m"
    INFO = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    RESET = "\033[0m"


def print_header() -> None:
    for line in HEADER.splitlines():
        print(color.HEADER + "{:^70}".format(line) + color.RESET)


def parse_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Image metada viewer"
    )
    parser.add_argument(
        "image", type=pathlib.Path, nargs="+", help="image to view EXIF data for."
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="delete all exif data",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="enable verbose mode",
    )
    args: argparse.Namespace = parser.parse_args()
    return args


def print_deleting_metadata_header() -> None:
    print("{:-^80}".format(""))
    print("Deleting metadata")
    print("{:-^80}".format(""))


def print_deleting_image_metadata(
    args: argparse.Namespace, image_number: int, image: pathlib.PosixPath, save: str
) -> None:
    print(
        f"[{color.INFO}{image_number}{color.RESET}/{len(args.image)}] Deleting metadata for image: {color.INFO}{image.resolve()}{color.RESET}"
    )
    print(
        f"Saving stripped image as: {color.INFO}{os.path.basename(save)}{color.RESET}"
    )
    print("")


def build_stripped_file_name(image_path: pathlib.PosixPath) -> str:
    dir: str = os.path.dirname(image_path.resolve())
    ext: str = os.path.splitext(image_path)[-1]
    name: str = os.path.splitext(image_path)[-2] + ".stripped"
    return dir + "/" + name + ext


def strip_image_metadata(
    args: argparse.Namespace, image_path: pathlib.PosixPath, index: int
) -> None:
    try:
        with Image.open(image_path) as source:
            data: list = list(source.getdata())
            stripped: Image.Image = Image.new(source.mode, source.size)
            stripped.putdata(data)
            save_name: str = build_stripped_file_name(image_path)
            stripped.save(save_name)
            print_deleting_image_metadata(args, index, image_path, save_name)
    except Exception as e:
        print(f"{color.WARNING}Skipping image: {e}{color.RESET}")


def print_image_metadata_header(
    args: argparse.Namespace, image_number: int, image: pathlib.Path
) -> None:
    print("{:-^80}".format(""))
    print(
        f"[{color.INFO}{image_number}{color.RESET}/{len(args.image)}] Metadata for image: {color.INFO}{image}{color.RESET}"
    )
    print("{:-^80}".format(""))


def extract_basic_file_info(
    image_path: pathlib.Path, metadata: dict[str, typing.Any]
) -> None:
    metadata["Filename"] = os.path.basename(image_path)
    metadata["Directory"] = os.path.dirname(image_path.resolve())
    metadata["File Size"] = humanize.naturalsize(
        os.path.getsize(image_path), binary=True
    )
    metadata["Creation Date"] = time.ctime(os.path.getctime(image_path))
    metadata["Modification Date"] = time.ctime(os.path.getmtime(image_path))
    metadata["File Permissions"] = stat.filemode(os.stat(image_path).st_mode)


def extract_basic_image_info(
    image: Image.Image, metadata: dict[str, typing.Any]
) -> None:
    metadata["Format"] = image.format
    metadata["Mode"] = image.mode
    metadata["Image Width"] = image.width
    metadata["Image Height"] = image.height


def add_separator(metadata: dict[str, typing.Any]) -> None:
    metadata[SEPARATOR] = SEPARATOR


def extract_image_exif(image: Image.Image, metadata: dict[str, Image.Image]) -> None:
    exifdata: typing.Any = image.getexif()
    for tag_id, value in exifdata.items():
        tag: str = ExifTags.TAGS.get(tag_id, tag_id)
        metadata[tag] = value


def print_metadata_value(key: str, value: typing.Any, verbose: bool = False) -> None:
    if verbose and (isinstance(value, str) or isinstance(value, bytes)):
        if isinstance(value, str) and not value.isprintable():
            value = repr(value)
    print(f"{key:30}: {value}")


def print_image_metadata(
    metadata: dict[str, typing.Any], verbose: bool = False
) -> None:
    for key, value in metadata.items():
        try:
            if isinstance(value, bytes):
                value: str = value.decode("utf-8")
                if verbose and all(c in "\x00" for c in value):
                    raise Exception("value contains only NULL bytes")
                if not verbose and not value.isprintable():
                    value: str = ""
            print_metadata_value(key, value, verbose)
        except Exception as e:
            if verbose:
                warn: str = f"{color.WARNING}{e}{color.RESET}"
                print(f"{key:30}: {warn} : {repr(value)}")
            continue


def display_image_metadata(
    args: argparse.Namespace, image_path: pathlib.Path, index: int
) -> None:
    print_image_metadata_header(args, index, image_path)
    metadata: dict[str, typing.Any] = {}
    try:
        extract_basic_file_info(image_path, metadata)
        with Image.open(image_path) as image:
            extract_basic_image_info(image, metadata)
            add_separator(metadata)
            extract_image_exif(image, metadata)
        print_image_metadata(metadata, args.verbose)
    except Exception as e:
        add_separator(metadata)
        print_image_metadata(metadata, args.verbose)
        print(f"{color.WARNING}Skipping image: {e}{color.RESET}")


def process_metadata(args: argparse.Namespace) -> None:
    if args.delete:
        print_deleting_metadata_header()
    for i, image in enumerate(args.image):
        if args.delete:
            strip_image_metadata(args, image, i + 1)
        else:
            display_image_metadata(args, image, i + 1)


def main() -> None:
    print_header()
    args: argparse.Namespace = parse_args()
    process_metadata(args)
    print("{:-^80}".format(""))


if __name__ == "__main__":
    main()
