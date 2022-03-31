import logging
from argparse import ArgumentParser

from serial.tools.list_ports import comports

from logger import create_logger
from uno_lcd_terminal import UnoLCDTerminal

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(description="Daemon for the Uno LCD Terminal.")
parser.add_argument("-l", "--list-ports", dest="list_ports",
                    action="store_true",
                    help="List serial ports and exit.")
parser.add_argument("-c", "--connect", dest="connect",
                    action="store_true",
                    help="Connect to an Uno LCD Terminal.")
parser.add_argument("-p", "--port", dest="port", metavar="PORT",
                    action="store",
                    help="A port to connect to. Required if connecting with "
                         "-c or --connect. Can be a path or an index from "
                         "-l or --list-ports.")
parser.add_argument("-u", "--update-interval", dest="update_interval",
                    metavar="INTERVAL", action="store", type=int,
                    default=1,
                    help="The update interval for the Uno LCD Terminal in "
                         "integer seconds. "
                         "Required if connecting with -c or --connect. "
                         "Defaults to 1.")
parser.add_argument("-r", "--change-interval", dest="change_interval",
                    metavar="INTERVAL", action="store", type=int,
                    default=5,
                    help="The change interval for the Uno LCD Terminal in "
                         "integer seconds. "
                         "Required if connecting with -c or --connect. "
                         "Defaults to 1.")
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
elif args.connect:
    port_path = args.port
    if port_path.replace("-", "").isnumeric():
        port_path = int(port_path)
        logger.debug(f"Finding port at index {port_path}")
        ports = sorted(comports(), key=lambda p: p.name)
        if port_path > len(ports) or port_path < 1:
            logger.error(f"No port at index {port_path}! "
                         f"(out of {len(ports)} ports)")
            exit(1)
        port_path = ports[port_path - 1].device
    logger.info(f"Connecting to {port_path}")
    term = UnoLCDTerminal(port_path)
    try:
        term.run(args.update_interval, args.change_interval,
                 [
                     lambda: "Function 1",
                     lambda: "Function 2"
                 ])
    except KeyboardInterrupt:
        logger.warning("Exiting!")
else:
    logger.warning("Nothing to do!")
