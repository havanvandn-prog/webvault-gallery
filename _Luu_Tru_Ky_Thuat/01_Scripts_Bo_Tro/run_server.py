# -*- coding: utf-8 -*-
"""
Smart Local Server Runner cho WebVault (v2.0 — Tích hợp 1-Click Sync API)
- Tự động dò tìm cổng trống
- Tự động mở trình duyệt sau khi máy chủ đã sẵn sàng
- Khóa cứng thư mục gốc dự án
- TÍCH HỢP DIRECT SYNC API: Nhấn nút trên web tự động nạp mẫu vào index.html & đẩy lên GitHub Pages
"""

import os
import sys
import socket
import webbrowser
import threading
import time
import json
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Xác định thư mục gốc dự án
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(BASE_DIR)

# Import sync handler
sys.path.append(os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro"))
try:
    from sync_handler import sync_approved_items_to_hub
except ImportError:
    sync_approved_items_to_hub = None

def find_free_port(preferred_ports=[8000, 8081, 9000, 9999, 7860, 5173]):
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    for port in range(8001, 8999):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return 8000

class WebVaultRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Bật CORS cho toàn bộ response để file:/// hoặc localhost đều gọi được
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith('/api/sync-approved'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                approved_items = data.get('approved_items', [])
                industry_slug = data.get('industry_slug', 'decor-su-kien')
                industry_name = data.get('industry_name', 'Trang Trí & Decor Tiệc')

                print(f"[*] Nhan yeu cau dong bo tu trinh duyet: {len(approved_items)} mau...")
                if sync_approved_items_to_hub:
                    res = sync_approved_items_to_hub(approved_items, industry_slug, industry_name)
                else:
                    res = {"success": False, "error": "Chưa nạp được module sync_handler"}

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
            return
        
        super().do_POST()

    def log_message(self, format, *args):
        # Chỉ in log khi có lỗi hoặc khi gọi API
        if "api" in str(args) or "404" in str(args) or "500" in str(args):
            sys.stderr.write(f"[*] {format % args}\n")

def open_browser_delayed(url):
    time.sleep(0.8)
    print(f"[*] Dang tu dong mo trinh duyet: {url}")
    webbrowser.open(url)

def main():
    port = find_free_port()
    url = f"http://localhost:{port}/web_nhap_staging.html"

    print("====================================================================")
    print("   WEBVAULT - KHO MAU WEBSITE CAO CAP (DARK ZEIT EDITION v2.0)")
    print("====================================================================")
    print(f"[*] Thu muc web: {BASE_DIR}")
    print(f"[+] May chu Localhost dang chay tai: {url}")
    print("[+] Tinh nang: DA KICH HOAT DIRECT SYNC API (1-Click Dong Bo Tu Dong)")
    print("--------------------------------------------------------------------")
    print("[!] Luu y: Giu cua so nay mo trong khi ban dang xem va duyet website.")
    print("    (Nhan Ctrl + C hoac dong cua so nay de tat may chu)")
    print("====================================================================\n")

    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    TCPServer.allow_reuse_address = True
    with TCPServer(("127.0.0.1", port), WebVaultRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Da tat may chu WebVault an toan.")

if __name__ == "__main__":
    main()
