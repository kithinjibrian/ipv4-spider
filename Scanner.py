import asyncio
import os
import sys
sys.path.append('./data')

import nmap
import ipaddress
import random
import subprocess
import webbrowser

from db import DB

class Scan:
    def __init__(self,noofips=3000):
        self.db = DB("./data/sqldb/.sqlite3","./data/scripts")
        self.noofips = noofips
        self.ips = []
        self.results = {}

    def genip(self):
        while len(self.ips) < self.noofips:
            ip = ".".join(str(random.randint(0,255)) for _ in range(4))
            try:
                ip_obj = ipaddress.IPv4Address(ip)
                if ip_obj.is_global:
                    self.ips.append(ip)
            except ipaddress.AddressValueError:
                pass
    
    def ping_ip(self,ip):
        try:
            result = subprocess.run(["ping", "-c", "1", "-w", "1", ip], capture_output=True, text=True, check=True)
            if "1 received" in result.stdout:
                self.results[ip] = {"scan":{}}
                self.db.add_ip(ip)
                print(f"{ip} is alive!")
            else:
                print(f"{ip} is not alive.")
        except subprocess.CalledProcessError:
            print(f"{ip} ping failed.")

    def ping_ips(self):
        for ip in self.ips:
            if self.db.ip_exists(ip):
                print(f"{ip} already exists in the database.")
                continue
            self.ping_ip(ip)

    def scan(self):
        for ip in self.results:
            try:
                print(f"Scanning {ip}...")
                nm = nmap.PortScanner()
                nm.scan(ip, arguments="-sC -sV -T4")
                for host in nm.all_hosts():
                    portd = {}
                    for port in nm[host]['tcp']:
                        portd[port] = nm[host]['tcp'][port]
                        self.db.add_scan_data(
                            ip,
                            port,
                            portd[port]['state'],
                            portd[port]['reason'],
                            portd[port]['name'],
                            portd[port]['product'],
                            portd[port]['version'],
                            portd[port]['extrainfo'],
                            portd[port]['conf'],
                            portd[port]['cpe'],
                            portd[port].get('script', '') # use empty string as default value if 'script' key doesn't exist
                        )
                    self.results[ip]['scan'] = portd
            except Exception as e:
                pass


    async def run(self):
        self.genip()
        self.ping_ips()
        self.scan()

###################################################
async def server():
    print("Opening web server...........")
    os.chdir("./server/b")
    proc = await asyncio.create_subprocess_exec(
        "npm","start",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

async def openbrowser():
    print("Page loading in browser......")
    webbrowser.open_new_tab("http://localhost:3001")

async def main():
    scan = Scan()
    await asyncio.gather(scan.run())

###################################################
asyncio.run(main())