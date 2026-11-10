# -*- coding: utf-8 -*-
import sys
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 1. Check redirects from search_web results (LadiPage, Webflow, ThemeForest, Dribbble)
redirects = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG0V97CTm4cKLzLPLQuLU7DUmjJoRD1184Eqww-oGynYwR0ShUcwSvIDuJA_LCmCCk2BtMeMCJ5F0HZZxcUhBIJjVYXpAHK75KTBDYXKKyrGrfgPOZ9x32r52E5uj0xsnwjgcSIgXwZ5xfZaq7uuqKvi8ZCiAGdY33G_wp65e1MCfqkiVNa5x9pVg6IWMDZkvl_dh5LOdqayE6_qSbtQypQ34txAT7FB5eA136gHGkcRTmex-KI2zJ09HBASGf3ZfOH3TQawLo=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGePtFov3l9WgKOvUkIpFpHKI7NUcp6O4w6k5wy4LVy6tUF7hyAusE6472zx406XW76bvFJHPjeiQyIug2_DdBfTLV28QEkXmlt3PZH6W8GXS5VmoPA3KxwUl5qzzq3zEhqPeLEFo5MUfDNErk_oXDOHWeu_cHAFo9C89o=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnt2i0B1bgjcG2Ug4EOWwFKWHJvAyk2Q42VUOi1488CR_fIFs0FAlW6I2M5Rx3R6XQK1VBioFW_-oL9FXCciMYNU-Gw_vDLQijmATv0rAIwoUL-RuhNFuor-qVqmzASy3GQw==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErfNJdc19BsS9zt0hEUr2Jfp5dte1jZqp0zQx6Ag0jLYFkFUeZAh6UuVYtT5n5slmTOZnb5dJRlISod-QMV1raGGWEcpIsrvz1MsjpdSIOMWAN583uQEDattufhk0G4gKcaeYomh-li6W2NeFWGqC0QMAFAh6EJf32VqL4b1g==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFey0Jlokujz99kpWo95rOgLzkVpgwNKFS2OykJGZTCcYN0IhU57zuy2UnN3P1pDpoTOoqBI70WyZU9yoC6ohFLAL6h2qkzAy3qC9B-qTCEuaPTeu9HeXB6ppEZI_3Z",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHGdjPrNuYAWoJWLEG_5jqqQFYM9pKQ3gdVPcCz12xBin-Bj8kRSqcUkk0V9F-jdSBkb7WYh5QnGwy_tFNYluyORm9Bnzskxb6xK3SF2AowBQEunxMIE9PKCQgIKoGZUOScJ_LG8sFLqOhMx0mzkECBDmfvUI5oBYglqv4RAO5dIbZDoBSLONmfCzk5Q==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEkt-Tqg43kqBO5nV3a7WMRBDP0d5HJ7WQxhKyWThG7KI2l3FOJuM9obMQ7zd9TrqLrl_VrDcEXf0dlKFFktXAtNZ6YoPzGalSxinvwgWl1a-ul40KBCtP57LaRX7J0vWSEfVeSqwmAT_Y-EiPyHs1WW9frDdXz6mSrEGLq13cmwE9royGF1TO9gDxHwuDU0OkX6vjx64nDW2VHsYDRmGUVASUO",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQWWH2BQLrxqHgOcD-Eu1qIXvV46yo3mGxjW5yzbrzjSmCZ1eYRWTm9Ap9OKsuOnWigHJTxXH5B32lZnEy2_lh9ET3JimPmIG0R4nyCPru0HwMh5b1tGDkX-hx-zTZ_yWg09nbbz2zKbR5x8ux2oXidQG5jcVC2vus3brjpcv5PPi6_UnBhVOgqzcs8vcsL8AoQQmkPTE=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqvhExisK8Ue3gfh1ZMhLQ2vsPluq7v3IJx1zMp_ehR64sReIRw3uKJfL8cQUoAB_0VIaPxLigEAogqBQ9xBjTNuTJeFJkZ19_W2VPJGGURtKb3HVzljw3MXh9pZqBYOiBs7UTFPymUaeL5Hl4fPmPv5C_ceqeo1cOajL0t-QkZA6v77suWg5ZGxuURNqU-NQ7TUq04EA==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHKfoGNiiYD4RNhLbJSD5sqeLuLjFB_qYbs1OTLtQM8gEZp-6QBbgDToDpfUxKYXLObUv6esOmG8pFSDMKxwmFNCOc-Jo_uhnJmWaxCelKBHM7bGWp14z7hcIdBnPJGN6BB4LeMh1xPI0JFFt5-KOhQn90XzImi8bFOERl3-uXj",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSieyCsd7rQmb0UfbZ0sylRs5rb0vjYfCR4EBwIyoLuGCXBGuBFbuzR93q2oUrOkUbb54aQkuTgtJeequo2E0VkBz7T30hkSQ5uvQamGiBdA1AUboAc4B8_FLGyDmjDITyiSgEK8S-JLToHP0BqYIXM8tvOdELuEEOyCMrHEGEsRJ-rTL7Ci5s0hvcxhg_"
]

print("--- Resolving Redirects ---")
for u in redirects:
    try:
        r = requests.get(u, headers=headers, timeout=8, allow_redirects=True)
        print(f"  [{r.status_code}] {r.url}")
    except Exception as e:
        print(f"  [ERR] {e}")

# 2. Check LadiPage Marketplace API/Search
print("\n--- Searching LadiPage Marketplace ---")
for kw in ["fpt", "internet", "wifi", "mang", "vien thong", "viettel", "camera"]:
    try:
        r = requests.get(f"https://marketplace.ladipage.vn/api/themes?q={urllib.parse.quote(kw)}", headers=headers, timeout=8)
        print(f"  API q={kw}: status {r.status_code}, len {len(r.text)}")
        if r.status_code == 200 and "{" in r.text[:10]:
            print("   Sample:", r.text[:200])
    except Exception as e:
        print("  API err:", e)

# 3. Search DuckDuckGo HTML for Vietnamese FPT/Internet LadiPages
print("\n--- Searching DuckDuckGo HTML ---")
ddg_queries = [
    '"lắp mạng fpt" site:ladipage.vn',
    '"lắp mạng fpt" "ladipage"',
    '"lắp mạng fpt" inurl:khuyen-mai',
    '"lắp mạng viettel" "ladipage"',
    '"lắp mạng vnpt" "ladipage"'
]
for q in ddg_queries:
    try:
        r = requests.post("https://html.duckduckgo.com/html/", data={"q": q}, headers=headers, timeout=10)
        s = BeautifulSoup(r.text, "html.parser")
        links = s.select("a.result__a")
        print(f"  DDG '{q}' -> {len(links)} results:")
        for a in links[:8]:
            print(f"    {a.get('href')} | {a.get_text(strip=True)[:50]}")
    except Exception as e:
        print("  DDG err:", e)
