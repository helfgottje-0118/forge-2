# Forge

A simple local command runner, built independently with no Hermes code, AI model, API key, or runtime dependencies. Requires Python 3.9 or newer. Intended for Linux and macOS.

## Run immediately

```bash
git clone https://github.com/helfgottje-0118/forge-2.git
cd forge-2
python3 forge.py 'pwd && ls -la'
python3 forge.py
```

## Install the forge command

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
source .venv/bin/activate
forge 'pwd && ls -la'
forge --cwd /tmp 'touch forge-test && ls -l forge-test'
forge
```

In interactive mode, `cd /path` persists your working directory. `/pwd`, `/help`, and `/exit` are built in. Output streams directly to your terminal. Single commands return the shell's exit status.

Enter actual shell commands, not natural language. Commands execute immediately with your account's permissions. Pipes and redirects work. Each command starts a fresh shell, so exports and shell functions do not persist between prompts; combine dependent commands in one line. For full shell sessions, run `bash`.
