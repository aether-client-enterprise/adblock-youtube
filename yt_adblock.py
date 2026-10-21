# language: Python 3, file: yt_adblock.py, target: Windows 10/11 x64, admin required
# technique: hosts-file redirection + GitHub raw blocklist sync + local state folder
import ctypes
import os
import sys
import urllib.request
from datetime import datetime

HOSTS = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT = "127.0.0.1"
AD_DOMAINS = [
    "pubads.g.doubleclick.net",
    "securepubads.g.doubleclick.net",
    "googlesyndication.com",
    "pagead2.googlesyndication.com",
    "tpc.googlesyndication.com",
    "video-ad-stats.googlesyndication.com",
    "adservice.google.com",
    "ad.doubleclick.net",
    "googleadservices.com",
    "www.googletagservices.com",
    "static.doubleclick.net",
    "googleads.g.doubleclick.net",
]
STATE_DIR = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), "YTAdBlock")
BLOCKLIST_FILE = os.path.join(STATE_DIR, "blocklist.txt")
LOG_FILE = os.path.join(STATE_DIR, "adblock.log")
GITHUB_RAW = "https://raw.githubusercontent.com/aether-client-enterprise/adblock-youtube/main/blocklist.txt"

def log(msg):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def load_blocklist():
    domains = set(AD_DOMAINS)
    if os.path.exists(BLOCKLIST_FILE):
        with open(BLOCKLIST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                d = line.strip().lower()
                if d and not d.startswith("#"):
                    domains.add(d)
    return domains

def sync_github(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read().decode("utf-8", errors="ignore")
        new = 0
        for line in data.splitlines():
            d = line.strip().lower()
            if d and not d.startswith("#"):
                with open(BLOCKLIST_FILE, "a", encoding="utf-8") as f:
                    f.write(d + "\n")
                new += 1
        log(f"github sync: {new} novos dominios")
    except Exception as e:
        log(f"github sync falhou: {e}")

def backup_hosts():
    bak = HOSTS + ".ytadblock.bak"
    if not os.path.exists(bak):
        with open(HOSTS, "r", encoding="utf-8", errors="ignore") as src:
            data = src.read()
        with open(bak, "w", encoding="utf-8") as dst:
            dst.write(data)

def apply_hosts(domains):
    backup_hosts()
    marker = "# YTAdBlock start"
    end_marker = "# YTAdBlock end"
    with open(HOSTS, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    out = []
    in_block = False
    for line in lines:
        if line.strip() == marker:
            in_block = True
            continue
        if line.strip() == end_marker:
            in_block = False
            continue
        if not in_block:
            out.append(line)
    out.append(marker + "\n")
    for d in sorted(domains):
        out.append(f"{REDIRECT} {d}\n")
    out.append(end_marker + "\n")
    with open(HOSTS, "w", encoding="utf-8") as f:
        f.writelines(out)

def main():
    if not is_admin():
        print("execute como administrador para gravar o hosts.")
        sys.exit(1)
    os.makedirs(STATE_DIR, exist_ok=True)
    domains = load_blocklist()
    sync_github(GITHUB_RAW)
    domains = load_blocklist()
    apply_hosts(domains)
    log(f"aplicados {len(domains)} dominios")
    print(f"bloqueados {len(domains)} dominios de anuncio do youtube.")

if __name__ == "__main__":
    main()