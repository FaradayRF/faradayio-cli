# faradayio-cli
[![Build Status](https://travis-ci.org/FaradayRF/faradayio-cli.svg?branch=master)](https://travis-ci.org/FaradayRF/faradayio-cli) [![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/FaradayRF/Lobby)

The `faradayio-cli` package provides a command line implementation of the [`faradayio`](https://github.com/FaradayRF/faradayio) module. Like the `faradayio` module this program is also radio agnostic and will work with any RF module that accepts serial port SLIP encoded IP frames. Running `faradayio-cli` results in a TUN/TAP adapter being implemented which persists as long as the program is running. This module then redirects any packets destined for the IP range assinged to the TUN/TAP adapter to the serial port specified.
