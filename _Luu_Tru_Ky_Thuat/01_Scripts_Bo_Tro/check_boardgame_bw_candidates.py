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
    ("Draughts London", "https://www.draughtslondon.com/", "UK - Board Game Cafe & Bar"),
    ("Hex & Co NYC", "https://www.hexnyc.com/", "USA - Board Game Cafe & Bar"),
    ("The Uncommons NYC", "https://www.uncommonsnyc.com/", "USA - Board Game Cafe"),
    ("Sip & Play NYC", "https://www.sipnplaynyc.com/", "USA - Board Game Cafe & Boba/Food"),
    ("Snakes & Lattes", "https://www.snakesandlattes.com/", "Canada/USA - Board Game Bar & Restaurant"),
    ("Mox Boarding House", "https://www.moxboardinghouse.com/", "USA - Board Game Restaurant & Bar"),
    ("Bad Moon Cafe", "https://www.badmooncafe.co.uk/", "UK - Board Game Cafe & Bar"),
    ("Chance & Counters", "https://www.chanceandcounters.com/", "UK - Board Game Cafe & Bar"),
    ("Thirsty Meeples", "https://www.thirstymeeples.co.uk/", "UK - Board Game Cafe & Bar"),
    ("Bastard Cafe", "https://bastardcafe.dk/", "Denmark - Board Game Cafe"),
    ("Boardroom Berlin", "https://boardroom.berlin/", "Germany - Board Game Cafe"),
    ("King and the Pawn", "https://www.kingandthepawn.com/", "Singapore - Board Game Cafe & Bar"),
    ("Board Dublin", "https://boarddublin.com/", "Ireland - Board Game Bar & Cafe"),
    ("Board & Brewed", "https://www.boardandbrewed.ie/", "Ireland - Board Game Cafe & Pizza"),
    ("Bohemia Boards & Brews", "https://www.bohemiaboardsandbrews.com/", "Czech - Board Game Bar & Bistro"),
    ("Meeples & Coffee", "https://www.meeples.cafe/", "Czech - Board Game Cafe"),
    ("Nerd Alert", "https://www.nerdalert.cz/", "Czech - Board Game Bistro"),
    ("Knight Moves Cafe", "https://www.knightmovescafe.com/", "USA - Board Game Cafe"),
    ("Victory Point Cafe", "https://www.victorypointcafe.com/", "USA - Board Game Cafe & Pub"),
    ("The Board and Brew", "https://theboardandbrew.com/", "USA - Board Game Restaurant & Bar"),
    ("Boards & Brews NH", "https://www.boardsandbrewsnh.com/", "USA - Board Game Cafe & Bar"),
    ("Emerald Tavern", "https://emeraldtaverngames.com/", "USA - Board Game Tavern & Kitchen"),
    ("Table Top Cafe", "https://www.tabletopcafe.ca/", "Canada - Board Game Cafe"),
    ("The Hexagon Cafe", "https://thehexcafe.com/", "Canada - Board Game Cafe"),
    ("The Raving Gamer", "https://www.ravinggamer.com/", "Canada - Board Game Bistro"),
    ("Fortress Melbourne", "https://fortress.games/", "Australia - Gaming Bar & Restaurant"),
    ("Side Quest Bar", "https://www.sidequestbar.nl/", "Netherlands - Board Game Bar"),
    ("Arcanists Tavern", "https://arcaniststavern.uk/", "UK - Tabletop Tavern"),
    ("Potions and Rations", "https://www.potionsandrations.co.uk/", "UK - Tabletop Tavern"),
    ("Replay Bristol", "https://www.replaybristol.com/", "UK - Board Game Cafe & Cocktails"),
    ("Goodtime Games", "https://www.goodtimegames.co.uk/", "UK - Board Game Cafe & Pizza"),
    ("Game Point Cafe", "https://gamepointcafe.com/", "USA - Board Game Cafe"),
    ("JELLY JELLY CAFE", "https://jellyjellycafe.com/", "Japan - Board Game Cafe"),
    ("The Mind Cafe SG", "https://themindcafe.com.sg/", "Singapore - Board Game Cafe"),
    ("For The Win Cafe", "https://www.forthewincafe.com/", "Canada - Board Game Cafe & Bar"),
    ("The Ludoquist", "https://www.theludoquist.com/", "UK - Board Game Cafe & Bar"),
    ("Sugar and Dice", "https://www.sugaranddice.co.uk/", "UK - Board Game Cafe"),
    ("Well Played Cafe", "https://wellplayedasheville.com/", "USA - Board Game Cafe & Bar"),
    ("Piece & Pint", "https://www.pieceandpint.com/", "USA - Board Game Pub"),
    ("Rook & Pawn", "https://www.rookandpawn.com/", "USA - Board Game Cafe & Bar"),
    ("Too Bad Games", "https://toobadgames.com/", "Global - Minimalist Board Game Studio"),
    ("Meeple Design", "https://meepledesign.com/", "Global - Minimalist Board Game Art"),
]

