# -*- coding: utf-8 -*-
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import verify_url_health, verify_captured_image

def main():
    print("=== TEST 1: KIỂM ĐỊNH SỨC KHỎE URL & DOMAIN GUARD ===")
    # 1. Test domain expired (gudecorate.com)
    ok1, reason1, _, _ = verify_url_health("https://gudecorate.com/")
    print(f"gudecorate.com: Healthy={ok1} | Reason={reason1}")
    assert not ok1, "Expired domain should be detected as unhealthy"

    # 2. Test live domain (theplannersvn.com)
    ok2, reason2, _, title2 = verify_url_health("https://theplannersvn.com/")
    print(f"theplannersvn.com: Healthy={ok2} | Reason={reason2} | Title={title2[:40]}")
    assert ok2, "Valid domain should be detected as healthy"

    print("\n=== TEST 2: KIỂM ĐỊNH TOÀN DIỆN 20 ẢNH STAGING BẰNG POST-CAPTURE QA ===")
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const CANDIDATES = (\[.*?\]);', html, re.DOTALL)
    data = json.loads(m.group(1))

    all_pass = True
    for item in data:
        full_path = item['full']
        is_valid, msg = verify_captured_image(full_path)
        print(f"[{item['id']}] {item['short_name']:<18} -> Valid: {is_valid} | {msg}")
        if not is_valid:
            all_pass = False

    assert all_pass, "All staging images must pass post-capture QA!"
    print("\nALL CAPTURE ENGINE V2 TESTS PASSED 100%!")

if __name__ == '__main__':
    main()
