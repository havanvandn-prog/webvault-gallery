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
    ("Draughts London (retry)", "https://www.draughtslondon.com/", "UK - Board Game Restaurant & Bar"),
    ("The Board and Brew (retry)", "https://theboardandbrew.com/", "USA - Board Game Restaurant & Bar"),
    ("Randolph Gaming Pub", "https://www.randolph.ca/en/", "Canada - Board Game Pub & Restaurant"),
    ("Colonel Moutarde", "https://colonelmoutarde.ca/", "Canada - Board Game Pub & Bistro"),
    ("Mench Cafe", "https://menchcafe.com/", "Canada - Board Game Cafe"),
    ("The Missing Piece", "https://www.themissingpiecegames.com/", "USA - Board Game Cafe & Bar"),
    ("Raygun Lounge", "https://www.raygunlounge.com/", "USA - Tabletop & Arcade Bar"),
    ("Otter Chaos", "https://www.otterchaos.co.uk/", "UK - Board Game Cafe & Bar"),
    ("Boardgame Cafe Sydney", "https://www.theboardgamecafesydney.com.au/", "Australia - Board Game Cafe"),
    ("Interactivity Cafe", "https://ibgcafe.com/", "Canada - Board Game Cafe"),
    ("Across the Board", "https://acrosstheboardcafe.com/", "Canada - Board Game Cafe & Dining"),
    ("Loading Bar UK", "https://loading.bar/", "UK - Gaming Bar & Cafe"),
    ("Ludorati Cafe", "https://www.ludorati.com/", "UK - Board Game Cafe & Bar"),
    ("Treehouse Sheffield", "https://www.treehousesheffield.com/", "UK - Board Game Cafe & Kitchen"),
    ("The Brooklyn Strategist", "https://www.thebrooklynstrategist.com/", "USA - Board Game Lounge & Cafe"),
    ("The Uncommons (direct)", "https://uncommonsnyc.com/", "USA - Board Game Cafe"),
    ("Hex and Co (direct)", "https://hexandco.com/", "USA - Board Game Cafe & Bar"),
    ("Mox Boarding House (wait)", "https://www.moxboardinghouse.com/", "USA - Board Game Restaurant & Bar"),
    ("Dice & Donuts / Roll", "https://www.rollwithitcafe.com/", "USA - Board Game Cafe"),
    ("Brew & Board", "https://www.theboardroomdc.com/", "USA - Board Game Bar & Bistro"),
]

debug_dir = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "02_Screenshots_Debug_Va_Khao_Sat", "bg_bw_probe2")
os.makedirs(debug_dir, exist_ok=True)

results = []
print(f"=== PROBING BATCH 2 ({len(CANDIDATES)} CANDIDATES) ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, (name, url, cat) in enumerate(CANDIDATES, 1):
        ok, reason, final_url, title = verify_url_health(url, timeout=8)
        slug = name.lower().replace(" ", "_").replace("&", "and").replace("'", "")
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        shot_path = os.path.join(debug_dir, f"{idx:02d}_{slug}.png")

        if not ok:
            print(f"[{idx:02d}] DEAD  | {name:26s} | {reason}")
            results.append({"name": name, "url": url, "cat": cat, "ok": False, "reason": reason})
            continue

        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
                                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = ctx.new_page()
        setup_page_protection(page)
        try:
            page.goto(final_url, timeout=30000, wait_until="networkidle")
            time.sleep(2.5)
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
            bg_info = page.evaluate("""() => {
                const cs = getComputedStyle(document.body);
                return {bg: cs.backgroundColor, color: cs.color, h: document.documentElement.scrollHeight};
            }""")
            print(f"[{idx:02d}] ALIVE | {name:26s} | BW_px={bw_pixel_ratio:.2f} | Dark={dark_ratio:.2f} | Light={light_ratio:.2f} | Sat={mean_sat:.2f} | H={bg_info['h']} | {final_url}")
            results.append({
                "name": name, "url": final_url, "cat": cat, "ok": True,
                "bw_ratio": round(bw_pixel_ratio, 3), "dark_ratio": round(dark_ratio, 3),
                "light_ratio": round(light_ratio, 3), "mean_sat": round(mean_sat, 3),
                "scroll_h": bg_info["h"], "bg": bg_info["bg"], "shot": shot_path, "title": title
            })
        except Exception as e:
            print(f"[{idx:02d}] ERR   | {name:26s} | {str(e)[:60]}")
            results.append({"name": name, "url": final_url, "cat": cat, "ok": False, "reason": str(e)[:80]})
        finally:
            ctx.close()
    browser.close()

out_json = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "bg_bw_probe2.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved batch 2 probe results to", out_json)
