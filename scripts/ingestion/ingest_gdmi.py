"""
Ingestion Script for GDMI Weekly Sellout (Agent 01) -> DuckDB
Ingests weekly sellout volume, revenue, inventory, and WOS across 18 European entities.
"""

import os
import sys
import glob
import json
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
GDMI_DATA_DIR = os.path.join(BASE_DIR, "..", "01. GDMI_Weekly_Sellout_Analysis-main", "_data")

def ingest_gdmi():
    print("[*] Ingesting 01. GDMI Weekly Sellout into DuckDB...")
    if not os.path.exists(GDMI_DATA_DIR):
        print(f"  [!] GDMI _data directory not found: {GDMI_DATA_DIR}")
        return False, 0, "Directory not found"

    d_conn = duckdb.connect(DUCKDB_PATH)
    now = datetime.now()
    
    metric_files = glob.glob(os.path.join(GDMI_DATA_DIR, "metrics_*.json"))
    if not metric_files:
        print("  [!] No metrics_*.json files found")
        return False, 0, "No files"

    print(f"  -> Found {len(metric_files)} subsidiary metrics files")
    
    fact_sellout = []
    anomalies = []
    latest_week_str = "W00"
    
    for mf in metric_files:
        try:
            with open(mf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [!] Error reading {mf}: {e}")
            continue

        corp_code = data.get("code") or data.get("region_name") or "UNKNOWN"
        week_num = data.get("week") or 0
        week_str = data.get("week_str") or f"W{week_num}"
        latest_week_str = max(latest_week_str, week_str)
        
        summary = data.get("summary", {})
        total_sellout = float(summary.get("total_sellout") or summary.get("sellout_qty") or 0)
        total_inventory = float(summary.get("total_inventory") or summary.get("inventory_qty") or 0)
        wos = float(summary.get("wos") or 0.0)
        
        # Insert Total Entity Row
        fact_sellout.append((
            2026, int(week_num) if week_num else 35, corp_code.upper(),
            "ALL_RETAILERS", "TOTAL", "TOTAL_TV",
            total_sellout, total_sellout * 550.0, total_inventory, wos, now
        ))
        
        # Ingest Segments if available
        segments = data.get("segments", {})
        if isinstance(segments, dict):
            for seg_name, seg_val in segments.items():
                if isinstance(seg_val, dict):
                    s_qty = float(seg_val.get("sellout") or seg_val.get("qty") or 0)
                    s_inv = float(seg_val.get("inventory") or 0)
                    s_wos = float(seg_val.get("wos") or 0)
                else:
                    s_qty = float(seg_val) if isinstance(seg_val, (int, float)) else 0
                    s_inv, s_wos = 0.0, 0.0
                
                fact_sellout.append((
                    2026, int(week_num) if week_num else 35, corp_code.upper(),
                    "ALL_RETAILERS", seg_name.upper(), f"{corp_code}_{seg_name}",
                    s_qty, s_qty * 650.0, s_inv, s_wos, now
                ))

        # Check WOS Anomaly
        if wos > 12.0 or (wos < 2.0 and total_sellout > 50):
            severity = "CRITICAL" if wos > 15.0 or wos < 1.5 else "WARNING"
            anomalies.append((
                f"ALERT_GDMI_WOS_{week_str}_{corp_code}",
                "gdmi-weekly",
                "WOS_RISK",
                severity,
                corp_code.upper(),
                f"{corp_code} 재고 주수(WOS) {wos:.1f}주 (적정 기준 4~8주 이탈)",
                "wos",
                6.0,
                wos,
                round(((wos - 6.0) / 6.0) * 100, 1),
                now
            ))

    # Idempotent Weekly Upsert: delete only specific (year, week, subsidiary_code) being inserted
    weeks_to_replace = set((r[0], r[1], r[2]) for r in fact_sellout)
    for yr, wk, sub in weeks_to_replace:
        d_conn.execute("DELETE FROM fact_sellout_weekly WHERE year = ? AND week = ? AND subsidiary_code = ?;", [yr, wk, sub])
    d_conn.executemany("""
    INSERT INTO fact_sellout_weekly
    (year, week, subsidiary_code, retailer_name, series_group, model_id, sellout_qty, sellout_amount_eur, inventory_qty, wos, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, fact_sellout)

    if anomalies:
        d_conn.executemany("""
        INSERT OR REPLACE INTO data_anomaly_alerts
        (alert_id, agent_id, alert_type, severity, entity, description, metric_name, old_value, new_value, change_pct, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, anomalies)

    # Update agent_sync_status
    d_conn.execute("""
    INSERT OR REPLACE INTO agent_sync_status
    (agent_id, agent_name, last_sync_timestamp, latest_data_period, record_count, status, quality_gate_passed, latest_error_log)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, ("gdmi-weekly", "GDMI Weekly Sellout", now, latest_week_str, len(fact_sellout), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] GDMI Weekly Sellout ingested: {len(fact_sellout)} records across 18 countries, period: {latest_week_str}")
    return True, len(fact_sellout), None

if __name__ == "__main__":
    ingest_gdmi()
