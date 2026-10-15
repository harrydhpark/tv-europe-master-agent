"""
TV Europe Sales Master AI Agent - Strategic Sales Reports PPTX Parser & DuckDB Indexer
Parses 2025~2026 strategic meeting reports, extracts slide texts, tables, and notes,
and populates fact_strategic_slides & dim_strategic_reports in master_analytics.duckdb with FTS.
"""

import os
import sys
import io
import re
import glob
import json
from datetime import datetime

# Ensure stdout handles UTF-8 on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import duckdb
from pptx import Presentation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "master_analytics.duckdb")
REPORTS_DIR = r"d:\TV 유럽영업\1.영업 주요보고"
CATALOG_PATH = os.path.join(DATA_DIR, "strategic_reports_catalog.json")

# Subsidiary Detection Keywords
SUBSIDIARY_KEYWORDS = {
    'DG': ['독일', 'dg', 'lgedg', 'germany', 'mediamarkt de', 'saturn'],
    'UK': ['영국', 'uk', 'lgeuk', 'currys', 'john lewis', 'ao.com'],
    'FS': ['프랑스', 'fs', 'lgefs', 'france', 'fnac', 'darty', 'boulanger'],
    'IS': ['이탈리아', '이태리', 'is', 'lgeis', 'italy', 'mediaworld', 'unieuro'],
    'ES': ['스페인', 'es', 'lgees', 'spain', 'el corte ingles', 'carrefour es'],
    'PL': ['폴란드', 'pl', 'lgepl', 'poland', 'euro net', 'media expert'],
    'BN': ['베네룩스', '네덜란드', 'bn', 'lgebn', 'benelux', 'netherlands', 'coolblue'],
    'CK': ['체코', '슬로바키아', 'ck', 'lgeck', 'czech', 'slovakia', 'alza'],
    'MK': ['헝가리', 'mk', 'lgemk', 'hungary'],
    'HS': ['그리스', 'hs', 'lgehs', 'greece', 'kotsovolos'],
    'PT': ['포르투갈', 'pt', 'lgept', 'portugal', 'worten'],
    'RO': ['루마니아', 'ro', 'lgero', 'romania'],
    'SW': ['스웨덴', '노르딕', '북유럽', 'sw', 'lgesw', 'sweden', 'nordic', 'elkjop'],
    'SWISS': ['스위스', 'swiss', 'switzerland', 'fust', 'interdiscount'],
    'AG': ['오스트리아', 'ag', 'lgeag', 'austria'],
    'LA': ['발틱', '라트비아', 'la', 'lgela', 'baltic', 'latvia'],
    'RA': ['러시아', 'ra', 'lgera', 'russia']
}

PRODUCT_KEYWORDS = {
    'OLED': ['oled', '올레드', 'woled', 'mrgb', 'c4', 'c5', 'g4', 'g5', 'b4', 'b5', 'm4', 'm5', 'wallpaper'],
    'QNED': ['qned', '미니led', 'mini led', 'qned90', 'qned85', 'qned80'],
    'MRGB': ['mrgb', 'micro rgb', 'm-rgb'],
    'UHD': ['uhd', '4k', 'nanocell', 'ut80', 'ur80'],
    'StandbyME': ['스탠바이미', 'standbyme', 'standby me'],
    'UltraLarge': ['초대형', '극초대형', '98인치', '97인치', '83인치', '77인치', '86인치', '85인치']
}

