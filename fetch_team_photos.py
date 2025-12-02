"""Fetch team photos from people.utwente.nl (photos on utwente.becdn.net CDN)."""
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

TEAM = [
    "joerg.osterrieder", "r.effing", "j.huellmann", "a.trivella", "m.r.k.mes",
    "x.huang", "c.kolb", "r.guizzardi", "e.svetlova", "p.khrennikova",
    "f.s.bernard", "mathis.jander", "j.vanhillegersberg", "mohamed.faid",
    "m.r.machado", "armin.sadighi", "w.j.a.vanheeswijk", "manuele.massei"
]
OUT = Path("static/images/team")
OUT.mkdir(parents=True, exist_ok=True)

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 Chrome/120'

for name in TEAM:
    url = f"https://people.utwente.nl/{name}"
    print(f"{name}...", end=" ")
    try:
        soup = BeautifulSoup(s.get(url, timeout=30).text, 'html.parser')
        for img in soup.find_all('img', src=True):
            src = img['src']
            if 'becdn.net' in src and '.wh/ea/uc/' in src and 'logo' not in src.lower():
                data = s.get(src, timeout=30).content
                (OUT / f"{name.replace('.','_')}.jpg").write_bytes(data)
                print(f"OK ({len(data)//1024}KB)")
                break
        else:
            print("not found")
    except Exception as e:
        print(f"error: {e}")
    time.sleep(0.3)
