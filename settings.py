import os
import requests
import subprocess
import shutil
import time
import sys


def is_termux():
    return "TERMUX_VERSION" in os.environ


MODULES_DIR = ".modules"


def run_go_module(filepath):
    import tempfile

    if not os.path.isfile(filepath):
        print(f"❌ File not found: {filepath}")
        return

    print(f"[▶️] Executing Go module: {os.path.basename(filepath)}")

    with tempfile.TemporaryDirectory() as tmp:
        safe_path = os.path.join(tmp, "main.go")
        shutil.copy(filepath, safe_path)

        try:
            result = subprocess.run(
                ["go", "run", "main.go"],
                cwd=tmp,
                text=True,
                capture_output=True,
                check=True,
            )
            print(result.stdout, end="")
            if result.stderr.strip():
                print("STDERR:", result.stderr, file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print("❌ Failed to run Go module:")
            print("Exit code:", e.returncode)
            if e.stdout.strip():
                print("STDOUT:\n", e.stdout)
            if e.stderr.strip():
                print("STDERR:\n", e.stderr)
        except FileNotFoundError:
            print("❌ 'go' command not found. Install Go.")


class Main:
    def run(self):
        banner = """
                                                               ░██
                                                               ░██
                ░██    ░██ ░████████   ░███████   ░███████  ░████████
                ░██    ░██ ░██    ░██ ░██        ░██    ░██    ░██
                ░██    ░██ ░██    ░██  ░███████  ░█████████    ░██
                ░██   ░███ ░███   ░██        ░██ ░██           ░██
                 ░█████░██ ░██░█████   ░███████   ░███████      ░████
                           ░██
                           ░██


                         Wake up, Neo. Follow the white rabbit.


                        [1] - OSINT
                        [2] - DOS
                        [3] - GENERATED PAYLOAD
                        [4] - INSTALL MODULES
                        [5] - USE MODULES
                        [6] - ABOUT AUTHOR
"""
        print(banner)
        choice = input("upset@software: ")
        if choice == "2":
            self.DOS()
        elif choice == "1":
            self.OSINT()
        elif choice == "3":
            payloads = Payloads()
            payloads.main()
        elif choice == "5":
            p = Modules()
            p.exec()
        elif choice == "6":
            msg = "Enter to my telegram channel https://t.me/+dX9hj3xAbF9hYTQ0 and follow the news!"

            for letter in msg:
                print(letter, end="", flush=True)
                time.sleep(0.05)
        elif choice == "4":
            s = Modules()
            s.install()
        else:
            print("Invalid option.")

    def DOS(self):
        os.system("go run dos.go")

    def OSINT(self):
        tabl = """
DOCS:

[1] - search by nickname
[2] - search by ip
"""
        print(tabl)
        choice = input("upset@software: ")
        if choice == "1":
            nick = input("enter nickname: ")
            ps = Osint()
            ps.nickname(nick=nick)
        elif choice == "2":
            ipa = input("enter ip-address: ")
            ps = Osint()
            ps.ip(ip=ipa)


class Osint:
    def nickname(self, nick, proxy=None):
        search_urls = {
            "vk": "https://vk.com/{}",
            "telegram": "https://t.me/{}",
            "instagram": "https://instagram.com/{}",
            "twitter": "https://twitter.com/{}",
            "facebook": "https://facebook.com/{}",
            "steam": "https://steamcommunity.com/id/{}",
            "github": "https://github.com/{}",
            "reddit": "https://reddit.com/user/{}",
            "twitch": "https://twitch.tv/{}",
            "youtube": "https://youtube.com/@{}",
            "tiktok": "https://tiktok.com/@{}",
            "pinterest": "https://pinterest.com/{}",
            "linkedin": "https://linkedin.com/in/{}",
            "spotify": "https://open.spotify.com/user/{}",
            "discord": "https://discord.com/users/{}",
            "medium": "https://medium.com/@{}",
            "soundcloud": "https://soundcloud.com/{}",
            "deviantart": "https://{}.deviantart.com",
            "habr": "https://habr.com/ru/users/{}/",
            "gitlab": "https://gitlab.com/{}",
            "keybase": "https://keybase.io/{}",
            "hackerrank": "https://hackerrank.com/{}",
            "leetcode": "https://leetcode.com/{}",
            "codewars": "https://codewars.com/users/{}",
            "stackoverflow": "https://stackoverflow.com/users/{}",
            "behance": "https://behance.net/{}",
            "dribbble": "https://dribbble.com/{}",
            "flickr": "https://flickr.com/people/{}",
            "vimeo": "https://vimeo.com/{}",
            "ok": "https://ok.ru/{}",
            "tumblr": "https://{}.tumblr.com",
            "wikipedia": "https://ru.wikipedia.org/wiki/User:{}",
        }
        if proxy:
            for site, link in search_urls.items():
                try:
                    full_url = link.format(nick)
                    response = requests.get(full_url, proxies=proxy, timeout=10)
                    if response.status_code == 200:
                        print(f"{site}: {full_url} -- FOUND")
                except Exception as e:
                    print(f"{site}: {full_url} -- ERROR ({str(e)})")
        else:
            for site, link in search_urls.items():
                try:
                    full_url = link.format(nick)
                    response = requests.get(full_url, timeout=10)
                    if response.status_code == 200:
                        print(f"{site}: {full_url} -- FOUND")
                except Exception as e:
                    print(f"{site}: {full_url} -- ERROR ({str(e)})")

    def ip(self, ip, proxy=None):
        try:
            api = "http://ip-api.com/json/" + str(ip)
            params = {"fields": "query,country,countryCode,city,lat,lon,org"}
            if proxy:
                response = requests.get(api, params=params, proxies=proxy, timeout=10)
            else:
                response = requests.get(api, params=params, timeout=10)
            data = response.json()
            if data.get("status") == "fail":
                print(f"Ошибка: {data.get('message')}")
                return
            msg = f"""
==== INFO ABOUT {data["query"]} ====

COUNTRY: {data["country"]}
COUNTRY CODE: {data["countryCode"]}
CITY: {data["city"]}
LAT: {data["lat"]}
LON: {data["lon"]}
ORG: {data["org"]}
            """
            print(msg)
        except Exception as e:
            print(f"ERROR: {e}")


class Payloads:
    def main(self):
        print("\n[🔍] Check avaible payloads")
        url = "https://api.github.com/users/upsetting-god/gists"

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"❌ Error: (code {response.status_code})")
                return

            gists = response.json()
            payload_files = []

            for gist in gists:
                for file_data in gist["files"].values():
                    filename = file_data["filename"]
                    if filename.startswith("payload_"):
                        payload_files.append(
                            {"filename": filename, "url": file_data["raw_url"]}
                        )

            if not payload_files:
                print("No avaible files")
                return

            print("\nAvaible payload-files:")
            for i, file in enumerate(payload_files, start=1):
                print(f"  [{i}] {file['filename']}")

            print()
            try:
                choice = int(input("Enter number for download (0 for cancel): ")) - 1
                if choice == -1:
                    print("Cancel.")
                    return
                if choice < 0 or choice >= len(payload_files):
                    print("❌ Unknown number.")
                    return
            except ValueError:
                print("❌ Please enter number.")
                return

            selected = payload_files[choice]
            filename = selected["filename"]
            raw_url = selected["url"]

            print(f"[📥] Installing '{filename}'...")
            file_response = requests.get(raw_url, timeout=10)

            if file_response.status_code == 200:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(file_response.text)
                print(f"✅: {filename}")
                if ".c" in filename:
                    print(f"[*] Unpacking {filename}")
                    gcc_path = shutil.which("gcc")
                    if gcc_path:
                        ms = """
                        [1] compiling .exe file
                        [2] compiling .out file

                        """
                        print(ms)
                        s = input("upset@software: ")
                        if s == "2":
                            output_name = filename.replace(".c", ".out")
                            subprocess.run(["gcc", filename, "-o", output_name])
                            print(".out is compiling")
                            subprocess.run(["rm", f"{filename}"])
                        elif s == "1":
                            mingw_path = shutil.which("x86_64-w64-mingw32-gcc")
                            if is_termux():
                                if not mingw_path:
                                    subprocess.run(
                                        ["pkg", "install", "mingw-w64"], check=True
                                    )
                                    mingw_path = shutil.which("x86_64-w64-mingw32-gcc")
                                if mingw_path:
                                    subprocess.run(
                                        [
                                            "x86_64-w64-mingw32-gcc",
                                            "-O2",
                                            "-s",
                                            "-static",
                                            "-o",
                                            "payload.exe",
                                            filename,
                                            "-lws2_32",
                                        ]
                                    )
                                    print(".exe is compiling")
                                    subprocess.run(["rm", f"{filename}"])
                            else:
                                if not mingw_path:
                                    subprocess.run(
                                        [
                                            "sudo",
                                            "apt",
                                            "install",
                                            "-y",
                                            "gcc-mingw-w64",
                                        ],
                                        check=True,
                                    )
                                    mingw_path = shutil.which("x86_64-w64-mingw32-gcc")
                                if mingw_path:
                                    subprocess.run(
                                        [
                                            "x86_64-w64-mingw32-gcc",
                                            "-O2",
                                            "-s",
                                            "-static",
                                            "-o",
                                            "payload.exe",
                                            filename,
                                            "-lws2_32",
                                        ]
                                    )
                                    print(".exe is compiling")
                                    subprocess.run(["rm", f"{filename}"])
            else:
                print(f"❌: {file_response.status_code}")

        except Exception as e:
            print(f"❌Error: {str(e)}")


