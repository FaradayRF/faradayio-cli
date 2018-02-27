# faradayio-cli
[![Build Status](https://travis-ci.org/FaradayRF/faradayio-cli.svg?branch=master)](https://travis-ci.org/FaradayRF/faradayio-cli) [![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/FaradayRF/Lobby)

The `faradayio-cli` package provides a command line implementation of the [`faradayio`](https://github.com/FaradayRF/faradayio) module. Like the `faradayio` module this program is also radio agnostic and will work with any RF module that accepts serial port SLIP encoded IP frames. Running `faradayio-cli` results in a TUN/TAP adapter being implemented which persists as long as the program is running. This module then redirects any packets destined for the IP range assinged to the TUN/TAP adapter to the serial port specified.

## Installation
Install from PyPi for general use. If you would like to develop with the project them please follow these instructions to setup a virtual environment with a fork of the project and install the project in editable mode.

### PyPi

### Git Repository Editable Mode

## Usage

## FaradayRF
This project is provided by [FaradayRF](https://www.faradayrf.com) as [GPLv3](https://github.com/FaradayRF/faradayio/blob/master/LICENSE) software aimed at the amateur radio (ham radio) community. Please join us on our [Gitter lobby](https://gitter.im/FaradayRF/Lobby) if you have any questions. Send an email to [Support@faradayrf.com](Support@faradayrf.com) if you would like to contact us via email.
