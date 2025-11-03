#!/usr/bin/env python3

import os
import sys
import urllib.request
import shutil
from settings import *


class AutoUpdate:
    VERSION = "0.2"
    FILES = ["upset.py", "settings.py"]
    REPO_URL = (
        "https://raw.githubusercontent.com/upsetting-god/upset-automatly-software/main"
    )
    BACKUP_DIR = ".backups"

    def __init__(self):
        self.script_path = os.path.abspath(__file__)
        os.makedirs(self.BACKUP_DIR, exist_ok=True)

    def _fetch_remote_version(self):
        try:
            with urllib.request.urlopen(f"{self.REPO_URL}/VERSION") as resp:
                return resp.read().decode("utf-8").strip()
        except Exception as e:
            print(f"[-] Failed to fetch VERSION: {e}")
            return None

    def _download_files(self):
        try:
            for fname in self.FILES:
                url = f"{self.REPO_URL}/{fname}"
                urllib.request.urlretrieve(url, fname + ".new")
            return True
        except Exception as e:
            print(f"[!] Download failed: {e}")
            for fname in self.FILES:
                tmp = fname + ".new"
                if os.path.exists(tmp):
                    os.remove(tmp)
            return False

    def run(self):
        print(f"[*] Current version: {self.VERSION}")
        remote_version = self._fetch_remote_version()
        if not remote_version:
            return

        if remote_version == self.VERSION:
            print("[i] You are up to date.")
            return

        print(f"[+] New version {remote_version} available. Updating...")
        if not self._download_files():
            print("[!] Aborted: download error.")
            sys.exit(1)

        for fname in self.FILES:
            backup_path = os.path.join(self.BACKUP_DIR, fname + ".bak")
            if os.path.exists(fname):
                shutil.copy2(fname, backup_path)
            shutil.move(fname + ".new", fname)

        print("[+] Update applied. Restarting...")
        os.execv(sys.executable, [sys.executable, self.script_path])


if __name__ == "__main__":
    subprocess.run(["mkdir", ".backups"])
    updater = AutoUpdate()
    updater.run()

    s = Main()
    s.run()
