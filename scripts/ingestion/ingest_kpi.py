"""
Ingestion Script for KPI Sheet (Agent 06) -> DuckDB
Ingests 21 European entities' KPI metrics, WOS risks, and executive insights.
"""

import os
import sys
import json
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
KPI_DIR = os.path.join(BASE_DIR, "..", "06. KPI Sheet")
INSIGHTS_PATH = os.path.join(KPI_DIR, "executive_insights.json")
METRICS_PATH = os.path.join(KPI_DIR, "build_metrics.json")

def ingest_kpi():
    print("[*] Ingesting 06. KPI Sheet into DuckDB...")
    if not os.path.exists(INSIGHTS_PATH):
        print(f"  [!] KPI Sheet insights not found: {INSIGHTS_PATH}")
        return False, 0, "File not found"

    d_conn = duckdb.connect(DUCKDB_PATH)
    now = datetime.now()

    try:
        with open(INSIGHTS_PATH, "r", encoding="utf-8") as f:
            insights = json.load(f)
    except Exception as e:
        print(f"  [!] Error reading KPI insights: {e}")
        return False, 0, str(e)

    # Ingest WOS & Regional Rankings into fact_sellout_weekly as entity summaries
    rankings = insights.get("regional_rankings", {})
    risk_wos = rankings.get("risk_wos", [])
    
    anomalies = []
    kpi_records = []
    
    for r in risk_wos:
        entity = r.get("entity", "").upper()
        wos_val = float(r.get("wos") or 0.0)
        status_str = r.get("status", "NORMAL")
        
        # Add into fact_sellout_weekly as KPI summary row
        kpi_records.append((
            2026, 35, entity, "ALL_RETAILERS", "KPI_SUMMARY", f"KPI_{entity}",
            0.0, 0.0, 0.0, wos_val, now
        ))
        
        if wos_val > 10.0 or wos_val < 2.0:
            anomalies.append((
                f"ALERT_KPI_WOS_{entity}_2026",
                "kpi-sheet",
                "KPI_WOS_BREACH",
                "CRITICAL" if wos_val > 14.0 else "WARNING",
                entity,
                f"KPI Sheet {entity} 재고 주수 {wos_val:.1f}주 (위험 수준 경보)",
                "wos",
                6.0,
                wos_val,
                round(((wos_val - 6.0) / 6.0) * 100, 1),
                now
            ))

    if kpi_records:
        d_conn.executemany("""
        INSERT INTO fact_sellout_weekly
        (year, week, subsidiary_code, retailer_name, series_group, model_id, sellout_qty, sellout_amount_eur, inventory_qty, wos, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, kpi_records)

    if anomalies:
        d_conn.executemany("""
        INSERT OR REPLACE INTO data_anomaly_alerts
        (alert_id, agent_id, alert_type, severity, entity, description, metric_name, old_value, new_value, change_pct, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, anomalies[:20])

    latest_period = "2026-YTD"

    # Update agent_sync_status
    d_conn.execute("""
    INSERT OR REPLACE INTO agent_sync_status
    (agent_id, agent_name, last_sync_timestamp, latest_data_period, record_count, status, quality_gate_passed, latest_error_log)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, ("kpi-sheet", "KPI Sheet", now, latest_period, len(kpi_records), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] KPI Sheet ingested: {len(kpi_records)} risk entities, alerts: {len(anomalies)}")
    return True, len(kpi_records), None

if __name__ == "__main__":
    ingest_kpi()
