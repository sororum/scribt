#!/usr/bin/python

import argparse
import getpass
import os
import sys


class colors:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"


parser = argparse.ArgumentParser(
    prog="bvlk",
    description="Yet another bulk rename utility.",
    epilog="By default, it only affects files (that are not hidden), when no argument is passed.",
)
parser.add_argument("-f", "--files", action="store_true", help="include files")
parser.add_argument("-d", "--dirs", action="store_true", help="include directories")
parser.add_argument("-i", "--hidden_files", action="store_true", help="include hidden files")
parser.add_argument("-o", "--hidden_dirs", action="store_true", help="include hidden directories")
parser.add_argument("path", help="specify target path", action="store", type=str)

args = parser.parse_args()

if args.path == ".":
    exec_dir = os.getcwd()
elif args.path == "..":
    exec_dir = os.path.dirname(os.getcwd())
elif not args.path == "." and os.path.isdir(args.path):
    exec_dir = args.path
else:
    print(colors.BOLD + f"{colors.RED}Directory is not valid!")
    sys.exit()

pwd = os.listdir(exec_dir)
username = getpass.getuser()

normal_files = next(os.walk(exec_dir))[2]
hidden_files = [i for i in normal_files if i.startswith(".")]
# only one level of sub directories
normal_sub_dirs = next(os.walk(exec_dir))[1]
hidden_sub_dirs = [i for i in normal_sub_dirs if i.startswith(".")]


def randint():
    r = os.urandom(6).hex()
    return r


def read_dir():
    print(f"{colors.BOLD}In the current directory:{colors.ENDC} {exec_dir}")
    print(
        f"""    {colors.CYAN}{len(normal_files)}{colors.ENDC} 📄 in total, {colors.PURPLE}{len(hidden_files)}{colors.ENDC} of which are hidden.
    {colors.CYAN}{len(normal_sub_dirs)}{colors.ENDC} 📁 in total, {colors.PURPLE}{len(hidden_sub_dirs)}{colors.ENDC} of which are hidden."""
    )


def rename(f):
    old_name, ext = os.path.splitext(f)
    new_name = randint()
    source_rename = f"{exec_dir}/{old_name}{ext}"
    normal_rename = f"{exec_dir}/{new_name}{ext}"
    hidden_rename = f"{exec_dir}/.{new_name}{ext}"
    argument = any((args.dirs, args.hidden_files, args.hidden_dirs))

    normal_renamed = (
        colors.BOLD
        + f"{f}{colors.PURPLE} -> {colors.ENDC}"
        + f"{colors.CYAN}{new_name}{ext}{colors.ENDC}"
        + colors.ENDC
    )
    hidden_renamed = (
        colors.BOLD
        + f"{f}{colors.PURPLE} -> {colors.ENDC}"
        + f"{colors.CYAN}.{new_name}{ext}{colors.ENDC}"
        + colors.ENDC
    )

    if (
        not old_name.startswith(".")
        and os.path.isfile(f)
        and (not argument or args.files)
    ):
        os.rename(source_rename, normal_rename)
        print(normal_renamed)
    elif not old_name.startswith(".") and os.path.isdir(f) and args.dirs:
        os.rename(source_rename, normal_rename)
        print(normal_renamed)
    elif old_name.startswith(".") and os.path.isfile(f) and args.hidden_files:
        os.rename(source_rename, hidden_rename)
        print(hidden_renamed)
    elif old_name.startswith(".") and os.path.isdir(f) and args.hidden_dirs:
        os.rename(source_rename, hidden_rename)
        print(hidden_renamed)


def main():
    script_name = "bvlk.py"

    if script_name not in pwd:
        for f in pwd:
            rename(f)
    else:
        pwd.append(pwd.pop(pwd.index(script_name)))
        print(
            f"{colors.YELLOW}\nThe script is potentially in the directory. {colors.BOLD}Ignored!{colors.ENDC}{colors.ENDC}"
        )
        pwd.remove(script_name)
        for f in pwd:
            rename(f)


def prompt():
    prompt_input = input(
        f"{colors.BOLD}{colors.UNDERLINE}Proceed?{colors.ENDC} {colors.BOLD}[y/N] {colors.ENDC}"
    )
    if prompt_input.casefold().strip() == "y":
        main()
    elif prompt_input.casefold().strip() == "n" or not prompt_input.strip():
        sys.exit()
    else:
        print(f"{colors.YELLOW}Input incomprehensible.", file=sys.stderr)


try:

    if not exec_dir.startswith("/home/") or exec_dir.endswith("/home/"):
        print(
            colors.BOLD
            + f"{colors.YELLOW}Prohibited directory.{colors.ENDC} {colors.RED}Abborted!"
            + colors.ENDC
        )
        sys.exit()

    elif exec_dir.endswith(f"/home/{username}"):
        read_dir()
        print(
            colors.BOLD
            + f"{colors.YELLOW}Running in the XDG User Directories!{colors.ENDC}"
            + colors.ENDC
        )
        prompt()

    else:
        read_dir()
        prompt()

except (KeyboardInterrupt, SystemExit):
    print(colors.BOLD + f"\n{colors.RED}❌Canceled...!{colors.ENDC}" + colors.ENDC)
    sys.exit()
