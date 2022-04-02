# Uno-LCD-Terminal-Daemon
A daemon for the [Uno LCD Terminal](https://github.com/UnsignedArduino/Uno-LCD-Terminal)!

The daemon will create an icon in the notification area ([incorrectly known as the "system tray"](https://www.howtogeek.com/685748/did-you-know-windows-has-never-had-a-system-tray/)) and will show the status and allow you to quit the program!

![Picture of the Uno LCD Terminal Daemon icon in the notification area](https://user-images.githubusercontent.com/38868705/161360910-2c7c82f6-b802-463b-b5a3-602af09a5d1e.png)

It is hot pluggable, so you can unplug and replug your Uno LCD Terminal back in all you want! (As long as the serial port name stays the same) It's also happy being started on system startup.

## Hardware 

See the [`README.md`](https://github.com/UnsignedArduino/Uno-LCD-Terminal/blob/main/README.m) for the Uno LCD Terminal for instructions and details.

## Software

### Installation

1. Clone this repo.
2. Create virtual environment if desired.
3. Install dependencies in [`requirements.txt`](https://github.com/UnsignedArduino/Uno-LCD-Terminal-Daemon/blob/main/requirements.txt).

### Running

Run [`main.py`](https://github.com/UnsignedArduino/Uno-LCD-Terminal-Daemon/blob/main/main.py). 

This is my batch file (`.bat` file on Windows) which I set to auto start on Windows:

```commandline
REM Go to the E: drive
E:

REM Change directories to the "Uno LCD Terminal Daemon" directory
cd "Uno LCD Terminal Daemon"

REM Run main.py with pythonw (the binary in venv\Scripts\ will respect the virtual environment) 
"venv\Scripts\pythonw" main.py -c -p COM8 -o "time" -o "cpu" -o "memory" -o "disk" -o "network"
```

### Command line arguments

#### Help
Run with `-h` or `--help` to view the help:
```commandline
usage: main.py [-h] [-lp] [-lo] [-c] [-p PORT] [-u INTERVAL] [-r INTERVAL]
               [-o NAME] [-d]

Daemon for the Uno LCD Terminal.

optional arguments:
  -h, --help            show this help message and exit
  -lp, --list-ports     List serial ports and exit.
  -lo, --list-outputs   List function outputs and exit.
  -c, --connect         Connect to an Uno LCD Terminal.
  -p PORT, --port PORT  A port to connect to. Required if connecting with -c
                        or --connect. Can be a path or an index from -l or
                        --list-ports.
  -u INTERVAL, --update-interval INTERVAL
                        The update interval for the Uno LCD Terminal in float
                        seconds. Required if connecting with -c or --connect.
                        Defaults to 1.0.
  -r INTERVAL, --change-interval INTERVAL
                        The change interval for the Uno LCD Terminal in
                        integer seconds. Required if connecting with -c or
                        --connect. Defaults to 1.
  -o NAME, --output NAME
                        The outputs you want to use. At least one is required
                        if connecting with -c or --connect. Can be specified
                        multiple times.
  -d, --debug           Whether to show debug output or not.
```

#### Example commands:

List all serial ports:
```commandline
main.py -lp
```
Example output on Windows:
```commandline
2022-04-01 21:42:27,946 - __main__ - INFO - Listing connected serial ports
2022-04-01 21:42:27,956 - __main__ - INFO - 1/6: COM1 - Communications Port (COM1)
2022-04-01 21:42:27,957 - __main__ - INFO - 2/6: COM14 - Standard Serial over Bluetooth link (COM14)      
2022-04-01 21:42:27,957 - __main__ - INFO - 3/6: COM15 - Standard Serial over Bluetooth link (COM15)      
2022-04-01 21:42:27,957 - __main__ - INFO - 4/6: COM18 - USB Serial Device (COM18)
2022-04-01 21:42:27,957 - __main__ - INFO - 5/6: COM3 - Intel(R) Active Management Technology - SOL (COM3)
2022-04-01 21:42:27,957 - __main__ - INFO - 6/6: COM8 - Arduino Uno (COM8)
```

List all output functions: (they generate text to send to the Terminal)
```commandline
main.py -lo
```
Example output on Windows:
```commandline
2022-04-01 21:43:22,217 - __main__ - INFO - Listing output functions
2022-04-01 21:43:22,217 - __main__ - INFO - 1 / 5: time - Shows the date and time.
2022-04-01 21:43:22,217 - __main__ - INFO - 2 / 5: cpu - Shows the CPU utilization
2022-04-01 21:43:22,217 - __main__ - INFO - 3 / 5: memory - Shows the memory utilization
2022-04-01 21:43:22,217 - __main__ - INFO - 4 / 5: disk - Shows the disk IO counters
2022-04-01 21:43:22,217 - __main__ - INFO - 5 / 5: network - Shows the network IO counters
```

Connect to `COM8` and use the output functions `time`, `cpu`, `memory`, `disk`, and `network`:
```commandline
main.py -c -p COM8 -o "time" -o "cpu" -o "memory" -o "disk" -o "network"
```
Note that doing this needs a [supported desktop](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QSystemTrayIcon.html#detailed-description). (sorry hardcore command line users - you can go back [earlier in time to use an older version that does not use an icon](https://github.com/UnsignedArduino/Uno-LCD-Terminal-Daemon/tree/72daaa94cdf53d8a4c3adfc83c4ee9840ae5664c))

According to the [Qt 5 docs](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QSystemTrayIcon.html#detailed-description):
> The `QSystemTrayIcon` class can be used on the following platforms:
> 
> - All supported versions of Windows.
> 
> - All window managers and independent tray implementations for X11 that implement the http://standards.freedesktop.org/systemtray-spec/systemtray-spec-0.2.html freedesktop.org XEmbed system tray specification.
> 
> - All X11 desktop environments that implement the D-Bus http://www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierItem specification, including recent versions of KDE and Unity.
> 
> - All supported versions of macOS.

Example output on Windows:
```commandline
2022-04-01 21:43:41,550 - __main__ - INFO - Connecting to COM8
2022-04-01 21:43:41,663 - uno_lcd_terminal - INFO - Connected!
```
