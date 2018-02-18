"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.0"

import sys
import argparse

from faradayio.faraday import Faraday

def setupArgParse():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("callsign", help="Callsign of Faraday radio")
    parser.add_argument("ID", type=int, help="ID number Faraday radio")

    # Optional arguments
    parser.add_argument("-l", "--loopback", action="store_true", help="Use software loopback serial port")

    # Parse and return arguments
    return parser.parse_args()

def main():
    print("Executing faradayio-cli version {0}".format(__version__))

    # Setup command line arguments
    args = setupArgParse()
