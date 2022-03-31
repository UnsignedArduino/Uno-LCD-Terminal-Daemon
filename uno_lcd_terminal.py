import logging
from enum import Enum
from time import sleep, time as unix
from typing import Callable, Optional, Sized

from serial import Serial

from logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class UnoLCDTerminalAttribute(Enum):
    WIDTH = b"w"
    HEIGHT = b"h"
    HAS_COLOR = b"c"


class UnoLCDTerminalBacklightColor(Enum):
    OFF = b"o"
    RED = b"r"
    YELLOW = b"y"
    GREEN = b"g"
    TEAL = b"t"
    BLUE = b"b"
    VIOLET = b"v"
    WHITE = b"w"


class UnoLCDTerminal:
    """
    Represents a Uno LCD Terminal.
    """

    def __init__(self, path: str):
        """
        Initiate a Uno LCD Terminal wrapper at a device path.

        :param path: The device path to the terminal. (for example, "COM8"
         or "/dev/ttyUSB0")
        """
        self.path = path

    def run(self, update_interval: int, change_interval: int,
            output_funcs: list[Callable]):
        """
        Connect to the device and start sending text.

        :param update_interval: The update interval, in integer seconds.
        :param change_interval: The time between switching output functions,
         in integer seconds.
        :param output_funcs: A Sized of output functions that we will step
         through every change interval.
        """
        logger.debug(f"Opening path {self.path}")
        with Serial(self.path) as port:
            logger.info("Connected!")
            logger.debug(f"Update interval: {update_interval}s")
            logger.debug(f"Change interval: {change_interval}s")
            logger.debug(f"Output functions: {len(output_funcs)}")
            last_change = unix()
            curr_func_idx = 0

            def write_cmd(sequence: bytes):
                # logger.debug(f"Command: {sequence}")
                port.write(sequence)

            write_cmd(UnoLCDTerminal.reset_sequence())
            write_cmd(UnoLCDTerminal.set_background_color_sequence(
                UnoLCDTerminalBacklightColor.WHITE))
            while True:
                if unix() - last_change > change_interval:
                    last_change = unix()
                    curr_func_idx += 1
                    if curr_func_idx > len(output_funcs) - 1:
                        curr_func_idx = 0
                # write_cmd(UnoLCDTerminal.clear_sequence())
                write_cmd(UnoLCDTerminal.home_sequence())
                output = output_funcs[curr_func_idx]()
                for index, line in enumerate(output):
                    write_cmd(UnoLCDTerminal.set_cursor_sequence(row=index))
                    write_cmd(UnoLCDTerminal.write_string_sequence(line))
                sleep(update_interval)

    @staticmethod
    def reset_sequence() -> bytes:
        """
        Return the reset sequence.

        :return: Bytes.
        """
        return b"r"

    @staticmethod
    def clear_sequence() -> bytes:
        """
        Return the clear sequence.

        :return: Bytes.
        """
        return b"d"

    @staticmethod
    def home_sequence() -> bytes:
        """
        Return the home sequence.

        :return: Bytes.
        """
        return b"h"

    @staticmethod
    def set_cursor_sequence(col: Optional[int] = None,
                            row: Optional[int] = None) -> bytes:
        """
        Return the set cursor sequence.

        :param col: The new column to set to.
        :param row: The new row to set to.
        :return: Bytes.
        """
        b = b""
        if col is not None:
            b += b"cc"
            b += str(col).encode()
        if row is not None:
            b += b"cr"
            b += str(row).encode()
        return b

    @staticmethod
    def get_attribute_sequence(attr: UnoLCDTerminalAttribute) -> bytes:
        """
        Return the get attribute sequence.

        :param attr: The attribute to get for.
        :return: Bytes.
        """
        return b"a" + attr.value

    @staticmethod
    def write_string_sequence(string: str) -> bytes:
        """
        Return the write string sequence.

        :param string: The string to write.
        :return: Bytes.
        """
        return b"p" + string.encode() + b"\r\n"

    @staticmethod
    def set_background_color_sequence(
            color: UnoLCDTerminalBacklightColor) -> bytes:
        """
        Return the set background color sequence.

        :param color: The color to set to.
        :return: Bytes.
        """
        return b"b" + color.value
