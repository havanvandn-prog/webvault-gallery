# -*- coding: utf-8 -*-
import sys, os
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

websites = [
    {"id": "dhdc01", "name": "IMM Group", "url": "https://immgroup.com/", "domain": "immgroup.com", "slug": "immgroup_com"},
    {"id": "dhdc02", "name": "Interimm", "url": "https://www.interimm.vn/", "domain": "interimm.vn", "slug": "interimm_vn"},
    {"id": "dhdc03", "name": "Harvey Law Group Vietnam", "url": "https://dautudinhcu.com/", "domain": "dautudinhcu.com", "slug": "dautudinhcu_com"},
    {"id": "dhdc04", "name": "Citizen Pathway", "url": "https://citizenpathway.org/", "domain": "citizenpathway.org", "slug": "citizenpathway_org"},
    {"id": "dhdc05", "name": "Kornova Vietnam", "url": "https://kornova-viet.com/", "domain": "kornova-viet.com", "slug": "kornova-viet_com"},
    {"id": "dhdc06", "name": "First Consulting Group (FCG)", "url": "https://ditrumy.com/", "domain": "ditrumy.com", "slug": "ditrumy_com"},
    {"id": "dhdc07", "name": "Khai Phú Investments", "url": "https://tuvanditru.com/", "domain": "tuvanditru.com", "slug": "tuvanditru_com"},
    {"id": "dhdc08", "name": "Maple Leaf Vietnam", "url": "https://mapleleafvn.com/", "domain": "mapleleafvn.com", "slug": "mapleleafvn_com"},
    {"id": "dhdc09", "name": "American Study", "url": "https://americanstudy.edu.vn/", "domain": "americanstudy.edu.vn", "slug": "americanstudy_edu_vn"},
    {"id": "dhdc10", "name": "Nam Anh Scholarship", "url": "https://hocbongnamanh.edu.vn/", "domain": "hocbongnamanh.edu.vn", "slug": "hocbongnamanh_edu_vn"},
    {"id": "dhdc11", "name": "Anh Ngữ Du Học ETEST", "url": "https://etest.edu.vn/", "domain": "etest.edu.vn", "slug": "etest_edu_vn"},
    {"id": "dhdc12", "name": "Summit Education", "url": "https://summit.edu.vn/", "domain": "summit.edu.vn", "slug": "summit_edu_vn"},
    {"id": "dhdc13", "name": "Du Học Á - Âu", "url": "https://duhocaau.vn/", "domain": "duhocaau.vn", "slug": "duhocaau_vn"},
    {"id": "dhdc14", "name": "Du Học VNPC", "url": "https://vnpc.vn/", "domain": "vnpc.vn", "slug": "vnpc_vn"},
    {"id": "dhdc15", "name": "Du Học BlueSea", "url": "https://duhocbluesea.edu.vn/", "domain": "duhocbluesea.edu.vn", "slug": "duhocbluesea_edu_vn"},
    {"id": "dhdc16", "name": "Du Học New Ocean", "url": "https://newocean.edu.vn/", "domain": "newocean.edu.vn", "slug": "newocean_edu_vn"},
    {"id": "dhdc17", "name": "New World Education", "url": "https://newworldedu.vn/", "domain": "newworldedu.vn", "slug": "newworldedu_vn"},
    {"id": "dhdc18", "name": "Du Học GSE", "url": "https://gse.edu.vn/", "domain": "gse.edu.vn", "slug": "gse_edu_vn"},
    {"id": "dhdc19", "name": "Vietint Education", "url": "https://vietint.net/", "domain": "vietint.net", "slug": "vietint_net"},
    {"id": "dhdc20", "name": "Du Học Toàn Cầu ASCI", "url": "https://duhoctoancau.com/", "domain": "duhoctoancau.com", "slug": "duhoctoancau_com"}
]

print(f"Bắt đầu kiểm tra {len(websites)} website bằng Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, w in enumerate(websites, 1):
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            res = page.goto(w["url"], timeout=20000, wait_until="domcontentloaded")
            status = res.status if res else "None"
            title = page.title()
            print(f"[{idx:02d}/20] PASS: {w['name']} ({w['domain']}) -> Status {status} | Title: {title[:45]}")
        except Exception as e:
            print(f"[{idx:02d}/20] FAIL: {w['name']} ({w['domain']}) -> Lỗi: {str(e)[:60]}")
        finally:
            page.close()
    browser.close()
