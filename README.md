# Telegram bots deployment guide

This project contains two Telegram bot scripts:

- fc.py — FC content bot
- smm.py — SMM/marketing bot

## 1) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 2) Configure environment

Copy the example file and fill in real values:

```bash
copy .env.example .env
```

Then update the values in .env with your actual bot tokens and API key.

## 3) Run the bot

```bash
python fc.py
```

or

```bash
python smm.py
```

## 4) Deploy to a remote server

Upload the project to your server via SSH/SFTP, install Python dependencies, then run the bot with a process manager such as systemd or PM2.

Example:

```bash
ssh user@your-server
cd /path/to/Xizmatlar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your real secrets
nohup python fc.py > fc.log 2>&1 &
```

> Important: keep the real token values in the server environment, not inside version control.
