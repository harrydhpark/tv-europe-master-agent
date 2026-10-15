"""
Ingestion Script for FX-Monitor (Agent 03) -> DuckDB
Ingests real-time exchange rates and FX commentary.
"""

import os
import sys
import json
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
FX_RATES_PATH = os.path.join(BASE_DIR, "..", "03. FX-Monitor-main", "data", "real_rates.json")

def ingest_fx():
    print("[*] Ingesting 03. FX-Monitor into DuckDB...")
    if not os.path.exists(FX_RATES_PATH):
        print(f"  [!] FX rates not found: {FX_RATES_PATH}")
        return False, 0, "File not found"

    d_conn = duckdb.connect(DUCKDB_PATH)
    now = datetime.now()

    try:
        with open(FX_RATES_PATH, "r", encoding="utf-8") as f:
            raw_rates = json.load(f)
    except Exception as e:
        print(f"  [!] Error reading FX rates: {e}")
        return False, 0, str(e)

    # Standard Plan Rates
    PLAN_RATES = {
        'EURUSD': 1.080, 'GBPUSD': 1.270, 'EURPLN': 4.320, 
        'EURCHF': 0.965, 'EURCZK': 25.10, 'EURHUF': 395.0,
        'EURSEK': 11.45, 'EURNOK': 11.60
    }

    rates_to_insert = []
    anomalies = []

    for curr_code, curr_data in raw_rates.items():
        if not isinstance(curr_data, dict):
            continue
        curr_code = curr_code.upper()
        pair = f"EUR{curr_code}" if curr_code != "EUR" else "EURUSD"
        
        # Get latest daily rate
        daily_list = curr_data.get("september_daily", [])
        if daily_list and isinstance(daily_list, list):
            rate_val = float(daily_list[-1].get("rate") or curr_data.get("cumulative_average") or 1.0)
        else:
            rate_val = float(curr_data.get("cumulative_average") or 1.0)
            
        base = "EUR"
        quote = curr_code if curr_code != "EUR" else "USD"
        plan = PLAN_RATES.get(pair, rate_val)
        gap_pct = round(((rate_val - plan) / plan) * 100, 2)
        
        rates_to_insert.append((
            pair, base, quote, plan, rate_val, now
        ))
        
        # Check FX volatility anomaly (e.g. > 3% deviation from plan)
        if abs(gap_pct) >= 3.0:
            anomalies.append((
                f"ALERT_FX_{pair}_{now.strftime('%Y%m%d')}",
                "fx-monitor",
                "FX_RATE_VOLATILITY",
                "WARNING" if abs(gap_pct) < 5.0 else "CRITICAL",
                pair,
                f"{pair} 실시간 환율 {rate_val:.4f} (연초 계획 {plan:.4f} 대비 {gap_pct:+.2f}% 변동)",
                "fx_rate_gap_pct",
                plan,
                rate_val,
                gap_pct,
                now
            ))

    if rates_to_insert:
        d_conn.executemany("""
        INSERT OR REPLACE INTO dim_fx_rates
        (currency_pair, base_currency, quote_currency, plan_rate, current_rate, updated_at)
        VALUES (?, ?, ?, ?, ?, ?);
        """, rates_to_insert)

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
    """, ("fx-monitor", "FX-Monitor", now, "LIVE", len(rates_to_insert), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] FX-Monitor ingested: {len(rates_to_insert)} currency pairs, alerts: {len(anomalies)}")
    return True, len(rates_to_insert), None

if __name__ == "__main__":
    ingest_fx()
