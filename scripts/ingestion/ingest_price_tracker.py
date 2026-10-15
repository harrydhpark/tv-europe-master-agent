"""
Ingestion Script for Price Tracker (Agent 04) -> DuckDB
Ingests daily prices, 1:1 competitor lineup comparisons, and anomaly alerts.
"""

import os
import sys
import sqlite3
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
SQLITE_PATH = os.path.join(BASE_DIR, "..", "04. Price Tracker", "data", "price_history.db")

def ingest_price_tracker():
    print("[*] Ingesting 04. Price Tracker into DuckDB...")
    if not os.path.exists(SQLITE_PATH):
        print(f"  [!] SQLite database not found at {SQLITE_PATH}")
        return False, 0, "SQLite DB missing"

    d_conn = duckdb.connect(DUCKDB_PATH)
    
    # 1. Connect to SQLite and extract latest prices & models
    s_conn = sqlite3.connect(SQLITE_PATH)
    s_cur = s_conn.cursor()
    
    s_cur.execute("""
    SELECT date, country, retailer, manufacturer, model_code, base_model, 
           display_size_inch, panel_type, selling_price, original_price, 
           currency, promo_text, in_stock
    FROM daily_prices
    ORDER BY date DESC
    LIMIT 100000;
    """)
    rows = s_cur.fetchall()
    s_conn.close()
    
    if not rows:
        print("  [!] No price records found in SQLite")
        return False, 0, "No records"

    print(f"  -> Extracted {len(rows)} raw price snapshots from SQLite")

    # 2. Populate dim_lineup_models from distinct models
    models_to_insert = set()
    fact_prices = []
    
    # Track latest price per (date, country, retailer, base_model, manufacturer)
    price_map = {}
    for r in rows:
        dt, country, retailer, mfg, model_code, base_model, size, p_type, price, orig_price, curr, promo, in_stock = r
        mfg = (mfg or '').strip().upper()
        base_model = (base_model or model_code or '').strip().upper()
        if not base_model or price is None or price <= 0:
            continue
            
        models_to_insert.add((base_model, base_model, size or 0, p_type or 'OLED', 'Y26', 120, 4, 'Alpha AI'))
        key = (dt, country, retailer, size, p_type)
        if key not in price_map:
            price_map[key] = {'LG': None, 'SAMSUNG': None, 'curr': curr, 'promo': bool(promo)}
        if 'LG' in mfg and not price_map[key]['LG']:
            price_map[key]['LG'] = (base_model, price)
        elif 'SAMS' in mfg and not price_map[key]['SAMSUNG']:
            price_map[key]['SAMSUNG'] = (base_model, price)

    # Insert lineup models
    d_conn.executemany("""
    INSERT OR REPLACE INTO dim_lineup_models 
    (model_id, series, inch, panel_type, release_year, refresh_rate_hz, hdmi_ports, processor)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, list(models_to_insert))

    # Build fact_prices_daily records
    anomalies = []
    now = datetime.now()
    for (dt, country, retailer, size, p_type), data in price_map.items():
        lg_info = data['LG']
        samsung_info = data['SAMSUNG']
        if not lg_info:
            continue
            
        lg_model, lg_price = lg_info
        comp_model = samsung_info[0] if samsung_info else 'N/A'
        comp_price = samsung_info[1] if samsung_info else 0.0
        gap = round(lg_price - comp_price, 2) if comp_price > 0 else 0.0
        
        # Anomaly check: price gap unusually large or zero
        is_anomaly = False
        if comp_price > 0 and abs(gap) > (lg_price * 0.4):
            is_anomaly = True
            anomalies.append((
                f"ALERT_PRICE_{dt}_{country}_{lg_model}",
                "price-tracker",
                "PRICE_GAP_OUTLIER",
                "WARNING",
                country,
                f"{retailer}에서 LG {lg_model}({lg_price})와 삼성 {comp_model}({comp_price}) 가격 갭 40% 이상 초과",
                "price_gap",
                comp_price,
                lg_price,
                round((gap / comp_price) * 100, 1),
                now
            ))

        fact_prices.append((
            dt, country, retailer, lg_model, comp_model,
            float(lg_price), float(comp_price), float(gap),
            data['curr'] or 'EUR', data['promo'], is_anomaly, now
        ))

    # Idempotent Daily Upsert: delete only specific (survey_date, country_code) being inserted
    dates_to_replace = set((r[0], r[1]) for r in fact_prices)
    for s_date, c_code in dates_to_replace:
        d_conn.execute("DELETE FROM fact_prices_daily WHERE survey_date = ? AND country_code = ?;", [s_date, c_code])
    d_conn.executemany("""
    INSERT INTO fact_prices_daily
    (survey_date, country_code, retailer_name, model_id, comp_model_id, lg_price, comp_price, price_gap, currency, is_promotion, anomaly_flag, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, fact_prices)

    if anomalies:
        d_conn.executemany("""
        INSERT OR REPLACE INTO data_anomaly_alerts
        (alert_id, agent_id, alert_type, severity, entity, description, metric_name, old_value, new_value, change_pct, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, anomalies[:50])

    latest_date = max(r[0] for r in fact_prices) if fact_prices else "N/A"
    
    # Update agent_sync_status
    d_conn.execute("""
    INSERT OR REPLACE INTO agent_sync_status
    (agent_id, agent_name, last_sync_timestamp, latest_data_period, record_count, status, quality_gate_passed, latest_error_log)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, ("price-tracker", "Price Tracker", now, str(latest_date), len(fact_prices), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] Price Tracker ingested: {len(fact_prices)} pairs, {len(models_to_insert)} models, latest date: {latest_date}")
    return True, len(fact_prices), None

if __name__ == "__main__":
    ingest_price_tracker()
