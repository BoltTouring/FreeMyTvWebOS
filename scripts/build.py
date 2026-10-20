#!/usr/bin/env python3
"""
Free My TV for webOS - Build Script
Packages the webOS application into a distributable .ipk file
"""

import os
import sys
import json
import shutil
import subprocess

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(REPO_DIR, "app")
DIST_DIR = os.path.join(REPO_DIR, "dist")

def read_appinfo():
    with open(os.path.join(APP_DIR, "appinfo.json"), "r", encoding="utf-8") as f:
        info = json.load(f)
    return info["id"], info["version"]

def ipk_filename(app_id, version):
    return f"{app_id}_{version}_all.ipk"

def build():
    os.makedirs(DIST_DIR, exist_ok=True)
    app_id, version = read_appinfo()
    print(f"[*] Packaging Free My TV from {APP_DIR}...")

    # Check if ares-package is available
    has_ares = shutil.which("ares-package") is not None
    if has_ares:
        cmd = f'ares-package "{APP_DIR}" -o "{DIST_DIR}"'
        print(f"[*] Running: {cmd}")
        res = subprocess.run(cmd, shell=True)
        if res.returncode == 0:
            print(f"[+] Successfully built package in {DIST_DIR}!")
            return True
        else:
            print("[!] ares-package failed, trying fallback packager...")

    # Fallback pure-python packager if ares-package is missing
    print("[*] Using built-in Python IPK packager...")
    import tarfile
    import io
    
    control_content = f"""Package: {app_id}
Version: {version}
Section: misc
Priority: optional
Architecture: all
Maintainer: FreeMyTV
Description: A fast, ad-free 60fps home screen for LG webOS TVs.
"""
    # 1. control.tar.gz
    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode="w:gz") as tar:
        ti = tarfile.TarInfo(name="control")
        ti.size = len(control_content)
        tar.addfile(ti, io.BytesIO(control_content.encode("utf-8")))
    control_bytes = control_buf.getvalue()

    # 2. data.tar.gz
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        for root, _, files in os.walk(APP_DIR):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, APP_DIR)
                dest_p = f"/usr/palm/applications/{app_id}/{rel_p.replace(os.sep, '/')}"
                tar.add(full_p, arcname=dest_p)
    data_bytes = data_buf.getvalue()

    # 3. debian-binary
    debian_binary = b"2.0\n"

    # 4. Standard ar archive
    ipk_path = os.path.join(DIST_DIR, ipk_filename(app_id, version))
    with open(ipk_path, "wb") as f:
        f.write(b"!<arch>\n")
        def write_ar_entry(name, data):
            hdr = f"{name:<16}{'0':<12}{'0':<6}{'0':<6}{'100644':<8}{len(data):<10}`\n".encode("latin1")
            f.write(hdr)
            f.write(data)
            if len(data) % 2 != 0:
                f.write(b"\n")
        write_ar_entry("debian-binary", debian_binary)
        write_ar_entry("control.tar.gz", control_bytes)
        write_ar_entry("data.tar.gz", data_bytes)

    print(f"[+] Successfully built fallback IPK: {ipk_path}")
    return True

if __name__ == "__main__":
    build()
