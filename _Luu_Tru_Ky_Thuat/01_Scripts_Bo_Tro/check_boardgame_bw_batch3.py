# -*- coding: utf-8 -*-
import os, sys, json, time
import numpy as np
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import verify_url_health, setup_page_protection
from playwright.sync_api import sync_playwright

CANDIDATES = [
    ("Pawn and Pint", "https://www.pawnandpint.net/", "USA - Board Game Pub"),
    ("Dice & Fork", "https://www.diceandfork.co.nz/", "NZ - Board Game Bar & Kitchen"),
    ("Hex & Co NYC", "https://www.hexnyc.com/", "USA - Board Game Cafe & Bar"),
    ("The Cardboard Cafe", "https://www.thecardboardcafe.com/", "Canada - Board Game Cafe"),
    ("Pieces Board Game Bar", "https://www.stlpieces.com/", "USA - Board Game Bar & Restaurant"),
    ("The Board Room Halifax", "https://www.boardroomgames.ca/", "Canada - Board Game Cafe"),
    ("Labyrinth Games", "https://www.labyrinthgameshop.com/", "USA - Board Game Shop & Events"),
    ("Draughts London (UA)", "https://www.draughtslondon.com/", "UK - Board Game Restaurant & Bar"),
]

debug_dir = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "02_Screenshots_Debug_Va_Khao_Sat", "bg_bw_probe3")
os.makedirs(debug_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, (name, url, cat) in enumerate(CANDIDATES, 1):
        ok, reason, final_url, title = verify_url_health(url, timeout=8)
        slug = name.lower().replace(" ", "_").replace("&", "and").replace("'", "").replace("(", "").replace(")", "")
        shot_path = os.path.join(debug_dir, f"{idx:02d}_{slug}.png")

        if not ok:
            print(f"[{idx:02d}] DEAD  | {name:24s} | {reason}")
            continue

        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
                                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = ctx.new_page()
        setup_page_protection(page)
        try:
            page.goto(final_url, timeout=25000, wait_until="domcontentloaded")
            time.sleep(3.5)
            page.screenshot(path=shot_path, full_page=False)
            img = Image.open(shot_path).convert("RGB")
            arr = np.array(img, dtype=np.float32)
            mx = arr.max(axis=2)
            mn = arr.min(axis=2)
            sat = np.where(mx > 0, (mx - mn) / mx, 0)
            mean_sat = float(sat.mean())
            bw_pixel_ratio = float((sat < 0.15).mean())
            dark_ratio = float((mx < 60).mean())
            light_ratio = float((mn > 200).mean())
            print(f"[{idx:02d}] ALIVE | {name:24s} | BW_px={bw_pixel_ratio:.2f} | Dark={dark_ratio:.2f} | Light={light_ratio:.2f} | Sat={mean_sat:.2f} | {final_url}")
        except Exception as e:
            print(f"[{idx:02d}] ERR   | {name:24s} | {str(e)[:60]}")
        finally:
            ctx.close()
    browser.close()
