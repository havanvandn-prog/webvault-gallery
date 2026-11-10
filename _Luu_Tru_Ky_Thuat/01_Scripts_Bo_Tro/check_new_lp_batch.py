# -*- coding: utf-8 -*-
import sys, re, requests
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

redirects = [
    ("Sylnet Webflow", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFeFROGMTTY26eGMett_yH53K__SMtLHncmFnAQh9lVMYTZ36hq1PDx22XNRZXjK9VSXtSqV4DjEF7cFVoBZvt3KQ3ZkWvXrcV1dwYth415VzjChyj28vFF_0hFdLIxsRDlYB1ktk4YjGAgkeVzUl2UfD4="),
    ("Tillman Fiber", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDPaG_cDaYTcAPpvY_3owZmltv1RSsjoBDYdIjz7A_Hmr85GM9iinGh__LWbGks887kJS1mtbPQrQU5_YIRiLsH0gYHpP7WWSkZy8LGmzzv3XFP938"),
    ("CBN Fiber Framer", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZjESmrTLrvLIr7EEbkhFtbpDoOZb5ZJjvkrhQoMf0TxAhay3IccQuxe0lt8l-idadT6roL57RbgqALIcDKdeaErgiHpr1brLgcVDXNWOb2_KDI4wcnvRun85gdEE="),
    ("Stallion Network Framer", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH_HzN-7K0mqmLyqnpMZwARLLgJCo7a3lq2dbnu_htibwsDOt-xDFT4WN-2hshvoDTdOxYYJSqZUcrRm44LcNhiyeBXomnoHFGGVzL4aQ5dzA7_GddZ_QrJ63zp5j4="),
    ("Stallion Network 2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGr9mPH2MJaFn8QkCE7KB1Nk84RPylnRsl8dx3OWv_H54dT-HqD3GDWhN-p2eXkg5JOMmH5-5uQeCPprdIkmcZDl_zO41t-3u-k9L1z_cbaFI2Isdct"),
    ("Tuybutky", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg_lfHKAKvQ3uwoeFMuI6-zscJ7G_hdynSnJxMBpEzM9aHUN-_HInziKB7B-ql4D_IOnMUPAzRQUsmFv9TaeB27Ngw4b_4_oV1F6ndcOg="),
    ("NVA FPT", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEwS8pS9e-PKX3JWMsh2klx-Q6bT5IGbY1U4mWuw7a-p33bMFh1DWqGSfMf1X-adqWvGKHO8s4mh3slC_bETol59wocdj5E_6iMSqviQkK6-UbBpE2UsnHcMpdwvw=="),
    ("LadiPage Viettel", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgv8RfdFLSkxGthkcTXU6Tw6eiSPNw47yJI-rmdP3wUxvlpUggSym7LUFXlHF7jkAXu3xWkf5w5JT5wQRWwRkK64_m7BdMQwRDHCbvbcJu2IgCuhCgZ0ktfaKahk1p-wQfYd4Ia-h9Lr60btdYSmket8u7OuYFcQ=="),
    ("FPT Danang Info", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQExJunTVnRNyYRs5E641GsqFOmFZ1sxoHmq8XpgWf-Zb0DjlgGfMEGDISZHQrNh9A7nPYUflQ8rmtN_avx2lruFUdzSzLfhNeepcf8PPzJ59ORnhIVPgrvkUE2xEO0="),
    ("Mang VNPT", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHC_V88C2R8sF-KrKip3SsaIeJWiML3wJyjj7wPu0wq0UiqEOSPNp66RmillmiDFcvo_z2sFt9JkowDVOfXJHubHec22CqhQae9sE4Clq0JsOLHHg3jxL7BbSkWNUWphvpGdaVlIZWcRNW9YQho7Y1rQFefAkVaGEWqrnLGrMiBu2YT-JCBhf5y"),
    ("LadiPage 3 Viettel", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTsRoQ7SGrT6nFVSuTyVJ5ne-yiuOACYQB7OagoMOTRsr61aZR-u1aQPMHZEQnxlbBT3RTB0JJTjg0o47F2Z6q5uF_NOAWaKRV4D-BvmHMtMxVYtxdNn7WTtUTuGN49H4fMcr2-DezjBgcklRoBT4hcN7K9ftOKzbX6ij8iX4W3VjrTNE="),
    ("LadiPage VNPT", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHn9YiN_cibnHhFVOgyGPw-qO64yEMoXk-ira2xfeHNssfSOVTidKRE2-zpl62LDg5LyuMOvZk1iET7XwbiDzgFYrSDO--biV5Ni-l6KqBfwYB4Gj9AJwjd8sPh54E=")
]

urls_to_audit = [
    "https://demo.deverust.com/netlink/template-kit/home/",
    "https://zaivoip.webflow.io/",
    "https://zainet.webflow.io/",
    "https://novos-fiber.webflow.io/",
    "https://fptconnect.vn/lap-internet-fpt",
    "https://fpttelecoms.vn/khuyen-mai-lap-mang-fpt/",
    "https://hi-fpt.vn/lap-mang-fpt-thang-10/",
    "https://lapmangwifi.com.vn/",
    "https://www.tongdaitructuyen.vn/vienthongcardinallapinternet",
    "https://www.tongdaitructuyen.vn/",
    "https://sites.google.com/view/lap-mang-fpt-telecom-net",
]

print("=== Resolving New Search Redirects ===")
for label, rurl in redirects:
    try:
        r = requests.get(rurl, headers=headers, timeout=10, allow_redirects=True)
        print(f"  {label:25s} -> [{r.status_code}] {r.url}")
        if r.status_code == 200:
            urls_to_audit.append(r.url)
    except Exception as e:
        print(f"  {label:25s} -> ERR: {str(e)[:60]}")

print("\n=== Auditing Structure ===")
for u in urls_to_audit:
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=True)
        html = r.text
        lower = html.lower()
        if "ngừng hoạt động" in lower or "suspended" in lower or "không tồn tại" in lower and len(html) < 5000:
            print(f"[DEAD] {u}")
            continue
        s = BeautifulSoup(html, "html.parser")
        title = s.title.get_text(strip=True) if s.title else ""
        is_ladi = ("ladi-section" in lower or "w.ladicdn.com" in lower or "ladipage" in lower)
        is_canvas = ("elementor-template-canvas" in lower)
        is_framer = ("framer.com" in lower or "framerusercontent" in lower)
        nav_links = len(s.select("header a, nav a, .menu a, .navbar a"))
        forms = len([fm for fm in s.find_all("form") if len([i for i in fm.find_all(["input","select","textarea"]) if i.get("type") not in ["hidden","submit","button"]]) > 0])
        tel = len(s.find_all("a", href=re.compile(r"^tel:", re.I)))
        print(f"[{r.status_code}] {r.url:55s} | Ladi:{str(is_ladi):5s} | Framer:{str(is_framer):5s} | Nav:{nav_links:2d} | Forms:{forms} | Tel:{tel:2d} | {title[:45]}")
    except Exception as e:
        print(f"[ERR] {u} -> {str(e)[:60]}")
