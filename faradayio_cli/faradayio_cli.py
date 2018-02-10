"""faradayio-cli.faradayio-cli: provides entry point main()."""

__version__ = "0.0.0"

import sys

from faradayio.faraday import Faraday

def main():
    print("Executing faradayio-cli version {0}".format(__version__))
