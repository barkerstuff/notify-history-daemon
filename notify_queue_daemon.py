#!/usr/bin/env python3

# Media queue daemon - A daemon that can aggregate an entire series of URLs sent to the client program over a designated timeframe, sort them as logically it can and formulate a playlist for a selected media player
#(C) 2018  Jason Barker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import subprocess
import re

listen_ip="127.0.0.1"
listen_port=8100

# Initialises this variable
called_notify_osd = False

def main():

    global first_run, called_notify_osd

    def init():
        s = bind_socket()
        return s

     # This calls the stuff that only needs to happen one time
    def first_run():
        s = init()


    # This function actually receives the datagrams
    def receive_datagram(s):
        data = (s.recvfrom(1024)[0]).decode().rstrip()
        return data

    # This is called when waiting for the first datagram containing a new message
    def pass_message(s):
        s.settimeout(None)
        data = receive_datagram(s)
        return first_datagram_time


    # Main daemon loop
    while True:
        if first_run:
            s = init()
            first_run = False

            # Reset called_notify_osd to False for the new set of links
            called_notify_osd = False
            # Get that first datagram, add the url to the list (global) and get the timestamp

        while True:
                print('Waiting for subsequent datagrams')
                message = receive_datagram(s)
                while called_notify_osd == False:
                    call_notify(message)
                else:
                    print('Got a message: {0}'.format(message))


def call_notify(message):
    global called_notify_osd
    try:
        subprocess.call(['notify-send','-u','critical',message])
    except:
        raise ValueError('Notification failure')
    else:
        called_notify_osd = True

# This just binds the UDP socket
def bind_socket():
    # Create a UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((listen_ip,listen_port))
    return s


if __name__ == main():
    main()
