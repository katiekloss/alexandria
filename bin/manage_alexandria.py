#!/usr/bin/env python2.7

import os
import sys
try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import alexandria.couch
import argparse

def action_addhost(args):
    """Adds a host to the database"""

    print "Adding host '%s' to the database" % args.host
    alexandria.couch.add_host(args.host)


def action_delhost(args):
    """Deletes a host from the database"""

    print "Removing host '%s' from the database" % args.host
    alexandria.couch.del_host(args.host)


def create_parser():
    """Create an ArgumentParser"""

    parser = argparse.ArgumentParser(description="Manage an Alexandria database")
    subparsers = parser.add_subparsers()

    addhost_parser = subparsers.add_parser('addhost',
        help="Add a host to the database")
    addhost_parser.add_argument('host', help="The host to add")
    addhost_parser.set_defaults(func=action_addhost)

    delhost_parser = subparsers.add_parser('delhost',
        help="Delete a host from the database")
    delhost_parser.add_argument('host', help="The host to remove")
    delhost_parser.set_defaults(func=action_delhost)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
