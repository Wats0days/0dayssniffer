import os
import subprocess
import time
import requests
import socket
import uuid
import re
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Styling Constants
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
RESET = Style.RESET_ALL

# Blood Red ASCII Art
BANNER = f"""{RED}
⣿⡟⢠⣿⣯⠦⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠈⠂⠀⠀⠀⠀⠀⠀⠀⠑⠐⠀⠀⠀⠀⠀⠀⠸⡀⠀
⣿⢇⡿⣭⡦⠗⠁⠄⠂⠀⠀⠀⠀⠀⡠⣰⢀⠀⠀⠀⢰⠋⡆⢀⢠⠀⠀⠀⠀⠀⠐⢆⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠁⠀
⣟⠘⣼⣎⠕⠊⠁⠀⠀⠀⢢⠆⡀⠬⡑⢿⣻⡆⠀⡀⡄⠄⣧⢸⡈⢀⠀⡆⢠⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⠸⡩⡠⡔⢱⢀⠰⣄⠔⠁⣻⣢⢙⣿⣼⣿⣷⠴⠿⣿⡗⣟⣿⡿⣷⣾⣤⣼⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠁⠈⠔⢱⢌⢿⢢⠑⠻⣗⠎⣀⣿⣟⢛⣍⣯⣿⣧⣤⣿⣧⣿⣿⣵⣾⣿⣎⡹⠿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢾⢱⣷⣷⡢⢾⣷⢯⣽⣽⣿⣿⠿⣿⣛⡿⠯⠿⠿⠿⡿⠿⣿⣿⣿⣿⣿⣿⣽⣟⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⠑⢬⣧⣻⣽⣽⣿⣿⣿⣿⢟⣻⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⣽⢿⡙⢿⣿⣿⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠳⢜⢿⣿⣿⢿⣿⣿⡿⣩⠋⠄⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣄⡀⠀⠀⠈⠻⣮⡟⠙⠹⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⢀⡀⠉⢟⡻⢛⣿⠿⡷⠁⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠹⣿⣷⣦⣱⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠚⣋⠶⣋⡵⢏⣰⠁⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢬⣷⣶⣽⣿⣦⡉⢡⠀⠀⠀⠀⠀⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⢄⡀⠀⠀
⠀⠀⠀⡨⠟⠉⠉⣉⠻⣿⡌⢆⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢔⣿⣽⣿⣿⣿⣿⣿⣤⠑⢶⡄
⠀⠀⠐⠁⠀⢠⡪⠒⣚⣻⣶⣄⠳⣠⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠐⣾⣿⣿⣿⣿⣿⣿⣿⣿⣱⣼⣯
⠀⠀⠀⢀⣔⢡⡴⢛⣳⡼⠿⢿⣧⣬⣑⠤⣀⡀⠉⠻⢿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⣀⣀⣤⣾⣿⣿⣿⡿⣿⣿⠿⠿⢿⢿⡿⠠
⠀⠀⠀⠉⠊⡝⠨⠋⠀⢀⡤⣾⣟⡻⣿⢷⣶⣬⣭⣐⣤⣄⢀⣈⣀⠀⡠⢄⡦⣤⡛⠩⣿⢛⣻⢿⢛⡼⠾⠝⡅⠭⠪⠴⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⠖⢛⢜⡩⠔⠋⣉⢔⠟⢪⡿⣫⠛⢿⣿⣿⡧⠉⣿⠎⠺⣾⠁⠃⣻⠑⠠⠂⠑⢒⢁⠤⠐⡄⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠐⠁⠀⠉⠁⠀⠀⣪⠼⠃⢠⠿⠈⢼⢀⣾⠯⢿⠂⢑⢸⠢⠂⠃⠀⠀⠐⡘⠄⢠⠔⠓⢙⡥⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⠀⠀⠇⠀⠃⠀⠘⢀⢉⠁⢀⢀⠀⡀⠀⠀⢔⠺⢽⠪⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⡀⢀⡅⠤⠀⠈⢤⠐⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⠈⠰⠓⢀⠄⠇⠺⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠁⠀⠀⠀⠴⠠⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                             ZANE WAS HERE 
"""

def acquire_wakelock():
    try:
        subprocess.run(["termux-wake-lock"], check=True)
        print(f"{GREEN}[+] SYSTEM WAKE LOCK: ACQUIRED")
    except Exception:
        print(f"{RED}[!] WAKE LOCK FAILED: RUN 'pkg install termux-api'")

def get_mac():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return mac.upper()

def check_ports(ip):
    # Common PT ports: 21(FTP), 22(SSH), 80(HTTP), 443(HTTPS), 3389(RDP)
    ports = [21, 22, 80, 443, 3389]
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((ip, port))
        if result == 0:
            open_ports.append(str(port))
        s.close()
    return ", ".join(open_ports) if open_ports else "NONE"

def get_network_data():
    hostname = socket.gethostname()
    # Private IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        status = "ALIVE"
    except:
        private_ip = "127.0.0.1"
        status = "DEAD"

    # Public IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
    except:
        public_ip = "OFFLINE"

    return hostname, private_ip, public_ip, status

def main():
    os.system('clear')
    print(BANNER)
    
    # Initialization (Green)
    acquire_wakelock()
    mac_addr = get_mac()
    print(f"{GREEN}[+] HARDWARE ID (MAC): {mac_addr}")
    print(f"{GREEN}[+] TARGETING LOCALHOST...")
    print(f"{RED}{'—'*60}")
    
    try:
        while True:
            host, priv, pub, alive = get_network_data()
            ports = check_ports(priv)
            timestamp = time.strftime("%H:%M:%S")
            
            # The "Blood Red" Data Stream
            log_line = (
                f"{RED}[{timestamp}] {RED}STATUS:{alive} | "
                f"{RED}HOST:{host} | "
                f"{RED}PRV:{priv} | "
                f"{RED}PUB:{pub} | "
                f"{RED}OPEN:{ports}"
            )
            
            print(log_line)
            
            # Save log locally
            with open("pt_scan.log", "a") as f:
                f.write(log_line + "\n")
                
            time.sleep(10) # Scanning frequency
    except KeyboardInterrupt:
        print(f"\n{RED}[!] KILLING PROCESS... RELEASING WAKE LOCK.")
        subprocess.run(["termux-wake-unlock"])

if __name__ == "__main__":
    main()