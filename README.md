# notify-history-daemon

## Overview
One of the problems when using a notification system in a window manager is that messages may be lost entirely if the user isn't present to read them. 
Notify-history-daemon solves this problem by creating a logged history of notifications, ensuring that they are not missed.

The way it works?  It's fairly straightforward. Firstly, the daemon is launched, whether manually, via user service or as a startup entry in your window manager. Once the daemon is listening, then the client can be used is used to send custom notifications using notify-osd. In addition to calling notify-osd itself, the daemon will print messages to standard output and log them to file.

One additional advantage of this approach is that since the daemon runs as the user, then notifications can also be easily shuttled from service managers such as systemd/runit to the desktop (e.g. by placing it in a systemd ExecStop= line). Normally this would be prevented if calling notify-send without the daemon.  Furthermore, it is possible to make the daemon and client communicate over a network, thereby allowing you to send notifications from another device.

The notify_history_client is quite flexible and can specify message headings, subheadings and icons.

## Install

This program requires minimal dependencies, using only standard Python libraries as well as notify-osd itself. Possible future improvement may include support for additional notification systems.

To install just copy notify-history-daemon and notify-history-client.py to your path (e.g. /usr/bin) and then launch notify-history-daemon.py.  Ensure that the daemon process is running as a user that can access the X session.

## Example usage
#### To specify a message with no icon 
notify-history-client -m "Message here"
#### To specify a message with an additional icon 
notify-history_client -i ~/iconfile.svg -m "Something happened"
#### To specify a message with a subheading and no icon
notify-history-client -m "Main heading of message" -s "Smaller subheading"
#### To send a message to a daemon process listening on another computer on the LAN
notify-history-client -m "Message here" -t 192.168.0.2
#### To bind the daemon on the LAN ip of 192.168.0.1 (rather than the default of listening locally only)
notify-history-daemon -i 192.168.0.1
#### To get help on additional options 
notify-history-client --help

notify-history-daemon --help

