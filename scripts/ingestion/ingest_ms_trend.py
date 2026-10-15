"""
Ingestion Script for MS Trend (Agent 08) -> DuckDB
Flattens the 6MB nested MS Trend JSON into normalized fact_market_share records.
"""

import os
import sys
import json
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
MS_DATA_PATH = os.path.join(BASE_DIR, "..", "08. MS Trend", "ms_trend_data.json")

def ingest_ms_trend():
    print("[*] Ingesting 08. MS Trend into DuckDB...")
    if not os.path.exists(MS_DATA_PATH):
        print(f"  [!] MS Trend data not found: {MS_DATA_PATH}")
        return False, 0, "File not found"

    d_conn = duckdb.connect(DUCKDB_PATH)
    now = datetime.now()

    try:
        with open(MS_DATA_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"  [!] Error reading MS Trend data: {e}")
        return False, 0, str(e)

    regions = raw_data.get("regions", {})
    print(f"  -> Parsing {len(regions)} regions from ms_trend_data.json...")

    REGION_CODE_MAP = {
        '유럽': 'EU', 'Switzerland': 'SWISS', 'AG': 'AG', 'DG': 'DG', 
        'UK (2)': 'UK', 'FS': 'FS', 'IS': 'IS', 'ES': 'ES', 'PL': 'PL', 
        'BN': 'BN', 'Netherlands': 'NL', 'Belgium': 'BE', 'CZ': 'CZ', 
        'HS': 'HS', 'RO': 'RO', 'PT': 'PT', 'SW (2)': 'SW'
    }

    fact_ms = []
    anomalies = []

    for reg_key, reg_val in regions.items():
        corp_code = REGION_CODE_MAP.get(reg_key, reg_key)
        data_rows = reg_val.get("data", [])
        
        for r in data_rows:
            idx = r.get("index")
            y26 = r.get("y26", {})
            if not y26:
                continue

            # Identify brand and segment by standard row indexes
            brand, seg = None, "TTL"
            if idx == 27:
                brand, seg = "LG", "TTL"
            elif idx == 60:
                brand, seg = "Samsung", "TTL"
            elif idx == 38:
                brand, seg = "LG", "OLED"
            elif idx == 68:
                brand, seg = "Samsung", "OLED"
            elif idx in (83, 96):
                brand, seg = "Sony", "OLED"
            elif idx == 109:
                brand, seg = "Philips", "OLED"
            elif idx == 122:
                brand, seg = "Panasonic", "OLED"

            if brand:
                # y26 is a list of [Jan, Feb, ..., Dec, YTD]
                for m_idx, ms_val in enumerate(y26[:12]):
                    m_num = m_idx + 1
                    if ms_val is None or ms_val <= 0:
                        continue
                        
                    fact_ms.append((
                        "MONTHLY", f"2026-{m_num:02d}", corp_code, seg, brand,
                        0.0, 0.0, 0.0, float(ms_val), 0.0, now
                    ))

                    # Anomaly: OLED MS drops below 30% for LG
                    if brand == "LG" and seg == "OLED" and ms_val < 30.0:
                        anomalies.append((
                            f"ALERT_MS_OLED_DROP_{corp_code}_2026_{m_num}",
                            "ms-trend",
                            "OLED_MS_DROP",
                            "WARNING",
                            corp_code,
                            f"{corp_code} 2026-{m_num:02d} LG OLED 점유율 30% 하회 ({ms_val:.1f}%)",
                            "market_share_pct",
                            45.0,
                            float(ms_val),
                            round(((float(ms_val) - 45.0) / 45.0) * 100, 1),
                            now
                        ))

    # Overwrite fact_market_share for MONTHLY
    d_conn.execute("DELETE FROM fact_market_share WHERE period_type = 'MONTHLY';")
    d_conn.executemany("""
    INSERT INTO fact_market_share
    (period_type, period_val, country_code, segment, brand, market_size_qty, market_size_eur, brand_sales_qty, market_share_pct, asp, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, fact_ms)

    if anomalies:
        d_conn.executemany("""
        INSERT OR REPLACE INTO data_anomaly_alerts
        (alert_id, agent_id, alert_type, severity, entity, description, metric_name, old_value, new_value, change_pct, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, anomalies[:30])

    latest_period = max(r[1] for r in fact_ms) if fact_ms else "2026-07"

    # Update agent_sync_status
    d_conn.execute("""
    INSERT OR REPLACE INTO agent_sync_status
    (agent_id, agent_name, last_sync_timestamp, latest_data_period, record_count, status, quality_gate_passed, latest_error_log)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, ("ms-trend", "M/S Trend", now, latest_period, len(fact_ms), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] MS Trend ingested: {len(fact_ms)} records across {len(regions)} regions, latest period: {latest_period}")
    return True, len(fact_ms), None

if __name__ == "__main__":
    ingest_ms_trend()
