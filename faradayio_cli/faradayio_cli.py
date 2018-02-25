"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.0"

import argparse
import serial
import threading
import time

from faradayio.faraday import Monitor
from faradayio.faraday import SerialTestClass


def setupArgparse():
    """Sets up argparse module to create command line options and parse them

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
    parser.add_argument("-l", "--loopback", action="store_true",
                        help="Use software loopback serial port")
    parser.add_argument("-p", "--port", default="/dev/ttyUSB0",
                        help="Physical serial port of radio")

    # Parse and return arguments
    return parser.parse_args()


def setupSerialPort(loopback, port):
    if loopback:
        # Implement loopback software serial port
        testSerial = SerialTestClass()
        serialPort = testSerial.serialPort
    else:
        # TODO enable serial port command line options (keep simple for user!)
        serialPort = serial.Serial(port, 115200, timeout=0)

    return serialPort


def main():
    print("Executing faradayio-cli version {0}".format(__version__))

    # Setup command line arguments
    try:
        args = setupArgparse()

    except argparse.ArgumentError as error:
        raise SystemExit(error)

    # Setup serial port
    try:
        serialPort = setupSerialPort(args.loopback, args.port)

    except serial.SerialException as error:
        raise SystemExit(error)

    # Create TUN adapter name
    tunName = "{0}-{1}".format(args.callsign.upper(), args.id)

    # Create threading event for TUN thread control
    # set() causes while loop to continuously run until clear() is run
    isRunning = threading.Event()
    isRunning.set()

    # Setup TUN adapter and start
    tun = Monitor(serialPort=serialPort, name=tunName, isRunning=isRunning)
    tun.start()

    # loop infinitely until KeyboardInterrupt, then clear() event, exit thread
    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        tun.isRunning.clear()
        tun.join()
