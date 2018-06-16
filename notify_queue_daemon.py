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
from datetime import datetime
import argparse
from os import path
import logging
from logging.handlers import RotatingFileHandler

parser = argparse.ArgumentParser()
parser.set_defaults(listen_ip="127.0.0.1",nolog=False,port=8100,logfile=path.join(path.expanduser('~'),'notify-daemon.log'))
parser.add_argument('--listen_ip','-i',type=str,help="Specifies the IP for the notification daemon to listen on.  Defaults to 127.0.0.1 for security reasons.")
parser.add_argument('--port','-p',type=int,help="Specifies the port for the notification daemon to listen on.  Defaults to 8100.")
parser.add_argument('--nolog','-n',action='store_true',help="Disables logging of notifications")
parser.add_argument('--logfile','-l',type=str,help="Specifies the file where notifications should be logged.  Defaults to ~/notify-daemon.log")
args = parser.parse_args()

# Initialises this variable
called_notify_osd = False
use_icons = True

def main():

    global first_run, called_notify_osd

    print('Notification queue: ')

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
    message_text_length = int(len(message.split(':')) - 1)
    message_text = message.split(':')[0]

    # Determines whether or not a subtitle for this message exists
    try:
        subtitle_text = message.split(':')[1]
    except:
        subtitle=False
    else:
        subtitle=True

    message_date = str('\u001b[31;1m' + datetime.now().ctime() + ': ' + '\u001b[0m')

    # Prints the message to the screen
    if subtitle:
        full_message = message_text + ' - ' + subtitle_text
        print(message_date + full_message)
    if not subtitle:
        full_message = message_text
        print(message_date + full_message)

    # Get the icon if specified
    try:
        message_icon = message.split(':')[-1]
    except:
        icon=False
    else:
        icon=True

    # Now send the notification with or without the icon
    if icon and subtitle:
        try:
            subprocess.call(['notify-send','-u','critical','-i',message_icon,message_text,subtitle_text])
        except subprocess.CalledProcessError as E:
            raise ValueError('Notification send failure') from E
    if not icon and subtitle:
        try:
            subprocess.call(['notify-send','-u','critical',message_text,subtitle_text])
        except subprocess.CalledProcessError as E:
            raise ValueError('Notification send failure') from E
    if icon and not subtitle:
        try:
            subprocess.call(['notify-send','-u','critical',message_text])
        except subprocess.CalledProcessError as E:
            raise ValueError('Notification send failure') from E
    if not icon and not subtitle:
        try:
            subprocess.call(['notify-send','-u','critical',message_text])
        except subprocess.CalledProcessError as E:
            raise ValueError('Notification send failure') from E

    # Log the notification
    def create_rotating_log(path,message_date,full_message):
        """
        Creates a rotating log
        """
        logger = logging.getLogger("Rotating Log")
        logger.setLevel(logging.INFO)

        # add a rotating handler
        handler = RotatingFileHandler(path, maxBytes=10000,
                                      backupCount=5)
        logger.addHandler(handler)
        log_output = message_date + full_message
        logger.info(log_output)

    if not args.nolog:
        create_rotating_log(args.logfile,message_date,full_message)

# This just binds the UDP socket
def bind_socket():
    # Create a UDP socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((args.listen_ip,args.port))
    return s


if __name__ == main():
    main()
