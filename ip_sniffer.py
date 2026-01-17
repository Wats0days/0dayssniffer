import os
import subprocess
import time
import requests
import socket
import re
from colorama import Fore, Style, init

init(autoreset=True)

RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT

BANNER = f"""{RED}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⣄⠀⠰⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⢸⡄⠀⢳⠀⠀⢀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⡄⠀⠀⢳⡄⠀⠀⠀⠀⠸⡆⡄⠀⠀⣿⠀⢸⡄⠀⠈⣇⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣄⠙⢆⠀⠀⢿⡄⠀⠀⠀⠀⣧⢸⠀⠀⣿⠀⢸⡇⠀⠀⢸⠈⡆⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣹⣧⣌⣧⣀⣸⣇⢳⡄⠀⠀⣿⢘⡇⢀⣿⠀⣸⢱⡀⠀⢸⠀⣿⠀⠀⢸⡇⠀⢀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⡿⠿⣟⠉⠉⢹⡇⢹⠁⣿⡟⠙⣿⠲⢶⣿⣸⡃⣼⠃⣰⡏⣼⠇⢀⣿⠀⣿⠀⠀⣾⠃⠀⢸⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⡿⠟⢋⡁⠠⣄⠘⣷⡀⢸⣿⣸⣤⣿⡇⣰⡿⢠⣿⢣⡟⣽⢿⣶⣿⣴⡿⢀⣼⡏⣸⡏⠀⣸⡿⠀⢀⡏⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠟⠉⢠⡀⠀⠙⣦⡘⣷⣘⣧⣿⣿⣿⣿⣿⣰⣿⣷⣿⣿⣿⣿⣿⣾⣿⣾⡿⣳⣿⣟⣴⡟⢀⣼⡿⡽⠀⡾⢠⠀⡼⠃⡼⠀⠀⣠⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⡿⠛⠁⠀⠀⢀⠙⣮⣷⣽⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣴⣿⢟⡼⣣⠞⣴⣣⡞⢁⡼⠃⢀⡴⠃⠀⣀⡄
⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⠀⠀⠀⠠⣄⠈⢷⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣟⣵⣾⡿⣋⣴⣟⣡⣶⠟⣁⣴⣾⣿⠇
⠀⠀⠀⠀⠀⠀⢀⣾⡿⠃⠀⠀⣄⠀⢳⣜⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⠟⠁⠀
⠀⠀⠀⠀⠀⢠⣿⠏⠀⢀⠀⢦⡘⢦⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⢻⣿⣿⣿⠛⠻⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⣰⡿⠃⠀⠀⢈⢶⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡖⠒⠚⣿⣿⡿⠀⠀⠀⠀⠀⠀⠈⠉⠉⢛⣿⣿⣿⣿⣿⣿⡿⣿⣿⣯⣅⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⡿⠁⠀⠀⣀⠈⢳⣾⣿⣿⣿⣿⣿⠟⣻⣿⣿⠀⢈⣿⣿⣿⣿⣿⣿⣿⠯⠍⠀⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⡿⢶⣄⠉⠛⠇⠀⠀⠀⠀⠀⠀
⠀⠀⢠⡿⠁⠀⠀⠀⠈⣿⣿⣿⣿⣿⢿⣿⡿⠤⣨⣿⣿⣿⣼⣿⣿⣿⣿⣿⡿⠏⠀⠂⠈⠛⢿⣿⠃⠀⠀⠀⠀⠀⠀⣰⣿⣿⣟⣋⣉⣉⣉⠛⠻⢷⡌⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡾⠁⠀⠀⠀⣠⣾⣿⣿⣿⠟⠁⠘⣿⣶⡧⠖⢸⡿⣿⣿⣿⣿⡿⣿⣿⠗⠀⠀⠈⢿⣦⣾⡟⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⡿⠯⢭⣍⡙⠓⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡼⠀⠀⠀⠀⣴⣿⣿⣿⠟⠀⠀⠀⠀⠹⣿⣥⢖⣠⣤⠟⠉⠛⠛⢻⠁⡀⠀⢀⣸⣷⣠⣿⡟⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣥⣤⣍⡛⠢⣄⠙⠳⣄⠉⢦⡀⠀⠀⠀⠀⠀⠀⠀
⠰⠁⠀⠀⢀⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠈⠻⣾⣽⣷⣖⡆⢀⣠⣸⣤⣿⣆⣈⣿⣿⡿⠋⠀⠀⢀⣠⣾⣿⣿⣿⣿⣭⣛⠻⢶⡀⠉⠳⢌⠳⠀⠈⠳⡄⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⣶⣿⣿⣿⣿⣿⠿⠟⠉⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣟⠿⣦⡙⠄⠀⠀⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⡿⢿⣝⡻⣟⢮⢣⠀⠙⣆⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣾⡟⠁⠀⠀⢀⣠⣴⣶⣶⣶⠷⣷⣶⣶⣶⣶⣦⣤⣤⣤⣴⣶⣶⣶⣿⣿⣿⣿⣿⣿⡻⢿⣿⢶⣍⠻⣝⢷⣌⠻⣮⠋⢧⢧⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⠋⠀⢀⣴⡾⠟⠋⠉⢠⠏⢀⡞⢩⠞⢩⡟⣹⠟⣹⠏⣿⢻⣿⢹⡿⣿⢻⢿⢿⣿⣿⣿⣦⠙⣇⠘⢧⡈⢦⠙⢧⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠐⠃⠀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠈⢠⠏⠀⡞⢠⠃⠀⢿⠀⠋⠘⡇⢸⠇⡏⢸⢸⠀⠹⣇⢳⠙⣧⠘⠀⠀⢳⡘⠆⠈⣧⠈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠈⠀⠀⠀⠇⡼⠀⠀⠏⠼⠀⠀⢻⢸⠄⠘⡆⠀⠀⠀⡇⠀⠀⠸⡄⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠘⠀⠀⠃⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def get_network_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        # Create subnet range (e.g., 192.168.1.0/24)
        subnet = '.'.join(ip.split('.')[:-1]) + '.0/24'
        return ip, subnet
    except:
        return "127.0.0.1", None

def scan_network(subnet):
    print(f"{RED}[!] SCANNING SUBNET: {subnet}...")
    # -sn is a ping scan (finds live devices without deep port scanning)
    cmd = ["nmap", "-sn", subnet]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Extract IPs and Hostnames using Regex
    devices = re.findall(r"Nmap scan report for ([\w\.-]+ )?\(?([\d\.]+)\)?", result.stdout)
    return devices

def main():
    os.system('clear')
    print(BANNER)
    subprocess.run(["termux-wake-lock"])
    print(f"{GREEN}[+] BACKGROUND WAKE LOCK ACTIVE")
    
    try:
        while True:
            my_ip, subnet = get_network_info()
            print(f"\n{RED}{'—'*60}")
            print(f"{RED}[{time.strftime('%H:%M:%S')}] YOUR IP: {my_ip}")
            
            if subnet:
                found_devices = scan_network(subnet)
                print(f"{GREEN}[+] FOUND {len(found_devices)} DEVICES CONNECTED:")
                
                for host, ip in found_devices:
                    host_name = host.strip() if host else "Unknown"
                    color = GREEN if ip == my_ip else RED
                    print(f"{color}  > {ip} [{host_name}]")
                    
                    # Log the findings
                    with open("network_discovery.log", "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {ip} ({host_name})\n")
            else:
                print(f"{RED}[!] NO LOCAL NETWORK DETECTED")

            print(f"{RED}{'—'*60}")
            time.sleep(30) # Wait 30 seconds before next discovery
            
    except KeyboardInterrupt:
        print(f"\n{RED}[!] RELEASING WAKE LOCK...")
        subprocess.run(["termux-wake-unlock"])

if __name__ == "__main__":
    main()