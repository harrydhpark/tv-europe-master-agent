"""
Ingestion Script for TV P&L Analysis (Agent 05) -> DuckDB
Ingests monthly Gross/Net Sales, Deductions, COGS, Marginal Profit, and Operating Profit across European subsidiaries.
"""

import os
import sys
import glob
import json
import re
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DUCKDB_PATH = os.path.join(BASE_DIR, "data", "master_analytics.duckdb")
PNL_DIR = os.path.join(BASE_DIR, "..", "05. TV P&L Analysis", "법인별")

def extract_json_from_html(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'<script id="dashboard-data" type="application/json">\s*(\{.*?\})\s*</script>', content, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        print(f"  [!] Error parsing HTML {html_path}: {e}")
    return None

def ingest_pnl():
    print("[*] Ingesting 05. TV P&L Analysis into DuckDB...")
    if not os.path.exists(PNL_DIR):
        print(f"  [!] P&L directory not found: {PNL_DIR}")
        return False, 0, "Directory not found"

    d_conn = duckdb.connect(DUCKDB_PATH)
    now = datetime.now()
    
    html_files = glob.glob(os.path.join(PNL_DIR, "*", "*_Report.html"))
    if not html_files:
        html_files = glob.glob(os.path.join(PNL_DIR, "*", "*.html"))
        html_files = [f for f in html_files if not f.endswith("report_template.html")]

    print(f"  -> Found {len(html_files)} subsidiary P&L report files")
    
    fact_pnl = []
    anomalies = []
    latest_period = "2026-08"
    
    for hf in html_files:
        folder_name = os.path.basename(os.path.dirname(hf))
        # folder_name e.g. "04. DG", "05. Swiss", "16. UK"
        code_part = folder_name.split(". ")[-1].strip().upper()
        if code_part == "SWISS":
            corp_code = "SWISS"
        else:
            corp_code = code_part
            
        data = extract_json_from_html(hf)
        if not data:
            continue
            
        latest_year = data.get("LATEST_YEAR", 2026)
        latest_month = data.get("LATEST_MONTH", 8)
        latest_period = f"{latest_year}-{latest_month:02d}"
        
        std = data.get("DATA", {}).get("standard", {})
        monthly_trend = std.get("monthly_trend", [])
        
        for m in monthly_trend:
            # m has fields like: month, gross, net, cogs, marginal_profit, op_profit, op_margin, etc.
            m_num = m.get("month") or m.get("m") or 0
            if isinstance(m_num, str) and m_num.isdigit():
                m_num = int(m_num)
            if not m_num:
                continue
                
            gross_sales = float(m.get("gross_sales") or m.get("gross") or 0.0)
            net_sales = float(m.get("net_sales") or m.get("net") or 0.0)
            cogs = float(m.get("cogs") or 0.0)
            mp = float(m.get("marginal_profit") or m.get("mp") or 0.0)
            mp_pct = float(m.get("marginal_profit_pct") or m.get("mp_margin") or 0.0)
            op = float(m.get("operating_profit") or m.get("op") or 0.0)
            op_pct = float(m.get("operating_profit_pct") or m.get("op_margin") or 0.0)
            deductions_pct = round(((gross_sales - net_sales) / gross_sales) * 100, 1) if gross_sales > 0 else 0.0
            sales_exp = round(mp - op, 2) if (mp and op) else 0.0
            
            fact_pnl.append((
                latest_year, m_num, corp_code, "TOTAL",
                gross_sales, 0.0, deductions_pct, net_sales,
                cogs, mp, mp_pct, sales_exp, op, op_pct, now
            ))
            
            # Anomaly check: Operating margin deeply negative
            if m_num == latest_month and op_pct < -5.0:
                anomalies.append((
                    f"ALERT_PNL_OP_{latest_period}_{corp_code}",
                    "pnl-analysis",
                    "PROFITABILITY_LOSS",
                    "CRITICAL" if op_pct < -10.0 else "WARNING",
                    corp_code,
                    f"{corp_code} {latest_period} 영업이익률 적자 지속: {op_pct:.1f}%",
                    "operating_profit_pct",
                    0.0,
                    op_pct,
                    op_pct,
                    now
                ))

    # Idempotent Monthly Upsert: delete only specific (year, month, subsidiary_code) being inserted
    periods_to_replace = set((r[0], r[1], r[2]) for r in fact_pnl)
    for yr, mo, sub in periods_to_replace:
        d_conn.execute("DELETE FROM fact_pnl_monthly WHERE year = ? AND month = ? AND subsidiary_code = ?;", [yr, mo, sub])
    d_conn.executemany("""
    INSERT INTO fact_pnl_monthly
    (year, month, subsidiary_code, segment, gross_sales_mil, g_asp, deductions_pct, net_sales_mil, cogs_mil, marginal_profit_mil, marginal_profit_pct, sales_expense_mil, operating_profit_mil, operating_profit_pct, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, fact_pnl)

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
    """, ("pnl-analysis", "TV P&L Analysis", now, latest_period, len(fact_pnl), "SUCCESS", True, None))

    d_conn.close()
    print(f"[OK] TV P&L Analysis ingested: {len(fact_pnl)} monthly records across subsidiaries, period: {latest_period}")
    return True, len(fact_pnl), None

if __name__ == "__main__":
    ingest_pnl()
