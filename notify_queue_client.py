#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2018 Jason Barker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import argv
from socket import socket
from socket import SOCK_DGRAM
from socket import AF_INET

# This part of the program is really just responsible for sending a UDP datagram to the media_queue_daemon

target_ip="127.0.0.1"
target_port=8100

def bind_socket():
    # Create a UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    return s

def main():
    s = bind_socket()

    # Receive_datagram
    def send_datagram():
        data = s.sendto(link,((target_ip,target_port)))

    # Initial values
    link = argv[1].encode()
    print(link)
    send_datagram()


if __name__ == main():
    main()
