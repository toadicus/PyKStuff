__author__ = 'toadicus'
__all__ = []

import argparse
import os
import sys

from KerbalStuff import KerbalStuff, Mod, ModVersion
from zipfile import is_zipfile

parser = argparse.ArgumentParser(description="Interact with the KerbalStuff API.")
actions = parser.add_subparsers(title="actions")
""":type : argparse._SubParsersAction"""


def parser_command(command_name: str, arguments: dict=[], **kwargs: dict) -> argparse.ArgumentParser:
    def meta_decorator(func) -> argparse.ArgumentParser:
        action = actions.add_parser(command_name, **kwargs)
        """:type : argparse.ArgumentParser"""
        for tuple in arguments:
            action.add_argument(*tuple[0], **tuple[1])
        action.set_defaults(func=func)
        return action
    return meta_decorator


@parser_command(
    'bf',
    arguments=[
        (
            ['page_id'],
            {'type': int, 'nargs': '?', 'help': 'optional page number for browse less-new mods', 'default': 1}
        )
    ],
    help="Fetches a list of featured mods from KerbalStuff"
)
def browse_featured(args):
    for m in KerbalStuff.browse_featured(args.page_id):
        print(m)


@parser_command(
    'bn',
    arguments=[
        (
            ['page_id'],
            {'type': int, 'nargs': '?', 'help': 'optional page number for browse less-new mods', 'default': 1}
        )
    ],
    help="Fetches a list of new mods from KerbalStuff"
)
def browse_new(args):
    for m in KerbalStuff.browse_new(args.page_id):
        print(m)


@parser_command(
    'bt',
    arguments=[
        (
            ['page_id'],
            {'type': int, 'nargs': '?', 'help': 'optional page number for browse less-new mods', 'default': 1}
        )
    ],
    help="Fetches a list of top mods from KerbalStuff"
)
def browse_top(args):
    for m in KerbalStuff.browse_top(args.page_id):
        print(m)


@parser_command(
    'mi',
    arguments=[
        (
            ['mod_id'],
            {'type': int}
        )
    ],
    help="Fetches info about a single mod from KerbalStuff"
)
def mod_info(args):
    print(KerbalStuff.mod_info(args.mod_id))


@parser_command(
    'ml',
    arguments=[
        (
            ['mod_id'],
            {'type': int}
        )
    ],
    help="Fetches info about the latest version of a single mod from KerbalStuff"
)
def mod_latest(args):
    print(KerbalStuff.mod_latest(args.mod_id))


@parser_command(
    'sm',
    arguments=[
        (
            ['query'],
            {'type': str}
        )
    ],
    help="Searches KerbalStuff for mods matching the given query and prints a list of any results."
)
def search_mod(args):
    for m in KerbalStuff.search_mod(args.query):
        print(m)


@parser_command(
    'su',
    arguments=[
        (
            ['query'],
            {'type': str}
        )
    ],
    help="Searches KerbalStuff for users matching the given query and prints a list of any results."
)
def search_user(args):
    for u in KerbalStuff.search_user(args.query):
        print(u)


@parser_command(
    'ui',
    arguments=[
        (
            ['username'],
            {'type': str, 'help': 'the username of the desired user'}
        )
    ],
    help="Fetches info about a single user from KerbalStuff"
)
def user_info(args):
    print(KerbalStuff.user_info(args.username))

login_arguments = [
    (
        ['--username', '-u'],
        {'type': str, 'help': 'the username to use in logging on', 'required': True}
    ),
    (
        ['--password', '-p'],
        {'type': str, 'help': 'the password to use in logging on', 'required': True}
    )
]


