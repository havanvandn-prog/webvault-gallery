# -*- coding: utf-8 -*-
"""
Smart Local Server Runner cho WebVault
- Tự động dò tìm cổng (port) trống (tránh trùng port 8080 của hệ thống)
- Tự động mở trình duyệt sau khi máy chủ đã sẵn sàng
- Khóa cứng thư mục gốc dự án
"""

import os
import sys
import socket
import webbrowser
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Xác định thư mục gốc dự án
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(BASE_DIR)

def find_free_port(preferred_ports=[8000, 8081, 9000, 9999, 7860, 5173]):
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    # Dò quét tự do
    for port in range(8001, 8999):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return 8000

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Chỉ in log khi có lỗi để màn hình console sạch sẽ
        if "404" in str(args) or "500" in str(args):
            sys.stderr.write(f"[-] {format % args}\n")

def open_browser_delayed(url):
    time.sleep(0.8)
    print(f"[*] Dang tu dong mo trinh duyet: {url}")
    webbrowser.open(url)

def main():
    port = find_free_port()
    url = f"http://localhost:{port}/index.html"

    print("====================================================================")
    print("   WEBVAULT - KHO MAU WEBSITE CAO CAP (DARK ZEIT EDITION)")
    print("====================================================================")
    print(f"[*] Thu muc web: {BASE_DIR}")
    print(f"[+] May chu Localhost dang chay tai: {url}")
    print("[+] Tinh nang: Da mo khoa quyen Copy anh 1-Click sang Facebook/Zalo")
    print("--------------------------------------------------------------------")
    print("[!] Luu y: Giu cua so nay mo trong khi ban dang xem website.")
    print("    (Nhan Ctrl + C hoac dong cua so nay de tat may chu)")
    print("====================================================================\n")

    # Mở trình duyệt trên luồng riêng
    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    TCPServer.allow_reuse_address = True
    with TCPServer(("127.0.0.1", port), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Da tat may chu WebVault an toan.")

if __name__ == "__main__":
    main()