def extract_date_from_string(s):
    # Match YYYY MM DD or YYYYMMDD or YYMMDD
    m = re.search(r'(202[456])[ ._-]?(\d{2})[ ._-]?(\d{2})', s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m2 = re.search(r'2[56](\d{2})(\d{2})', s)
    if m2:
        return f"2026-{m2.group(1)}-{m2.group(2)}"
    return "2026-01-01"

def determine_meeting_type(name):
    n = name.lower()
    if '전략회의' in n or 'strategy' in n:
        return '전략회의'
    if 'pd회의' in n or 'pd 회의' in n or 'pd' in n:
        return 'PD회의'
    if 'npi' in n or 'eol' in n:
        return 'NPI/라인업'
    if '워크샵' in n or 'workshop' in n:
        return '워크샵'
    if '캠페인' in n or 'campaign' in n:
        return '마케팅캠페인'
    if '보고' in n or 'task' in n or 'study' in n:
        return '현안보고'
    return '영업일반'

def extract_tags(text, keyword_dict):
    text_lower = text.lower()
    matched = []
    for tag, keywords in keyword_dict.items():
        for kw in keywords:
            if kw in text_lower:
                matched.append(tag)
                break
    return matched

import hashlib

def parse_pptx_file(file_path, folder_name):
    file_name = os.path.basename(file_path)
    report_date = extract_date_from_string(folder_name + " " + file_name)
    meeting_type = determine_meeting_type(folder_name + " " + file_name)
    file_hash = hashlib.md5((folder_name + "_" + file_name).encode('utf-8')).hexdigest()[:8]
    clean_folder = re.sub(r'[^A-Za-z0-9]', '', folder_name)[:16]
    report_id = f"REP_{clean_folder}_{file_hash}"
    
    try:
        prs = Presentation(file_path)
    except Exception as e:
        print(f"  [!] Failed to open PPTX: {file_name} ({e})")
        return None, []

    total_slides = len(prs.slides)
    slides_data = []

    for slide_no, slide in enumerate(prs.slides, 1):
        # 1. Slide Title
        slide_title = ""
        if slide.shapes.title and slide.shapes.title.has_text_frame:
            slide_title = slide.shapes.title.text_frame.text.strip()

        # 2. Text Frames & Bullets
        content_lines = []
        tables_markdown = []

        for shape in slide.shapes:
            # Body text
            if shape.has_text_frame and shape != slide.shapes.title:
                t = shape.text_frame.text.strip()
                if t:
                    # Clean repeated newlines
                    clean_t = re.sub(r'\n{3,}', '\n\n', t)
                    content_lines.append(clean_t)
                    # If title was empty, pick first non-empty text as title
                    if not slide_title and len(clean_t) < 80:
                        slide_title = clean_t.split('\n')[0]
            
            # Tables
            elif shape.has_table:
                try:
                    table = shape.table
                    rows_md = []
                    col_count = len(table.columns)
                    headers = [table.cell(0, col_idx).text.strip().replace('\n', ' ') for col_idx in range(col_count)]
                    rows_md.append("| " + " | ".join(headers) + " |")
                    rows_md.append("| " + " | ".join(["---"] * col_count) + " |")
                    for row_idx in range(1, len(table.rows)):
                        row_vals = [table.cell(row_idx, col_idx).text.strip().replace('\n', ' ') for col_idx in range(col_count)]
                        rows_md.append("| " + " | ".join(row_vals) + " |")
                    tables_markdown.append("\n".join(rows_md))
                except Exception as te:
                    pass

        # 3. Speaker notes
        speaker_notes = ""
        try:
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                speaker_notes = slide.notes_slide.notes_text_frame.text.strip()
        except Exception:
            pass

        full_slide_text = (slide_title + "\n" + "\n".join(content_lines) + "\n" + "\n".join(tables_markdown) + "\n" + speaker_notes).strip()
        if not full_slide_text:
            continue

        subs_tags = extract_tags(full_slide_text, SUBSIDIARY_KEYWORDS)
        prod_tags = extract_tags(full_slide_text, PRODUCT_KEYWORDS)

        slide_entry = {
            "slide_id": f"{report_id}_S{slide_no:03d}",
            "report_id": report_id,
            "report_name": file_name,
            "report_date": report_date,
            "meeting_type": meeting_type,
            "folder_name": folder_name,
            "file_path": file_path,
            "slide_no": slide_no,
            "slide_title": slide_title or f"Slide {slide_no}",
            "content_text": "\n\n".join(content_lines),
            "tables_markdown": "\n\n".join(tables_markdown),
            "speaker_notes": speaker_notes,
            "subsidiary_tags": ",".join(subs_tags),
            "product_tags": ",".join(prod_tags),
            "char_count": len(full_slide_text)
        }
        slides_data.append(slide_entry)

    report_meta = {
        "report_id": report_id,
        "report_name": file_name,
        "report_date": report_date,
        "meeting_type": meeting_type,
        "folder_name": folder_name,
        "file_path": file_path,
        "total_slides": total_slides,
        "parsed_slides_count": len(slides_data),
        "file_size_bytes": os.path.getsize(file_path)
    }

    return report_meta, slides_data

def run_ingestion():
    print("=" * 70)
    print(" 🚀 TV Europe Strategic Reports Ingestion & Knowledge Indexer")
    print(f" Source: {REPORTS_DIR}")
    print(f" Target DB: {DB_PATH}")
    print("=" * 70)

    if not os.path.exists(REPORTS_DIR):
        print(f"[!] Reports directory not found: {REPORTS_DIR}")
        return

    # Scan 2025~2026 folders
    folders = [f for f in os.listdir(REPORTS_DIR) if f.startswith(('2025', '2026')) and os.path.isdir(os.path.join(REPORTS_DIR, f))]
    folders.sort()

    all_reports = []
    all_slides = []

    for folder in folders:
        folder_path = os.path.join(REPORTS_DIR, folder)
        pptx_files = glob.glob(os.path.join(folder_path, "*.pptx"))
        for pptx_file in pptx_files:
            bname = os.path.basename(pptx_file)
            if bname.startswith("~$"): continue
            
            print(f"[*] Parsing: [{folder}] {bname}")
            meta, slides = parse_pptx_file(pptx_file, folder)
            if meta:
                all_reports.append(meta)
                all_slides.extend(slides)
                print(f"    -> Extracted {len(slides)}/{meta['total_slides']} content slides")

    print("\n" + "=" * 70)
    print(f" Parsing Complete! Total Reports: {len(all_reports)}, Total Slides: {len(all_slides)}")
    print("=" * 70)

    # 1. Save JSON Catalog
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_reports": len(all_reports),
            "total_slides": len(all_slides),
            "reports": all_reports,
            "slides": all_slides
        }, f, ensure_ascii=False, indent=2)
    print(f"[✓] Saved JSON catalog to: {CATALOG_PATH} ({os.path.getsize(CATALOG_PATH)/1024:.1f} KB)")

    # 2. Populate DuckDB
    print("\n[*] Populating DuckDB tables & building Full-Text Search (FTS) index...")
    conn = duckdb.connect(DB_PATH)

    # Create tables
    conn.execute("""
    CREATE TABLE IF NOT EXISTS dim_strategic_reports (
        report_id VARCHAR PRIMARY KEY,
        report_name VARCHAR,
        report_date VARCHAR,
        meeting_type VARCHAR,
        folder_name VARCHAR,
        file_path VARCHAR,
        total_slides INTEGER,
        parsed_slides_count INTEGER,
        file_size_bytes BIGINT,
        indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_strategic_slides (
        slide_id VARCHAR PRIMARY KEY,
        report_id VARCHAR,
        report_name VARCHAR,
        report_date VARCHAR,
        meeting_type VARCHAR,
        folder_name VARCHAR,
        file_path VARCHAR,
        slide_no INTEGER,
        slide_title VARCHAR,
        content_text TEXT,
        tables_markdown TEXT,
        speaker_notes TEXT,
        subsidiary_tags VARCHAR,
        product_tags VARCHAR,
        char_count INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Clear existing and insert
    conn.execute("DELETE FROM dim_strategic_reports;")
    conn.execute("DELETE FROM fact_strategic_slides;")

    # Batch insert reports
    for r in all_reports:
        conn.execute("""
        INSERT INTO dim_strategic_reports 
        (report_id, report_name, report_date, meeting_type, folder_name, file_path, total_slides, parsed_slides_count, file_size_bytes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, [
            r['report_id'], r['report_name'], r['report_date'], r['meeting_type'],
            r['folder_name'], r['file_path'], r['total_slides'], r['parsed_slides_count'], r['file_size_bytes']
        ])

    # Batch insert slides
    for s in all_slides:
        conn.execute("""
        INSERT INTO fact_strategic_slides
        (slide_id, report_id, report_name, report_date, meeting_type, folder_name, file_path,
         slide_no, slide_title, content_text, tables_markdown, speaker_notes, subsidiary_tags, product_tags, char_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, [
            s['slide_id'], s['report_id'], s['report_name'], s['report_date'], s['meeting_type'],
            s['folder_name'], s['file_path'], s['slide_no'], s['slide_title'], s['content_text'],
            s['tables_markdown'], s['speaker_notes'], s['subsidiary_tags'], s['product_tags'], s['char_count']
        ])

    print(f"[✓] Inserted {len(all_reports)} reports and {len(all_slides)} slides into DuckDB.")

    # Build DuckDB FTS Index
    print("[*] Building DuckDB FTS Index on fact_strategic_slides...")
    try:
        conn.execute("INSTALL fts; LOAD fts;")
        # Drop previous FTS index if exists
        try:
            conn.execute("PRAGMA drop_fts_index('fact_strategic_slides');")
        except Exception:
            pass
        
        conn.execute("PRAGMA create_fts_index('fact_strategic_slides', 'slide_id', 'slide_title', 'content_text', 'tables_markdown', 'speaker_notes');")
        print("[✓] DuckDB FTS Index created successfully!")
    except Exception as fe:
        print(f"[!] FTS creation warning: {fe}")

    # Verify query
    sample_query = "OLED"
    res = conn.execute(f"""
    SELECT slide_id, report_name, slide_no, slide_title, score
    FROM (
        SELECT *, fts_main_fact_strategic_slides.match_bm25(slide_id, '{sample_query}') AS score
        FROM fact_strategic_slides
    )
    WHERE score IS NOT NULL
    ORDER BY score DESC
    LIMIT 3;
    """).fetchall()
    
    print("\n[*] Sample FTS Verification Query ('OLED'):")
    for r in res:
        print(f"  - Slide {r[2]} ({r[1]}): {r[3]} (BM25 Score: {r[4]:.3f})")

    conn.close()
    print("\n🎉 Strategic Knowledge Base Ingestion completed successfully!")

if __name__ == "__main__":
    run_ingestion()