@parser_command(
    'mc',
    login_arguments + [
        (
            ['--name', '-n'],
            {'type': str, 'help': 'the name of the new mod', 'required': True}
        ),
        (
            ['--desc', '-d'],
            {'type': str, 'help': 'a short description (1000 characters or less) description of the new mod', 'required': True}
        ),
        (
            ['--version', '-v'],
            {'type': str, 'help': 'the human-friendly version name or number for the first version of the new mod', 'required': True}
        ),
        (
            ['--ksp', '-k'],
            {'type': str, 'help': 'the primary version of KSP with which the new mod is compatible', 'required': True}
        ),
        (
            ['--license', '-l'],
            {
                'type': str,
                'help': 'the name or title (128 characters or less) of the license under which the new mod is released',
                'required': True
            }
        ),
        (
            ['file'],
            {'type': str, 'help': 'the zip file to upload when creating the mod'}
        )
    ],
    help='Upload a new mod to KerbalStuff'
)
def mod_create(args):
    KerbalStuff.login(args.username, args.password)

    if KerbalStuff.current_json is None:
        sys.stderr.write("Login response was not valid JSON; aborting.")
        sys.exit(1)

    if KerbalStuff.current_json['error']:
        sys.stderr.write("Error during login: {0}".format(KerbalStuff.current_json['reason']))
        sys.exit(1)

    file_path = args.file

    if os.path.isfile(file_path):
        if not is_zipfile(file_path):
            sys.stderr.write("Not a valid zip file: '{0}'\n".format(file_path))
            sys.exit(1)
        file_name = os.path.basename(file_path)
    else:
        sys.stderr.write("File does not exist: '{0}'\n".format(file_path))
        sys.exit(1)

    mod = Mod(args.name, args.desc, args.version, args.ksp, args.license)

    try:
        KerbalStuff.mod_create(mod, file_name, file_path)
        if KerbalStuff.current_json["error"]:
            sys.stderr.write("Error creating mod '{0}': {1}".format(args.name, KerbalStuff.current_json["reason"]))
            sys.exit(1)
        else:
            sys.stdout.write("Mod created!  New mod id is {0}.  You can view the new mod at {1}{2}".format(
                KerbalStuff.current_json["id"],
                KerbalStuff.constants.RootUri,
                KerbalStuff.current_json["url"]
            ))
    except TypeError as x:
        sys.stderr.write(x)
        sys.exit(1)


@parser_command(
    'mu',
    login_arguments + [
        (
            ['--mod_id', '-m'],
            {'type': str, 'help': 'the id of the mod to be updated', 'required': True}
        ),
        (
            ['--notify', '-n'],
            {'action': 'store_true', 'help': "if used, the mod's followers will be notified of this update"}
        ),
        (
            ['--changelog', '-c'],
            {'type': str, 'help': 'an optional log describing the changes in this update'}
        ),
        (
            ['--version', '-v'],
            {'type': str, 'help': 'the human-friendly version name or number for the first version of the new mod', 'required': True}
        ),
        (
            ['--ksp', '-k'],
            {'type': str, 'help': 'the primary version of KSP with which the new mod is compatible', 'required': True}
        ),
        (
            ['file'],
            {'type': str, 'help': 'the zip file to upload when creating the mod'}
        )
    ],
    help='Update an existing mod on KerbalStuff'
)
def mod_update(args):
    KerbalStuff.login(args.username, args.password)

    if KerbalStuff.current_json is None:
        sys.stderr.write("Login response was not valid JSON; aborting.")
        sys.exit(1)

    if KerbalStuff.current_json['error']:
        sys.stderr.write("Error during login: {0}".format(KerbalStuff.current_json['reason']))
        sys.exit(1)

    file_path = args.file

    if os.path.isfile(file_path):
        if not is_zipfile(file_path):
            sys.stderr.write("Not a valid zip file: '{0}'\n".format(file_path))
            sys.exit(1)
        file_name = os.path.basename(file_path)
    else:
        sys.stderr.write("File does not exist: '{0}'\n".format(file_path))
        sys.exit(1)

    if 'changelog' in args and args.changelog is not None and len(args.changelog) > 0:
        ver = ModVersion(args.version, args.ksp, args.changelog)
    else:
        ver = ModVersion(args.version, args.ksp)

    try:
        KerbalStuff.mod_update(args.mod_id, ver, args.notify, file_name, file_path)
        if KerbalStuff.current_json["error"]:
            sys.stderr.write("Error updating mod #{0}: {1}".format(args.mod_id, KerbalStuff.current_json["reason"]))
            sys.exit(1)
        else:
            sys.stdout.write("Mod updated!  New version id is {0}.  You can view the new mod version at {1}{2}".format(
                KerbalStuff.current_json["id"],
                KerbalStuff.constants.RootUri,
                KerbalStuff.current_json["url"]
            ))
    except TypeError as x:
        sys.stderr.write(x)
        sys.exit(1)


def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    sys.exit(main())