#!/usr/bin/env python2.7

import os
import sys
try:
    import alexandria
except ImportError:
    sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])
    import alexandria

import alexandria.couch
import alexandria.exc
import alexandria.js
import argparse

def action_addhost(args):
    """Adds a host to the database"""

    try:
        alexandria.couch.add_host(args.host)
        print "Added host to database"
    except alexandria.exc.EditConflict:
        print "Host is already in database!"


def action_delhost(args):
    """Deletes a host from the database"""

    try:
        alexandria.couch.del_host(args.host)
        print "Removed host from database"
    except alexandria.exc.DocumentNotFound:
        print "Host is not in database!"


def action_pushviews(args):
    """Pushes design documents to CouchDB"""

    alexandria.couch.store_design_doc('files', alexandria.js.files_doc)
    print "Pushed all views"


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

    pushviews_parser = subparsers.add_parser('pushviews',
        help="Push design documents to CouchDB")
    pushviews_parser.set_defaults(func=action_pushviews)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
