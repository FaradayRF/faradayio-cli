"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.0"

import sys
import argparse

from faradayio.faraday import Faraday

def setupArgParse():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def main():
    print("Executing faradayio-cli version {0}".format(__version__))

    # Setup command line arguments
    args = setupArgParse()
