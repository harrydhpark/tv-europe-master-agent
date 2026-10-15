import os
import sys
import json
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")

def update_raw_mediamarkt_samsung():
    raw_path = os.path.join(DATA_DIR, "raw_mediamarkt_samsung.json")
    with open(raw_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # 1. Update 65S95H
    for it in items:
        if it.get("model_code") == "QE65S95H" or "180857100" in it.get("url", ""):
            it["price"] = 3500.0
            print("  [RAW] Updated 65S95H to 3500.0 CHF")

    # 2. Update 48S95H
    for it in items:
        if "48S95" in it.get("model_code", "") or "180857089" in it.get("url", ""):
            it["model_code"] = "QE48S95H"
            it["price"] = 1985.25
            print("  [RAW] Updated 48S95H to QE48S95H / 1985.25 CHF")

    # 3. Add 77S95H if not present
    has_77 = any("77S95H" in it.get("model_code", "") or "184263169" in it.get("url", "") for it in items)
    if not has_77:
        items.append({
            "brand": "Samsung",
            "year": 2026,
            "display": "OLED",
            "display_type": "OLED",
            "size": 77,
            "model_code": "QE77S95H",
            "price": 4553.7,
            "shipping": "Free",
            "cashback": 0,
            "promo": "None",
            "title": 'SAMSUNG QE77S95H Fernseher (77 " / 195.6 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe77s95h-fernseher-77-1956-cm-uhd-4k-184263169.html",
            "link": "https://www.mediamarkt.ch/de/product/_samsung-qe77s95h-fernseher-77-1956-cm-uhd-4k-184263169.html"
        })
        print("  [RAW] Added 77S95H (4553.70 CHF)")

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"[RAW] Successfully updated {raw_path} ({len(items)} items)")

def update_master_urls():
    master_path = os.path.join(DATA_DIR, "master_product_urls.json")
    with open(master_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    entries = {
        "CH_MEDIAMARKT_SAMSUNG_QE77S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE77S95H",
            "year": 2026,
            "size": 77,
            "title": 'SAMSUNG QE77S95H Fernseher (77 " / 195.6 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe77s95h-fernseher-77-1956-cm-uhd-4k-184263169.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_QE77S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE77S95H",
            "year": 2026,
            "size": 77,
            "title": 'SAMSUNG QE77S95H Fernseher (77 " / 195.6 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe77s95h-fernseher-77-1956-cm-uhd-4k-184263169.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_SAMSUNG_QE65S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE65S95H",
            "year": 2026,
            "size": 65,
            "title": 'SAMSUNG QE65S95H OLED TV (65 " / 165.1 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe65s95h-oled-tv-65-1651-cm-uhd-4k-180857100.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_QE65S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE65S95H",
            "year": 2026,
            "size": 65,
            "title": 'SAMSUNG QE65S95H OLED TV (65 " / 165.1 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe65s95h-oled-tv-65-1651-cm-uhd-4k-180857100.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_SAMSUNG_QE55S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE55S95H",
            "year": 2026,
            "size": 55,
            "title": 'SAMSUNG QE55S95H OLED TV (55 " / 139.7 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe55s95h-oled-tv-55-1397-cm-uhd-4k-180857119.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_QE55S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE55S95H",
            "year": 2026,
            "size": 55,
            "title": 'SAMSUNG QE55S95H OLED TV (55 " / 139.7 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe55s95h-oled-tv-55-1397-cm-uhd-4k-180857119.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_SAMSUNG_QE48S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE48S95H",
            "year": 2026,
            "size": 48,
            "title": 'SAMSUNG QE48S95HAEXZU OLED TV (48 " / 121.9 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe48s95haexzu-oled-tv-48-1219-cm-uhd-4k-180857089.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_QE48S95H": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE48S95H",
            "year": 2026,
            "size": 48,
            "title": 'SAMSUNG QE48S95HAEXZU OLED TV (48 " / 121.9 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe48s95haexzu-oled-tv-48-1219-cm-uhd-4k-180857089.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_SAMSUNG_QE48S95HAEXZU": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE48S95HAEXZU",
            "year": 2026,
            "size": 48,
            "title": 'SAMSUNG QE48S95HAEXZU OLED TV (48 " / 121.9 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe48s95haexzu-oled-tv-48-1219-cm-uhd-4k-180857089.html",
            "last_updated": "2026-10-06"
        },
        "CH_MEDIAMARKT_QE48S95HAEXZU": {
            "country": "CH",
            "retailer": "MediaMarkt",
            "brand": "SAMSUNG",
            "model_code": "QE48S95HAEXZU",
            "year": 2026,
            "size": 48,
            "title": 'SAMSUNG QE48S95HAEXZU OLED TV (48 " / 121.9 cm, UHD 4K)',
            "url": "https://www.mediamarkt.ch/de/product/_samsung-qe48s95haexzu-oled-tv-48-1219-cm-uhd-4k-180857089.html",
            "last_updated": "2026-10-06"
        }
    }

    for k, v in entries.items():
        master[k] = v
        print(f"  [MASTER] Registered {k}")

    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print(f"[MASTER] Successfully updated {master_path} ({len(master)} entries)")

