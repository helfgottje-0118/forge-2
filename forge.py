#!/usr/bin/env python3
"""Forge: a small local command runner. Python standard library only."""
import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time


BANNER = (
    "FFFFF  OOO  RRRR   GGG  EEEEE",
    "F     O   O R   R G     E",
    "FFFF  O   O RRRR  G GGG EEEE",
    "F     O   O R  R  G   G E",
    "F      OOO  R   R  GGG  EEEEE",
)


def paint(text, color="36"):
    if sys.stdout.isatty() and "NO_COLOR" not in os.environ:
        return f"\033[{color}m{text}\033[0m"
    return text


def panel(title, lines):
    width = max(20, min(78, shutil.get_terminal_size((80, 24)).columns - 2))
    title = f" {title} "[:width - 4]
    print(paint("╭─" + title + "─" * (width - len(title) - 3) + "╮", "33"))
    for line in lines:
        for start in range(0, max(1, len(line)), width - 4):
            chunk = line[start:start + width - 4]
            print(paint("│", "33") + " " + chunk.ljust(width - 4) + " " + paint("│", "33"))
    print(paint("╰" + "─" * (width - 2) + "╯", "33"))


def welcome():
    print()
    panel("FORGE", [*BANNER, "", "Local command runner · v0.1.0",
                    "Type a shell command to execute it.",
                    "/help  /pwd  /clear  /exit"])
    print()


def run(command, cwd):
    try:
        return subprocess.run(command, shell=True, cwd=cwd).returncode
    except KeyboardInterrupt:
        return 130
    except OSError as exc:
        print(f"forge: {exc}", file=sys.stderr)
        return 1


def interactive(cwd):
    try:
        import readline  # Native line editing and session history on Unix.
    except ImportError:
        pass
    welcome()
    last_code = 0
    while True:
        try:
            print(paint(f"  FORGE │ local shell │ {cwd} │ exit {last_code}", "2"))
            command = input(paint("❯ ", "33")).strip()
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
            panel("Help", ["Commands run immediately with your user's permissions.",
                           "cd PATH  Change directory (quote paths with spaces)",
                           "/pwd     Show current directory",
                           "/clear   Clear screen and show the banner",
                           "/exit    Quit Forge",
                           "Each command uses a fresh shell; exports do not persist."])
            continue
        if command == "/clear":
            if sys.stdout.isatty():
                print("\033[2J\033[H", end="")
            welcome()
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
        print(paint("─" * max(20, min(78, shutil.get_terminal_size((80, 24)).columns - 2)), "2"))
        started = time.monotonic()
        last_code = run(command, cwd)
        elapsed = time.monotonic() - started
        status = "Completed" if last_code == 0 else "Failed"
        print(paint(f"  {status} │ exit {last_code} │ {elapsed:.2f}s", "32" if last_code == 0 else "31"))
        print()


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
