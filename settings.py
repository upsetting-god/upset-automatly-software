import os
import requests
import subprocess
import shutil
import time


def is_termux():
    return "TERMUX_VERSION" in os.environ


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
                        [4] - ABOUT AUTHOR
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
        elif choice == "4":
            msg = "Enter to my telegram channel https://t.me/+dX9hj3xAbF9hYTQ0 and follow the news!"

            for letter in msg:
                print(letter, end="", flush=True)
                time.sleep(0.05)
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


if __name__ == "__main__":
    app = Main()
    app.run()
