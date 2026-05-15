# rtsp camera scanner

![Python](https://img.shields.io/badge/Python-3.x-blue)
![RTSP](https://img.shields.io/badge/Protocol-RTSP-green)
![Made by](https://img.shields.io/badge/made%20by-%40000nico-gray)

Scans random IPs on the internet looking for exposed RTSP cameras with default credentials.

## how it works

1. threads generate random IPs and check if port 554 is open
2. IPs with open port are added to a queue
3. 40 threads take IPs from the queue and test credentials
4. Credentials are verified via raw RTSP sockets
5. If credentials pass, verifies real video with OpenCV
6. Valid streams are saved to `Desktop/cameras.txt`

## requirements
```bash
pip install opencv-python colorama
```

## usage
```bash
python scanner.py
```

## disclaimer

For educational purposes only. Only use on networks you own or have explicit permission to test.
