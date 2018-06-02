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

from socket import socket
from socket import AF_INET
from socket import SOCK_DGRAM
import subprocess
import re

listen_ip="127.0.0.1"
listen_port=8100

# Initialises this variable
called_notify_osd = False
use_icons = True

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
                #print('Waiting for subsequent datagrams')
                message = receive_datagram(s)
                #print('Got a message: {0}'.format(message))
                call_notify(message)


def call_notify(message):
    # Get the message component
    message_text = message.split(':')[0]
    print("Message: " + message_text)

    # Get the icon if specified
    try:
        message_icon = message.split(':')[1]
    except:
        icon=False
    else:
        icon=True

    # Now send the notification with or without the icon
    if icon:
        try:
            subprocess.call(['notify-send','-u','critical',message_text,'-i',message_icon])
        except CalledProcessError as E:
            raise ValueError('Notification send failure') from E
    else:
        try:
            subprocess.call(['notify-send','-u','critical',message_text])
        except CalledProcessError as E:
            raise ValueError('Notification send failure') from E


# This just binds the UDP socket
def bind_socket():
    # Create a UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((listen_ip,listen_port))
    return s


if __name__ == main():
    main()
