#!/bin/bash

main() {
    if command -v go &> /dev/null; then
        echo "[+] golang is install"
    else
        echo "[-] golang not found, installing.."
        if [ -n "$TERMUX_VERSION" ]; then
            pkg install -y golang
        else
            sudo apt install -y golang
        fi
    fi
    if command -v python3 &> /dev/null; then
        echo "[+] python3 is install"
    else
        echo "[-] python3 not found, installing.."
        if [ -n "$TERMUX_VERSION" ]; then
            pkg install -y python3 python3-pip
        else
            sudo apt install -y python3 python3-pip
        fi
    fi

    pip install -r requiments.txt &> /dev/null
    chmod +x ./upset.py
    echo "for the next launch use ./upset.py"
    python3 upset.py
}

main
