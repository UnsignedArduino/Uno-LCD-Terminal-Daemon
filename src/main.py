import logging
import sys
from argparse import ArgumentParser
from time import sleep

from PyQt5.QtCore import QCoreApplication, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

import uno_lcd_terminal
from logger import create_logger
from outputs import OUTPUT_FUNCTIONS
from uno_lcd_terminal import UnoLCDTerminal

parser = ArgumentParser(description="Daemon for the Uno LCD Terminal.")
parser.add_argument("-lp", "--list-ports", dest="list_ports",
                    action="store_true",
                    help="List serial ports and exit.")
parser.add_argument("-lo", "--list-outputs", dest="list_outputs",
                    action="store_true",
                    help="List function outputs and exit.")
parser.add_argument("-c", "--connect", dest="connect",
                    action="store_true",
                    help="Connect to an Uno LCD Terminal.")
parser.add_argument("-p", "--port", dest="port", metavar="PORT",
                    action="store",
                    help="A port to connect to. Required if connecting with "
                         "-c or --connect. Can be a path or an index from "
                         "-l or --list-ports.")
parser.add_argument("-u", "--update-interval", dest="update_interval",
                    metavar="INTERVAL", action="store", type=float,
                    default=1.0,
                    help="The update interval for the Uno LCD Terminal in "
                         "float seconds. "
                         "Required if connecting with -c or --connect. "
                         "Defaults to 1.0.")
parser.add_argument("-r", "--change-interval", dest="change_interval",
                    metavar="INTERVAL", action="store", type=int,
                    default=10,
                    help="The change interval for the Uno LCD Terminal in "
                         "integer seconds. "
                         "Required if connecting with -c or --connect. "
                         "Defaults to 1.")
parser.add_argument("-o", "--output", dest="outputs",
                    metavar="NAME", action="append",
                    help="The outputs you want to use. At least one is "
                         "required if connecting with -c or --connect. Can be "
                         "specified multiple times.")
parser.add_argument("-d", "--debug", dest="debug",
                    action="store_true",
                    help="Whether to show debug output or not. ")
args = parser.parse_args()

logger = create_logger(name=__name__, level=logging.INFO)
logger.debug(f"Arguments received: {args}")

if args.debug:
    all_loggers = (
        logger,
        uno_lcd_terminal.logger
    )

    for l in all_loggers:
        l.setLevel(logging.DEBUG)


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
elif args.list_outputs:
    logger.info("Listing output functions")
    for index, (key, value) in enumerate(OUTPUT_FUNCTIONS.items()):
        logger.info(f"{index + 1} / {len(OUTPUT_FUNCTIONS.keys())}: "
                    f"{key} - {value.__doc__}")
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
    if args.outputs is None:
        logger.error("Please specify at least one output function!")
        exit(1)
    time_between_recon = 2


    class SystemTrayIcon(QSystemTrayIcon):
        def __init__(self, icon, parent=None):
            super().__init__(icon, parent)
            menu = QMenu(parent)
            menu.setTitle("Uno LCD Terminal Daemon")
            self.title_action = menu.addAction("Uno LCD Terminal Daemon")
            self.title_action.setEnabled(False)
            menu.addSeparator()
            self.status_action = menu.addAction("Starting")
            self.status_action.setEnabled(False)
            menu.addSeparator()
            self.exit_action = menu.addAction("Exit", QCoreApplication.exit)
            self.setContextMenu(menu)
            self.daemon_t = QThread()
            self.daemon = DaemonQObject()
            self.daemon.moveToThread(self.daemon_t)
            self.daemon.finished.connect(self.daemon_t.quit)
            self.daemon.status.connect(lambda s: self.status_action.setText(s))
            self.daemon_t.started.connect(self.daemon.run)
            self.daemon_t.start()


    class DaemonQObject(QObject):
        finished = pyqtSignal()
        status = pyqtSignal(str)

        def run(self):
            while True:
                try:
                    self.status.emit(f"Connected to {port_path}")
                    term.run(args.update_interval, args.change_interval,
                             [OUTPUT_FUNCTIONS[o.lower()] for o in
                              args.outputs])
                except SerialException:
                    self.status.emit(f"Disconnected from {port_path}")
                    logger.warning(f"Unable to connect to {port_path}, "
                                   f"retrying in {time_between_recon}s...")
                    sleep(time_between_recon)
            self.finished.emit()


    app = QApplication(sys.argv)
    w = QWidget()
    tray_icon = SystemTrayIcon(QIcon("src/assets/icon.ico"), w)
    tray_icon.show()
    sys.exit(app.exec_())
else:
    logger.warning("Nothing to do!")
