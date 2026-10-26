import urllib.request
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    # Wedding Planner
    ("The Planners", "https://theplannersvn.com/"),
    ("Bliss Weddings & Events", "https://blissvn.com/"),
    ("Meraki Wedding Planner", "https://merakiweddingplanner.com/"),
    ("K.I.S.S Wedding Planner", "https://kisswe.com/"),
    ("VOAN Wedding & Event", "https://voan.vn/"),
    ("Tiffany Wedding", "https://tiff.vn/"),
    # Trung tam tiec cuoi
    ("GEM Center", "https://gemcenter.com.vn/"),
    ("White Palace", "https://whitepalace.com.vn/"),
    ("Capella Gallery Hall", "https://capellagallery.com/"),
    ("Riverside Palace", "https://riversidepalace.vn/"),
    ("Asiana Plaza", "https://asiana-plaza.com/"),
    ("Trong Dong Palace", "https://trongdongpalace.com/"),
    # Studio & Vay cuoi
    ("TuArt Wedding", "https://tuarts.net/"),
    ("Nupakachi Wedding", "https://nupakachi.com/"),
    ("Rin Wedding", "https://rinwedding.vn/"),
    ("Nicole Bridal", "https://nicolebridal.vn/"),
    ("Linh Nga Bridal", "https://linhnga.vn/"),
    ("Mimosa Wedding", "https://mimosawedding.net/"),
    # Nen tang cuoi & Thiep cuoi
    ("Biihappy (iWedding)", "https://biihappy.com/"),
    ("Weddingbook", "https://www.weddingbook.vn/"),
    ("Wedsite VN", "https://wedsite.vn/")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for name, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as res:
            print(f"OK [{res.status}]: {name} -> {u}", flush=True)
    except Exception as e:
        print(f"FAIL: {name} -> {u} ({e})", flush=True)
