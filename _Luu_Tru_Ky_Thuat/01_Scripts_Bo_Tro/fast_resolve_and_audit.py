# -*- coding: utf-8 -*-
import sys, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

redirects = [
    ("wf1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHB5lOXr-JWYCauDPOgJX1fn-nhCK6dN2cyCj07r_kaYmUdQ_TmQYQTB7mAskY38-riKF5clQQ7dDhFhweaO4VZmcF0EWWH4yoAhxE7aBmWiW3y9M4s0ozHsBTFQ7Sdsz5gDIhviVDNV5OD7ol0qvkq6u2kbAA8ipLHAjczJzX3RSgGwmuEFiXC"),
    ("wf2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKXGazMQLFSy9uJfovJeDW8DtRDBxOorYZRm-HJSgRAca0hDxrZTvrNjuaXfr6g9oATPDz3fi_Pm3QT9PJ41M3zHO6-EiRiddL_ZmGVTIvU4T7aV1Z42Fkrk7Jq_IEeVY9wA=="),
    ("wf3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9HoDB-ed0my-ycBSBldkFrOpf6zBM7MLtVRbtiO_qgcZDOdKaxYGI1c8ETePg9ZsQYR347iLp5JWafoE3pUsV_6SHwQZFDZGwxpwvjsCUIctVCb3LTNUeQbemLKwhYuZRCpdK_z1xitNhkbw="),
    ("wf4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHzjgp6SBYRIa3yNjr8B43-Lrcp3276d6DPP1uIOqiSz9-2JqE5clFpm48wWpHyrrnDkF7DdBV6Xq2XKOWYYCr1OPOIrph8X6lzQJoZXEJ4LtaoaTOIhA=="),
    ("wf5", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuM9Cm6MWy0M-cH6ZgqxGzxOd3g9vN8QLwpxVj_kKGRjYs8Wvqft8tlxMdYkpcGHCxTNT_o46VnvjmRCigJKxtMXf1R4ijSRDKThpVwA=="),
    ("wf6", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGkacp4KLwFFX7JI27kHw3MUK2DZDVgqkG6ivWv1Q9_IQ74g00Hfab2kPo_IqPQNBNM09jtzsDXo382zq8yUdpuWLQX_fTUsunOlbWIySn4lEOJ9hv6bdBg"),
    ("fpt_sub1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHALms4CJnejclVG0A1hQC5BXoq_2m9Tcq839CbR0VP_q7Yu5-suOjFLQxtgsM8dEJybwATWaBNNHadoCSOoxU5d72bZeLwJwi-pjDNVQD0UihZfY-2_zjOQY3jgJivcfQTHnZ7-sAkTdq8upIWUmqgLASnl0-pfP2mK1vA4wQUaRpjakpTBbM="),
    ("fpt_sub2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHyicdIXh1ut2N98xVtEOA1gaLhjeV5TU4AkybRhrS5VsHrh6rv8x2rXGRiBV2SEK58VzQzGj-7aREP3mY7Kh-NPPD9ZigelTPZGhCn"),
    ("fpt_vn1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbNHzif0_-uDpgfrovoiAb4yL7TZ0SX0E2D537kLZQk0Z5rN4j-yezh6LFs-J3f3_aXerCpSYfvDCAPZNM4ZhAx41aPXjBCUJ5Fh-kFQxmZSiCSFpGZ5TQXLJutCYd0zNV7QA0UMVUJLpZlwYX-yyCYSsnTaKHOGAfn2mIofgKxJveLs2LEpwyjubgdtL8InjqQFr3tAaldUeVUA=="),
    ("fpt_vn2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGf0mU4YO4e_QgM9in6c-kOCJ4c74WnOYk1VqRpppERW9jftT54ZGbbGQgIFTLn01uvsuhKDoTBFKBhYvRdzMkfxP8O0FKigzbs50Dghx30OvWe80aI8tdEa3s="),
    ("fpttelecomvietnam", "https://www.fpttelecomvietnam.vn/"),
    ("viettelca", "https://viettelca.vn/goi-cuoc-lap-mang-internet-wifi-viettel.html"),
    ("wifi24h", "https://wifi24h.vn/"),
    ("fpt_webmau", "https://fpt.webmau.dev/"),
    ("ladi_cd", "https://showcase.ladi.me/64ed9b10f862bd0012aaf304"),
    ("theme_tf", "https://tinyurl.com/3zpnturf"),
]

def check_one(item):
    lbl, u = item
    try:
        r = requests.get(u, headers=headers, timeout=6, allow_redirects=True)
        html = r.text
        lower = html.lower()
        dead = any(k in lower for k in ["ngừng hoạt động", "suspended"]) and len(html) < 25000
        s = BeautifulSoup(html, "html.parser")
        title = s.title.get_text(strip=True) if s.title else ""
        is_ladi = ("ladi-section" in lower or "w.ladicdn.com" in lower or "ladipage" in lower)
        is_framer = ("framer.com" in lower or "framerusercontent" in lower)
        is_wf = ("webflow" in lower)
        nav = len(s.select("header a, nav a, .menu a, .navbar a"))
        forms = len([fm for fm in s.find_all("form") if len([i for i in fm.find_all(["input","select","textarea"]) if i.get("type") not in ["hidden","submit","button"]]) > 0])
        tel = len(s.find_all("a", href=re.compile(r"^tel:", re.I)))
        # extract .webflow.io or demo links if webflow.com template page
        wf_demos = []
        if "webflow.com" in r.url:
            wf_demos = [x for x in set(re.findall(r'https://[a-z0-9\-]+\.webflow\.io/?', html)) if "webflow-templates" not in x][:4]
        return f"[{r.status_code}] {'DEAD' if dead else 'LIVE'} | {lbl:18s} -> {r.url:55s} | Ladi:{str(is_ladi):5s} | WF:{str(is_wf):5s} | Nav:{nav:2d} | Forms:{forms} | Tel:{tel:2d} | {title[:40]} | {wf_demos}"
    except Exception as e:
        return f"[ERR] {lbl:18s} -> {str(e)[:70]}"

with ThreadPoolExecutor(max_workers=10) as ex:
    for res in ex.map(check_one, redirects):
        print(res)
