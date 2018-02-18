"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.0"

import sys
import argparse

from faradayio.faraday import Faraday

def setupArgparse():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("Callsign", help="Callsign of radio")
    parser.add_argument("ID", type=int, help="ID number radio")

    # Optional arguments
    parser.add_argument("-l", "--loopback", action="store_true", help="Use software loopback serial port")
    parser.add_argument("-p", "--port", default="dev/ttyUSB0", help="Physical serial port of radio")

    # Parse and return arguments
    return parser.parse_args()

def main():
    print("Executing faradayio-cli version {0}".format(__version__))

    # Setup command line arguments
    args = setupArgparse()

    print(args)
    # Setup serial port
    # setupSerialPort(args.loopback)
