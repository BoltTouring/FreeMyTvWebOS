#!/usr/bin/env python3
"""
Free My TV for webOS - One-Command Installer
Automates discovery, pairing, and installation onto your LG Smart TV
"""

import os
import sys
import socket
import urllib.request
import subprocess
import shutil

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_IPK = os.path.join(REPO_DIR, "dist", "org.webos.freemytv_1.0.0_all.ipk")

def discover_lg_tv():
    print("[*] Scanning local network for LG webOS TV...")
    msg = (
        'M-SEARCH * HTTP/1.1\r\n'
        'HOST: 239.255.255.250:1900\r\n'
        'MAN: "ssdp:discover"\r\n'
        'MX: 2\r\n'
        'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n\r\n'
    ).encode('utf-8')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(2.5)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    try:
        sock.sendto(msg, ('239.255.255.250', 1900))
        while True:
            data, addr = sock.recvfrom(4096)
            ip = addr[0]
            # Probe dev port 9922
            s = socket.socket()
            s.settimeout(0.3)
            if s.connect_ex((ip, 9922)) == 0:
                s.close()
                sock.close()
                return ip
            s.close()
    except Exception:
        pass
    sock.close()
    return None

def install_app(tv_ip, passphrase=None):
    if not os.path.exists(DIST_IPK):
        print("[!] Package not found. Building first...")
        build_script = os.path.join(REPO_DIR, "scripts", "build.py")
        subprocess.run(f"python {build_script}", shell=True)

    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    raw_key = os.path.join(ssh_dir, "webos_tv_rsa")
    dec_key = os.path.join(ssh_dir, "webos_tv_rsa_decrypted")

    # Download key from TV if not present
    if not os.path.exists(dec_key):
        if not passphrase:
            passphrase = input(f"Enter the 6-character Passphrase shown in Developer Mode on TV ({tv_ip}): ").strip()

        print(f"[*] Downloading authentication key from http://{tv_ip}:9991/webos_rsa ...")
        try:
            with urllib.request.urlopen(f"http://{tv_ip}:9991/webos_rsa", timeout=5) as resp:
                key_data = resp.read()
                with open(raw_key, "wb") as f:
                    f.write(key_data)
        except Exception as e:
            print(f"[!] Failed to fetch key: {e}")
            print("[!] Make sure 'Key Server' is toggled ON in the Developer Mode app on the TV.")
            return False

        # Decrypt key
        from cryptography.hazmat.primitives import serialization
        key = serialization.load_pem_private_key(key_data, password=passphrase.encode())
        unenc = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(dec_key, "wb") as f:
            f.write(unenc)
        print("[+] SSH Key saved & decrypted successfully.")

    print(f"[*] Uploading Free My TV to TV ({tv_ip})...")
    ssh_opts = "-o StrictHostKeyChecking=no -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa"
    scp_cmd = f'scp {ssh_opts} -P 9922 -i "{dec_key}" "{DIST_IPK}" prisoner@{tv_ip}:/media/developer/temp/app.ipk'
    res = subprocess.run(scp_cmd, shell=True)
    if res.returncode != 0:
        print("[!] SCP upload failed.")
        return False

    print("[*] Installing package on TV...")
    install_cmd = 'luna-send-pub -i -u luna://com.webos.appInstallService/dev/install \'{"id":"org.webos.freemytv","ipkUrl":"/media/developer/temp/app.ipk","subscribe":true}\''
    ssh_cmd = f'ssh {ssh_opts} -p 9922 -i "{dec_key}" prisoner@{tv_ip} "{install_cmd}"'
    subprocess.run(ssh_cmd, shell=True)

    print("[*] Launching Free My TV...")
    launch_cmd = 'luna-send-pub -i -u luna://com.webos.applicationManager/launch \'{"id":"org.webos.freemytv"}\''
    subprocess.run(f'ssh {ssh_opts} -p 9922 -i "{dec_key}" prisoner@{tv_ip} "{launch_cmd}"', shell=True)

    print("\n[+] SUCCESS! Free My TV is installed and running on your LG TV! Enjoy! 🎉")
    return True

if __name__ == "__main__":
    ip = sys.argv[1] if len(sys.argv) > 1 else None
    passphrase = sys.argv[2] if len(sys.argv) > 2 else None

    if not ip:
        ip = discover_lg_tv()
        if not ip:
            ip = input("Enter TV IP Address (shown in Developer Mode app): ").strip()

    install_app(ip, passphrase)
