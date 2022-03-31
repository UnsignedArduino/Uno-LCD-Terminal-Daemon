import logging
from argparse import ArgumentParser
from serial.tools.list_ports import comports

from logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(description="Daemon for the Uno LCD Terminal.")
parser.add_argument("-l", "--list-ports", dest="list_ports",
                    action="store_true",
                    help="List serial ports and exit.")
args = parser.parse_args()
logger.debug(f"Arguments received: {args}")

if args.list_ports:
    logger.info("Listing connected serial ports")
    ports = sorted(comports(), key=lambda p: p.name)
    for index, port in enumerate(ports):
        port_index = f"{index + 1}/{len(ports)}:"
        logger.info(f"{port_index} "
                    f"{port.device} - "
                    f"{port.description}")
        indent_space = len(port_index) * " "
        logger.debug(f"{indent_space}HWID: {port.hwid} ")
        for label, value in {
            "VID": port.vid,
            "PID": port.pid,
            "Serial number": port.serial_number,
            "Location": port.location,
            "Manufacturer": port.manufacturer,
            "Product": port.product,
            "Interface": port.interface
        }.items():
            if value is None:
                continue
            logger.debug(f"{indent_space}{label}: {value}")
else:
    logger.warning("Nothing to do!")