def update_price_tracker_workbook():
    pt_path = os.path.join(DATA_DIR, "price tracker_swiss_2026 1006_v1.xlsx")
    if not os.path.exists(pt_path):
        print(f"[WARN] {pt_path} not found.")
        return

    wb = openpyxl.load_workbook(pt_path)
    sheet = wb["MediaMarkt_Samsung_Full"]

    # 1. Update 65S95H to 3500.0
    for r in range(2, sheet.max_row + 1):
        code = str(sheet.cell(row=r, column=5).value or "")
        if "QE65S95H" in code:
            sheet.cell(row=r, column=6).value = 3500
            print(f"  [PT WORKBOOK] Updated row {r} (QE65S95H) price to 3500 CHF")

    # 2. Update 48S95H model_code if needed
    for r in range(2, sheet.max_row + 1):
        code = str(sheet.cell(row=r, column=5).value or "")
        if "48S95" in code:
            sheet.cell(row=r, column=5).value = "QE48S95H"
            sheet.cell(row=r, column=6).value = 1985.25
            print(f"  [PT WORKBOOK] Updated row {r} (48S95) to QE48S95H / 1985.25 CHF")

    # 3. Add 77S95H if not present
    has_77 = False
    for r in range(2, sheet.max_row + 1):
        code = str(sheet.cell(row=r, column=5).value or "")
        year = sheet.cell(row=r, column=2).value
        if "QE77S95H" in code and year == 2026:
            has_77 = True
            break

    if not has_77:
        new_row = sheet.max_row + 1
        row_vals = ["Samsung", 2026, "OLED", 77, "QE77S95H", 4553.7, "Free", None, 0, "None"]
        for c, val in enumerate(row_vals, 1):
            sheet.cell(row=new_row, column=c).value = val
        print(f"  [PT WORKBOOK] Appended row {new_row} for QE77S95H (4553.70 CHF)")

    wb.save(pt_path)
    wb.close()
    print(f"[PT WORKBOOK] Successfully updated {pt_path}")

def update_swiss_ata_comparison():
    ata_path = os.path.join(DATA_DIR, "Swiss_ATA_Comparison_2026_1006.xlsx")
    if not os.path.exists(ata_path):
        print(f"[WARN] {ata_path} not found.")
        return

    wb = openpyxl.load_workbook(ata_path)
    sheet = wb["Swiss_2026"]

    # Check if 48S95H is already inserted
    found_48s95h = False
    s95h_55_row = None
    for r in range(4, 150):
        val_b = str(sheet.cell(row=r, column=2).value or "").strip()
        if val_b == "48S95H":
            found_48s95h = True
            break
        if val_b == "55S95H":
            s95h_55_row = r

    if not found_48s95h and s95h_55_row is not None:
        insert_at = s95h_55_row + 1  # Insert right after 55S95H
        print(f"  [ATA WORKBOOK] Inserting 48S95H row at row {insert_at}...")
        sheet.insert_rows(insert_at, 1)

        bold_samsung = Font(name="Calibri", size=11, bold=True, color="002060")
        reg_samsung = Font(name="Calibri", size=11, bold=False, color="002060")

        sheet.cell(row=insert_at, column=1).value = "OLED"
        sheet.cell(row=insert_at, column=1).font = bold_samsung
        sheet.cell(row=insert_at, column=2).value = "48S95H"
        sheet.cell(row=insert_at, column=2).font = bold_samsung

        sheet.cell(row=insert_at, column=3).value = "QE48S95H"
        sheet.cell(row=insert_at, column=3).font = reg_samsung
        sheet.cell(row=insert_at, column=4).value = f'=IF(E{insert_at}="","",E{insert_at}-F{insert_at})'
        sheet.cell(row=insert_at, column=5).value = 1985.25
        sheet.cell(row=insert_at, column=6).value = 0

        sheet.cell(row=insert_at, column=8).value = ""
        sheet.cell(row=insert_at, column=8).font = reg_samsung
        sheet.cell(row=insert_at, column=9).value = f'=IF(J{insert_at}="","",J{insert_at}-K{insert_at})'
        sheet.cell(row=insert_at, column=10).value = ""
        sheet.cell(row=insert_at, column=11).value = ""

        # Digitec already has 48S95H at 1916.0 CHF
        sheet.cell(row=insert_at, column=13).value = "QE48S95HAEXZU"
        sheet.cell(row=insert_at, column=13).font = reg_samsung
        sheet.cell(row=insert_at, column=14).value = f'=IF(O{insert_at}="","",O{insert_at}-P{insert_at})'
        sheet.cell(row=insert_at, column=15).value = 1916.0
        sheet.cell(row=insert_at, column=16).value = 0

    wb.save(ata_path)
    wb.close()
    print(f"[ATA WORKBOOK] Saved initial row insertion in {ata_path}")

if __name__ == "__main__":
    print("=== Step 1: Update raw_mediamarkt_samsung.json ===")
    update_raw_mediamarkt_samsung()

    print("\n=== Step 2: Update master_product_urls.json ===")
    update_master_urls()

    print("\n=== Step 3: Update price tracker_swiss_2026 1006_v1.xlsx ===")
    update_price_tracker_workbook()

    print("\n=== Step 4: Insert 48S95H row in Swiss_ATA_Comparison_2026_1006.xlsx ===")
    update_swiss_ata_comparison()

    print("\nAll patch operations completed successfully.")
