# notify-queue-daemon

## Overview
One of the problems when using a notification system in a window manager is that messages may be lost entirely if the user isn't present to read them. 
Notify-queue-daemon solves this problem by creating a logged history of notifications, ensuring that they are not missed.

The way it works?  It's fairly straightforward. Firstly, the daemon is launched, whether manually, via user service or as a startup entry in your window manager. Once the daemon is listening, then the client can be used is used to send custom notifications using notify-osd. In addition to calling notify-osd itself, the daemon will print messages to standard output and log them to file.

One advantage of this approach is that since the daemon runs as the user, then it can be used to shuttle notifications from service managers such as systemd or runit to the desktop (e.g. by placing it in a systemd ExecStop= line) 

The notify_queue_client is quite flexible and can specify message headings, subheadings and icons.

## Install

This program requires minimal dependencies, using only standard Python libraries as well as notify-osd itself. Possible future improvement may include support for additional notification systems.

To install just copy notify_queue_daemon.py and notify_queue_client.py to your path (e.g. /usr/bin) and then launch notify_queue_daemon.py.  Ensure that the daemon process is running as a user that can access the X session.

## Example usage
notify-queue_client -i ~/iconfile.svg -m "Something happened"

notify-queue-client -m "Main heading of message" -s "Smaller subheading"

