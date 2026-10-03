#!/usr/bin/env python3
"""Forge: a small local command runner. Python standard library only."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


def run(command, cwd):
    try:
        return subprocess.run(command, shell=True, cwd=cwd).returncode
    except KeyboardInterrupt:
        return 130
    except OSError as exc:
        print(f"forge: {exc}", file=sys.stderr)
        return 1


def interactive(cwd):
    print("Forge — enter shell commands. Use cd, /pwd, /help, or /exit.")
    while True:
        try:
            command = input(f"forge:{cwd}> ").strip()
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            continue
        if not command:
            continue
        if command in ("/exit", "exit", "quit"):
            return 0
        if command == "/help":
            print("Commands run immediately with your user's permissions.\n"
                  "cd PATH changes Forge's directory; /pwd shows it; /exit quits.\n"
                  "Each command uses a fresh shell; environment changes do not persist.")
            continue
        if command == "/pwd":
            print(cwd)
            continue
        if command == "cd" or command.startswith("cd "):
            try:
                parts = shlex.split(command)
                if len(parts) > 2:
                    raise ValueError("use cd with a single path (quote spaces)")
                target = Path(os.path.expandvars(os.path.expanduser(parts[1]))) if len(parts) == 2 else Path.home()
                target = (cwd / target).resolve()
                if not target.is_dir():
                    raise ValueError(f"not a directory: {target}")
                cwd = target
            except ValueError as exc:
                print(f"forge: {exc}", file=sys.stderr)
            continue
        code = run(command, cwd)
        if code:
            print(f"[exit {code}]", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Run shell commands with Forge.")
    parser.add_argument("command", nargs="?", help="quoted shell command; omit for interactive mode")
    parser.add_argument("--cwd", default=".", help="working directory (default: current directory)")
    args = parser.parse_args()
    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        parser.error(f"not a directory: {cwd}")
    return run(args.command, cwd) if args.command is not None else interactive(cwd)


if __name__ == "__main__":
    sys.exit(main())