class Modules:
    def __init__(self):
        os.makedirs(MODULES_DIR, exist_ok=True)

    def exec(self):
        print("=" * 10, "Available Modules", "=" * 10)
        try:
            md = [
                f
                for f in os.listdir(MODULES_DIR)
                if os.path.isfile(os.path.join(MODULES_DIR, f))
            ]
        except FileNotFoundError:
            print(f"Directory '{MODULES_DIR}' not found.")
            return

        if not md:
            print("No modules found.")
            return

        for i, name in enumerate(md, start=1):
            print(f"[{i}] {name}")

        print()
        try:
            choice = int(input("Choose your module → ")) - 1
            if choice < 0 or choice >= len(md):
                print("Invalid choice.")
                return
            selected = md[choice]
        except (ValueError, KeyboardInterrupt):
            print("Cancelled.")
            return

        path = os.path.join(MODULES_DIR, selected)

        if selected.endswith(".py"):
            print(f"[▶️] Executing Python module: {selected}")
            try:
                with open(path, encoding="utf-8") as f:
                    code = f.read()
                exec(code, {"__file__": path})
            except Exception as e:
                print(f"❌ Python execution failed: {e}")

        elif selected.endswith(".sh"):
            print(f"[^] Executing Bash module: {selected}")
            try:
                import subprocess

                result = subprocess.run(["bash", path], text=True, capture_output=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print("STDERR:", result.stderr, file=sys.stderr)
                if result.returncode != 0:
                    print(f"❌ Bash script failed (exit {result.returncode})")
            except Exception as e:
                print(f"❌ Bash execution failed: {e}")
        elif selected.endswith(".c"):
            print(f"[^] Compiling {selected} module..")
            nm_md = selected.strip(".c")
            import subprocess as sp

            sp.run(["gcc", f"./.modules/{selected}", "-o", f"module_{nm_md}"])
            print("[*] Compilation is successful")
            print(f"[*] Executing .c module: {selected}")
            sp.run([f"./module_{nm_md}"])
        elif selected.endswith(".go"):
            print(f"[*] Executing Go module: {selected}")
            run_go_module(f"./.modules/{selected}")
        else:
            print(f"⚠️ Unknown type: {selected}")

    def install(self):
        print("[💻] Checking available modules...")
        url = "https://api.github.com/users/upsetting-god/gists"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            gists = resp.json()
        except Exception as e:
            print(f"Failed to fetch gists: {e}")
            return

        files = []
        for gist in gists:
            for f in gist.get("files", {}).values():
                name = f.get("filename", "")
                raw = f.get("raw_url")
                if name.startswith("module_") and raw:
                    files.append({"filename": name, "url": raw})

        if not files:
            print("No modules available.")
            return

        print("\nAvailable modules:\n")
        for i, f in enumerate(files, start=1):
            print(f"[{i}] {f['filename']}")

        print()
        try:
            inp = input("Enter number (0 to cancel): ").strip()
            if not inp.isdigit():
                print("Invalid input.")
                return
            n = int(inp)
            if n == 0:
                print("Cancelled.")
                return
            if n < 1 or n > len(files):
                print("Invalid number.")
                return
            selected = files[n - 1]
        except KeyboardInterrupt:
            print("Cancelled.")
            return

        filename = selected["filename"]
        filepath = os.path.join(MODULES_DIR, filename)
        print(f"[📥] Downloading '{filename}'...")

        try:
            r = requests.get(selected["url"], timeout=10)
            r.raise_for_status()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"✅ Installed: {filename}")
        except Exception as e:
            print(f"Installation failed: {e}")


if __name__ == "__main__":
    app = Main()
    app.run()