debug_dir = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "02_Screenshots_Debug_Va_Khao_Sat", "bg_bw_probe")
os.makedirs(debug_dir, exist_ok=True)

results = []
print(f"=== PROBING {len(CANDIDATES)} CANDIDATES ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, (name, url, cat) in enumerate(CANDIDATES, 1):
        ok, reason, final_url, title = verify_url_health(url, timeout=8)
        slug = name.lower().replace(" ", "_").replace("&", "and").replace("'", "")
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        shot_path = os.path.join(debug_dir, f"{idx:02d}_{slug}.png")

        if not ok:
            print(f"[{idx:02d}] DEAD  | {name:24s} | {reason}")
            results.append({"name": name, "url": url, "cat": cat, "ok": False, "reason": reason})
            continue

        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
                                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = ctx.new_page()
        setup_page_protection(page)
        try:
            page.goto(final_url, timeout=25000, wait_until="domcontentloaded")
            time.sleep(2.5)
            page.screenshot(path=shot_path, full_page=False)
            # Analyze image colors (RGB saturation & brightness & B/W ratio)
            img = Image.open(shot_path).convert("RGB")
            arr = np.array(img, dtype=np.float32)
            mx = arr.max(axis=2)
            mn = arr.min(axis=2)
            sat = np.where(mx > 0, (mx - mn) / mx, 0)
            mean_sat = float(sat.mean())
            bw_pixel_ratio = float((sat < 0.15).mean())
            dark_ratio = float((mx < 60).mean())
            light_ratio = float((mn > 200).mean())
            # Also inspect CSS body background color
            bg_info = page.evaluate("""() => {
                const cs = getComputedStyle(document.body);
                return {bg: cs.backgroundColor, color: cs.color, h: document.documentElement.scrollHeight};
            }""")
            print(f"[{idx:02d}] ALIVE | {name:24s} | BW_px={bw_pixel_ratio:.2f} | Dark={dark_ratio:.2f} | Light={light_ratio:.2f} | Sat={mean_sat:.2f} | H={bg_info['h']} | {final_url}")
            results.append({
                "name": name, "url": final_url, "cat": cat, "ok": True,
                "bw_ratio": round(bw_pixel_ratio, 3), "dark_ratio": round(dark_ratio, 3),
                "light_ratio": round(light_ratio, 3), "mean_sat": round(mean_sat, 3),
                "scroll_h": bg_info["h"], "bg": bg_info["bg"], "shot": shot_path, "title": title
            })
        except Exception as e:
            print(f"[{idx:02d}] ERR   | {name:24s} | {str(e)[:60]}")
            results.append({"name": name, "url": final_url, "cat": cat, "ok": False, "reason": str(e)[:80]})
        finally:
            ctx.close()
    browser.close()

out_json = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "bg_bw_probe.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved probe results to", out_json)
