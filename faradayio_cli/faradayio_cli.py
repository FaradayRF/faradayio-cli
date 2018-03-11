"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.4"

import argparse
import serial
import threading
import time
import pytun
import ipaddress

from faradayio.faraday import Monitor
from faradayio.faraday import SerialTestClass


def setupArgparse():
    """Sets up argparse module to create command line options and parse them.

    Uses the argparse module to add arguments to the command line for
    faradayio-cli. Once the arguments are added and parsed the arguments are
    returned

    Returns:
        argparse.Namespace: Populated namespace of arguments
    """
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("callsign", help="Callsign of radio")
    parser.add_argument("id", type=int, help="ID number radio")

    # Optional arguments
    parser.add_argument("--addr", default="10.0.0.1",
                        help="Set IP Address of TUN adapter (Faraday Radio)")
    parser.add_argument("-b", "--baud", default="115200",
                        help="Set serial port baud rate")
    parser.add_argument("-l", "--loopback", action="store_true",
                        help="Use software loopback serial port")
    parser.add_argument("-m", "--mtu", default=1500,
                        help="Set Maximum Transmission Unit (MTU)")
    parser.add_argument("-p", "--port", default="/dev/ttyUSB0",
                        help="Physical serial port of radio")
    parser.add_argument("--timeout", default=0, type=int,
                        help="Set serial port read timeout")
    parser.add_argument("--writetimeout", default=None, type=int,
                        help="Set serial port read timeout")

    # Parse and return arguments
    return parser.parse_args()

def checkUserInput(args):
    """Checks user input for validity

    Args:
        args: argparse arguments

    """
    # Check callsign
    # Expect a string
    if not isinstance(args.callsign, str):
        raise TypeError
    # Callsigns are at most seven characters long
    if len(args.callsign) > 7:
        raise ValueError

    # Check ID
    # Expect and integer
    if not isinstance(args.id, int):
        raise TypeError
    # Expect a value between 0-255
    if args.id < 0 or args.id > 255:
        raise ValueError

    # Check IP Address
    # Expect a string
    if not isinstance(args.addr, str):
        raise TypeError
    # Expect an IP address that is valid
    ipaddress.IPv4Address(args.addr)


def setupSerialPort(loopback, port, baud, readtimeout, writetimeout):
    """Sets up serial port by connecting to phsyical or software port.

    Depending on command line options, this function will either connect to a
    SerialTestClass() port for loopback testing or to the specified port from
    the command line option. If loopback is True it overrides the physical port
    specification.

    Args:
        loopback: argparse option
        port: argparse option
        baud: serial port baudrate
        readtimeout: serial port read timeout
        writetimeout: serial port write timeout

    Returns:
        serialPort: Pyserial serial port instance
    """
    if loopback:
        # Implement loopback software serial port
        testSerial = SerialTestClass()
        serialPort = testSerial.serialPort
    else:
        # TODO enable serial port command line options (keep simple for user!)
        serialPort = serial.Serial(port=port,
                                   baudrate=baud,
                                   timeout=readtimeout,
                                   write_timeout=writetimeout)

    return serialPort


def main():
    """Main function of faradayio-cli client.

    Informs user of version being run and then sets up the program followed
    by starting up the TUN/TAP device threads.
    """
    print("Executing faradayio-cli version {0}".format(__version__))

    # Setup command line arguments
    try:
        args = setupArgparse()

    except argparse.ArgumentError as error:
        raise SystemExit(error)

    checkUserInput(args)

    # Setup serial port
    try:
        serialPort = setupSerialPort(loopback=args.loopback,
                                     port=args.port,
                                     baud=args.baud,
                                     readtimeout=args.timeout,
                                     writetimeout=args.writetimeout)

    except serial.SerialException as error:
        raise SystemExit(error)

    # Create TUN adapter name
    tunName = "{0}-{1}".format(args.callsign.upper(), args.id)

    # Create threading event for TUN thread control
    # set() causes while loop to continuously run until clear() is run
    isRunning = threading.Event()
    isRunning.set()

    # Setup TUN adapter and start
    try:
        tun = Monitor(serialPort=serialPort,
                      name=tunName,
                      isRunning=isRunning,
                      addr=args.addr,
                      mtu=int(args.mtu))
        tun.start()

    except pytun.Error as error:
        print("Warning! faradayio-cli must be run with sudo privileges!")
        raise SystemExit(error)

    # loop infinitely until KeyboardInterrupt, then clear() event, exit thread
    try:
        while True:
            # Check for KeyboardInterrupt every 100ms
            time.sleep(0.1)

    except KeyboardInterrupt:
        tun.isRunning.clear()
        tun.join()
