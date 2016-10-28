"""
Restaurant 2 Diner Droid.

Parameter <day> can be either "today" or "tomorrow".

Usage:
    @CERN-R2-D2 menu <day>
    @CERN-R2-D2 echo <msg>...
    @CERN-R2-D2 selfdestruct

Examples:
    @CERN-R2-D2 menu tomorrow
    @CERN-R2-D2 echo Hello @/all!

Options:
    -h --help   Show this help.
    --version   Show version.
"""

from __init__ import __version__
from docopt import docopt
from menu import fetch_menu, format_pretty_menu_msg
from config import ADMINS
import sys
from time import sleep


class Client(object):
    """Base communication client."""

    def send_msg(self, text):
        """Send a message to a destination."""
        raise NotImplementedError


class StdoutClient(Client):
    """Simple client for printing to console."""

    def send_msg(self, text):
        """Send a message to standard output."""
        print(text)


def bot_main(client, args, msg_json=None):
    """Main bot function."""
    if args['menu']:
        day = args['<day>']
        if day not in ['today', 'tomorrow']:
            msg = "Please specify a correct day (today or tomorrow)."
        else:
            menu = fetch_menu(day)
            msg = format_pretty_menu_msg(menu)
        client.send_msg(msg)
    elif args['echo']:
        msg = " ".join(args['<msg>'])
        client.send_msg(msg)
    elif args['selfdestruct']:
        if msg_json['fromUser']['username'] in ADMINS:
            client.send_msg("Self destructing in 3..")
            sleep(1)
            client.send_msg("..2")
            sleep(1)
            client.send_msg("..1")
            sleep(1)
            client.send_msg(":boom:")
            sys.exit(0)
        else:
            name = msg_json['fromUser']['displayName']
            name = name.split()[0] if name.split()[0] else name
            client.send_msg(
                "I'm sorry {0}, I'm afraid I can't do that.".format(name))

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    bot_main(StdoutClient(), args)
