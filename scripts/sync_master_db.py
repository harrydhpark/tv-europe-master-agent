"""
TV Europe Sales Master AI Agent - Central Database Synchronizer & Orchestrator
Coordinates multi-agent ETL into master_analytics.duckdb with Data Quality Gates.
"""

import os
import sys
import argparse
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
INGEST_DIR = os.path.join(SCRIPTS_DIR, "ingestion")
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "master_analytics.duckdb")

# Add scripts directory to path
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, INGEST_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from init_master_db import init_database
from ingest_price_tracker import ingest_price_tracker
from ingest_gdmi import ingest_gdmi
from ingest_pnl import ingest_pnl
from ingest_ms_trend import ingest_ms_trend
from ingest_advance_profit import ingest_advance_profit
from ingest_kpi import ingest_kpi
from ingest_fx import ingest_fx

AGENT_INGESTORS = {
    "price-tracker": ("Price Tracker", ingest_price_tracker),
    "gdmi-weekly": ("GDMI Weekly Sellout", ingest_gdmi),
    "pnl-analysis": ("TV P&L Analysis", ingest_pnl),
    "ms-trend": ("M/S Trend", ingest_ms_trend),
    "advance-profitability": ("선행 수익성 분석", ingest_advance_profit),
    "kpi-sheet": ("KPI Sheet", ingest_kpi),
    "fx-monitor": ("FX-Monitor", ingest_fx)
}

def print_status_table():
    if not os.path.exists(DB_PATH):
        print(f"[!] Master DB not found at: {DB_PATH}")
        return

    conn = duckdb.connect(DB_PATH)
    print("\n" + "="*80)
    print(" 🚀 TV Europe Master AI Agent — Central Analytics DB Status")
    print("="*80)
    
    # 1. Agent Sync Status
    print("\n[1] Sub-Agent Ingestion & Quality Gate Status:")
    print(f"{'Agent ID':<22} | {'Status':<8} | {'Quality Gate':<12} | {'Latest Period':<14} | {'Records':<8}")
    print("-" * 75)
    
    statuses = conn.execute("""
        SELECT agent_id, status, quality_gate_passed, latest_data_period, record_count 
        FROM agent_sync_status 
        ORDER BY last_sync_timestamp DESC;
    """).fetchall()
    
    for row in statuses:
        ag_id, st, qg, period, cnt = row
        qg_str = "PASSED" if qg else "FAILED"
        print(f"{ag_id:<22} | {st:<8} | {qg_str:<12} | {str(period):<14} | {cnt:<8}")

    # 2. Table Record Counts
    print("\n[2] DuckDB Fact & Dimension Table Row Counts:")
    tables = [
        "dim_subsidiaries", "dim_lineup_models", "dim_fx_rates",
        "fact_sellout_weekly", "fact_pnl_monthly", "fact_prices_daily",
        "fact_market_share", "fact_advance_profit", "data_anomaly_alerts"
    ]
    for tbl in tables:
        cnt = conn.execute(f"SELECT count(*) FROM {tbl}").fetchone()[0]
        print(f"  • {tbl:<24}: {cnt:>6} rows")

    # 3. Recent Anomaly Alerts
    alert_cnt = conn.execute("SELECT count(*) FROM data_anomaly_alerts").fetchone()[0]
    print(f"\n[3] Active Anomaly Alerts Detected: {alert_cnt} items")
    if alert_cnt > 0:
        recent_alerts = conn.execute("""
            SELECT alert_type, severity, entity, description 
            FROM data_anomaly_alerts 
            ORDER BY created_at DESC 
            LIMIT 5;
        """).fetchall()
        for a in recent_alerts:
            print(f"  - [{a[1]}] ({a[0]}) {a[2]}: {a[3]}")
            
    print("="*80 + "\n")
    conn.close()

def run_sync(agent_target=None, file_path=None):
    if not os.path.exists(DB_PATH):
        init_database()

    print(f"\n[*] Starting Master DB Synchronization at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    if file_path:
        print(f"  -> Target File: {file_path}")
    
    targets = AGENT_INGESTORS.keys() if (not agent_target or agent_target == "all") else [agent_target]
    
    success_count = 0
    fail_count = 0
    
    for aid in targets:
        if aid not in AGENT_INGESTORS:
            print(f"[!] Unknown agent: {aid}. Available: {list(AGENT_INGESTORS.keys())}")
            continue
            
        aname, func = AGENT_INGESTORS[aid]
        print(f"\n--- [Syncing] {aid} ({aname}) ---")
        try:
            ok, count, err = func()
            if ok:
                success_count += 1
            else:
                fail_count += 1
                print(f"  [X] Failed: {err}")
        except Exception as e:
            fail_count += 1
            print(f"  [!] Exception during {aid} sync: {e}")

    print(f"\n[*] Sync finished: {success_count} succeeded, {fail_count} failed.")
    print_status_table()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master Agent Database Synchronizer")
    parser.add_argument("--all", action="store_true", help="Sync all sub-agents")
    parser.add_argument("--agent", type=str, help="Sync specific sub-agent ID")
    parser.add_argument("--file", type=str, help="Specific file path that triggered synchronization")
    parser.add_argument("--status", action="store_true", help="Print current DB and agent sync status")
    
    args = parser.parse_args()
    
    if args.status:
        print_status_table()
    elif args.agent:
        run_sync(args.agent, args.file)
    else:
        run_sync("all", args.file)
