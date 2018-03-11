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
    parser.add_argument("-b", "--baud", default=115200, type=int,
                        help="Set serial port baud rate")
    parser.add_argument("-l", "--loopback", action="store_true",
                        help="Use software loopback serial port")
    parser.add_argument("-m", "--mtu", default=1500, type=int,
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
        raise TypeError("callsign must be a string")
    # Callsigns are at most seven characters long
    if not 3 <= len(args.callsign) <= 7:
        raise ValueError("callsign must be between 3 and 7 characters long")

    # Check ID
    # Expect and integer
    if not isinstance(args.id, int):
        raise TypeError("id must be an integer")
    # Expect a value between 0-255
    if not 0 <= args.id <= 255:
        raise ValueError("id must be between 0 and 255")

    # Check IP Address
    # Expect a string
    if not isinstance(args.addr, str):
        raise TypeError("IP address must be a string")
    # Expect an IP address that is valid
    ipaddress.IPv4Address(args.addr)

    # Check Baud Rate
    # Expect and integer
    if not isinstance(args.baud, int):
        raise TypeError("baud rate must be an integer")
    # Expect and integer that is a standard serial value
    # Should be able to use argparse choices too
    baudrate = [50, 75, 110, 134, 150, 200, 600, 1200, 1800, 2400, 4800, 9600,
                19200, 38400, 57600, 115200, 230400, 460800, 500000, 57600,
                921600]
    if args.baud not in baudrate:
        raise ValueError("baud rate must be a standard value per --help")

    # Check loopback True/False
    # Expect a boolean
    if not isinstance(args.loopback, bool):
        raise TypeError("loopback must be a boolean")

    # Check Maximum Transmission Unit (MTU)
    # Expect and integer
    if not isinstance(args.mtu, int):
        raise TypeError("mtu must be an integer")
    # Expect a value between 68-65535 per RFC 791
    if not 68 <= args.mtu <= 65535:
        raise ValueError("mtu must be between 68 and 65535 bytes")

    # Check serial port path value
    # Expect a string
    if not isinstance(args.port, str):
        raise TypeError("serial port path must be a string")

    # Check timeout
    # Expect and integer
    if not isinstance(args.timeout, int):
        if not isinstance(args.timeout, type(None)):
            # TODO: Likely cannot be NoneType yet per argparse design
            raise TypeError("read timeout must be an integer or Nonetype")
    # Expect a value greater than zero
    if isinstance(args.timeout, int):
        if not 0 <= args.timeout:
            raise ValueError("read timeout must be a positive value")

    # Check write timeout
    # Expect and integer
    if not isinstance(args.writetimeout, int):
        if not isinstance(args.writetimeout, type(None)):
            # TODO: Likely cannot be NoneType yet per argparse design
            raise TypeError("write timeout must be an integer or Nonetype")
    # Expect a value greater than zero
    if isinstance(args.writetimeout, int):
        if not 0 <= args.writetimeout:
            raise ValueError("write timeout must be a positive value")


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
