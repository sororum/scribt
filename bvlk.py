#!/usr/bin/python

import getpass
import os
import sys

exec_dir = os.getcwd()
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
    print(f"In the current directory: {exec_dir}")
    print(
        f"""    {len(normal_files)} 📄 in total, {len(hidden_files)} of which are hidden.
    {len(normal_sub_dirs)} 📁 in total, {len(hidden_sub_dirs)} of which are hidden."""
    )


def rename(f):
    old_name, ext = os.path.splitext(f)
    new_name = randint()

    if not old_name.startswith("."):
        os.rename(f"{exec_dir}/{old_name}{ext}", f"{exec_dir}/{new_name}{ext}")
        print(f"{f} -> {new_name}{ext}")

    else:
        os.rename(f"{exec_dir}/{old_name}{ext}", f"{exec_dir}/.{new_name}{ext}")
        print(f"{f} -> .{new_name}{ext}")


def main():
    script_name = "bvlk.py"

    if script_name not in pwd:
        for f in pwd:
            rename(f)
    else:
        pwd.append(pwd.pop(pwd.index(script_name)))
        print("\nThe script is potentially in the directory. Ignored!")
        pwd.remove(script_name)
        for f in pwd:
            rename(f)


def prompt(inp):
    if inp == "y":
        main()
    elif inp == "n" or " ":
        sys.exit()
    else:
        print("Input incomprehensible.")
        sys.exit()


try:

    if not exec_dir.startswith("/home/") or exec_dir.endswith("/home/"):
        print("Prohibited directory. Abborted!")
        sys.exit()

    elif exec_dir.endswith(f"/home/{username}"):
        read_dir()
        print("Running in the XDG User Directories!")

        prompt_input = input("Proceed? [y/N] ")
        prompt(prompt_input)

    else:
        read_dir()
        prompt_input = input("Proceed? [y/N] ")
        prompt(prompt_input)

except (KeyboardInterrupt, SystemExit):
    print("\n❌Canceled...!")
    sys.exit()
