import sys
import os
import re
from scrapling.fetchers import StealthySession
from bs4 import BeautifulSoup

with StealthySession(headless=False) as session:
    url = "https://www.mediamarkt.ch/de/search.html?query=65C67"
    print(f"Fetching URL: {url}")
    try:
        p = session.fetch(
            url,
            solve_cloudflare=True,
            wait=4000,
            timeout=60000
        )
        print(f"Status: {p.status}, Content Length: {len(p.html_content)}")
        
        html = str(p.html_content)
        with open("debug_mm_search_65c67.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved to debug_mm_search_65c67.html")
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Check for occurrences of 1599 and 1999 in full text
        print("\n--- Price keyword scan in search page ---")
        for price_target in ["1599", "1999", "65C67", "65 C67", "OLED65C6"]:
            matches = [m.start() for m in re.finditer(re.escape(price_target), html, re.I)]
            print(f"Target '{price_target}' occurrences: {len(matches)}")
            for idx in matches[:5]:
                snippet = html[max(0, idx-100):min(len(html), idx+100)].replace('\n', ' ')
                print(f"  Context around {price_target}: {snippet}")

        print("\n--- Product Links & Titles & Prices ---")
        links = soup.find_all('a', href=True)
        seen = set()
        for link in links:
            href = link['href']
            if '/product/' not in href:
                continue
            
            card = link.parent
            for _ in range(6):
                if card and card.parent:
                    card = card.parent
            
            card_text = card.get_text(separator=" | ", strip=True) if card else ""
            if '65' in card_text or 'C6' in card_text or '1599' in card_text or '1999' in card_text:
                key = href
                if key in seen: continue
                seen.add(key)
                print(f"\n[Product Found]")
                print(f"  Link: {href}")
                print(f"  Snippet: {card_text[:400]}")
                
        # Also fetch the direct PDP
        pdp_url = "https://www.mediamarkt.ch/de/product/_lg-oled65c67la-tv-flat-65-164-cm-uhd-4k-smart-tv-webos-2291289.html"
        print(f"\nFetching PDP URL: {pdp_url}")
        p2 = session.fetch(pdp_url, solve_cloudflare=True, wait=4000, timeout=60000)
        print(f"PDP Status: {p2.status}, Content Length: {len(p2.html_content)}")
        pdp_html = str(p2.html_content)
        with open("debug_mm_pdp_65c67.html", "w", encoding="utf-8") as f:
            f.write(pdp_html)
        
        print("\n--- Price keyword scan in PDP ---")
        for price_target in ["1599", "1999", "UVP", "Streichpreis", "Club"]:
            matches = [m.start() for m in re.finditer(re.escape(price_target), pdp_html, re.I)]
            print(f"PDP Target '{price_target}' occurrences: {len(matches)}")
            for idx in matches[:5]:
                snippet = pdp_html[max(0, idx-100):min(len(pdp_html), idx+100)].replace('\n', ' ')
                print(f"  PDP Context around {price_target}: {snippet}")

    except Exception as e:
        print(f"Error fetching URL: {e}")
