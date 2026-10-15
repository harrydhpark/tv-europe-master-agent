"""
TV Europe Sales Master AI Agent - DuckDB Schema Initializer
Initializes master_analytics.duckdb with Star Schema Fact & Dimension tables.
"""

import os
import sys
import duckdb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "master_analytics.duckdb")

def init_database():
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"[*] Initializing DuckDB at: {DB_PATH}")
    
    conn = duckdb.connect(DB_PATH)
    
    # 1. Dimension Tables
    print("  -> Creating Dimension Tables...")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS dim_subsidiaries (
        subsidiary_code VARCHAR PRIMARY KEY,
        subsidiary_name_kr VARCHAR,
        subsidiary_name_en VARCHAR,
        currency VARCHAR,
        region VARCHAR,
        pnl_folder VARCHAR
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS dim_lineup_models (
        model_id VARCHAR PRIMARY KEY,
        series VARCHAR,
        inch INTEGER,
        panel_type VARCHAR,
        release_year VARCHAR,
        refresh_rate_hz INTEGER,
        hdmi_ports INTEGER,
        processor VARCHAR
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS dim_fx_rates (
        currency_pair VARCHAR PRIMARY KEY,
        base_currency VARCHAR,
        quote_currency VARCHAR,
        plan_rate DOUBLE,
        current_rate DOUBLE,
        updated_at TIMESTAMP
    );
    """)

    # 2. Fact Tables
    print("  -> Creating Fact Tables...")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_sellout_weekly (
        year INTEGER,
        week INTEGER,
        subsidiary_code VARCHAR,
        retailer_name VARCHAR,
        series_group VARCHAR,
        model_id VARCHAR,
        sellout_qty DOUBLE,
        sellout_amount_eur DOUBLE,
        inventory_qty DOUBLE,
        wos DOUBLE,
        updated_at TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_pnl_monthly (
        year INTEGER,
        month INTEGER,
        subsidiary_code VARCHAR,
        segment VARCHAR,
        gross_sales_mil DOUBLE,
        g_asp DOUBLE,
        deductions_pct DOUBLE,
        net_sales_mil DOUBLE,
        cogs_mil DOUBLE,
        marginal_profit_mil DOUBLE,
        marginal_profit_pct DOUBLE,
        sales_expense_mil DOUBLE,
        operating_profit_mil DOUBLE,
        operating_profit_pct DOUBLE,
        updated_at TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_prices_daily (
        survey_date DATE,
        country_code VARCHAR,
        retailer_name VARCHAR,
        model_id VARCHAR,
        comp_model_id VARCHAR,
        lg_price DOUBLE,
        comp_price DOUBLE,
        price_gap DOUBLE,
        currency VARCHAR,
        is_promotion BOOLEAN,
        anomaly_flag BOOLEAN,
        updated_at TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_market_share (
        period_type VARCHAR, -- 'MONTHLY' or 'WEEKLY'
        period_val VARCHAR,  -- '2026-08' or '2026-W35'
        country_code VARCHAR,
        segment VARCHAR,
        brand VARCHAR,
        market_size_qty DOUBLE,
        market_size_eur DOUBLE,
        brand_sales_qty DOUBLE,
        market_share_pct DOUBLE,
        asp DOUBLE,
        updated_at TIMESTAMP
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS fact_advance_profit (
        order_id VARCHAR PRIMARY KEY,
        subsidiary_code VARCHAR,
        model_id VARCHAR,
        planned_qty DOUBLE,
        estimated_asp DOUBLE,
        estimated_cost DOUBLE,
        marginal_margin_pct DOUBLE,
        margin_risk BOOLEAN,
        shipment_month VARCHAR,
        updated_at TIMESTAMP
    );
    """)

    # 3. Governance & Quality Gate Tables
    print("  -> Creating Governance Tables...")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS agent_sync_status (
        agent_id VARCHAR PRIMARY KEY,
        agent_name VARCHAR,
        last_sync_timestamp TIMESTAMP,
        latest_data_period VARCHAR,
        record_count INTEGER,
        status VARCHAR, -- 'SUCCESS', 'WARNING', 'FAILED'
        quality_gate_passed BOOLEAN,
        latest_error_log VARCHAR
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS data_anomaly_alerts (
        alert_id VARCHAR PRIMARY KEY,
        agent_id VARCHAR,
        alert_type VARCHAR,
        severity VARCHAR, -- 'INFO', 'WARNING', 'CRITICAL'
        entity VARCHAR,
        description VARCHAR,
        metric_name VARCHAR,
        old_value DOUBLE,
        new_value DOUBLE,
        change_pct DOUBLE,
        created_at TIMESTAMP
    );
    """)

    # 4. Populate dim_subsidiaries with 19 European entities
    print("  -> Populating dim_subsidiaries master data...")
    subsidiaries = [
        ('EU_TOTAL', '유럽 전 권역', 'Europe Total', 'EUR', 'EU', 'EU_TOTAL'),
        ('DG', '독일 법인', 'Germany (LGEDG)', 'EUR', 'DACH', '04. DG'),
        ('UK', '영국 법인', 'UK (LGEUK)', 'GBP', 'Western EU', '16. UK'),
        ('FS', '프랑스 법인', 'France (LGEFS)', 'EUR', 'Western EU', '07. FS'),
        ('IS', '이탈리아 법인', 'Italy (LGEIS)', 'EUR', 'Western EU', '09. IS'),
        ('ES', '스페인 법인', 'Spain (LGEES)', 'EUR', 'Western EU', '06. ES'),
        ('SWISS', '스위스 지점', 'Switzerland', 'CHF', 'DACH', '05. Swiss'),
        ('AG', '오스트리아 법인', 'Austria (LGEAG)', 'EUR', 'DACH', '01. AG'),
        ('BN', '베네룩스 법인', 'Benelux (LGEBN)', 'EUR', 'Western EU', '02. BN'),
        ('CK', '체코/슬로바키아 법인', 'Czech/Slovakia (LGECK)', 'CZK', 'Eastern EU', '03. CK'),
        ('PL', '폴란드 법인', 'Poland (LGEPL)', 'PLN', 'Eastern EU', '12. PL'),
        ('PT', '포르투갈 법인', 'Portugal (LGEPT)', 'EUR', 'Western EU', '13. PT'),
        ('HS', '그리스 법인', 'Greece (LGEHS)', 'EUR', 'Eastern EU', '08. HS'),
        ('MK', '헝가리 법인', 'Hungary (LGEMK)', 'HUF', 'Eastern EU', '11. MK'),
        ('RO', '루마니아 법인', 'Romania (LGERO)', 'RON', 'Eastern EU', '14. RO'),
        ('SW', '스웨덴/노르딕 법인', 'Nordic (LGESW)', 'SEK', 'Nordic', '15. SW'),
        ('LA', '발트 3국', 'Baltic (LGELA)', 'EUR', 'Eastern EU', '10. LA'),
        ('RA', '러시아 법인', 'Russia (LGERA)', 'RUB', 'CIS', '17. RA'),
        ('AK', '카자흐스탄 법인', 'Kazakhstan (LGEAK)', 'KZT', 'CIS', '18. AK')
    ]
    
    conn.executemany("""
    INSERT OR REPLACE INTO dim_subsidiaries 
    (subsidiary_code, subsidiary_name_kr, subsidiary_name_en, currency, region, pnl_folder)
    VALUES (?, ?, ?, ?, ?, ?);
    """, subsidiaries)

    # 5. Populate initial dim_fx_rates
    print("  -> Populating dim_fx_rates master data...")
    rates = [
        ('EURUSD', 'EUR', 'USD', 1.080, 1.054, datetime.now()),
        ('GBPUSD', 'GBP', 'USD', 1.270, 1.261, datetime.now()),
        ('EURPLN', 'EUR', 'PLN', 4.320, 4.312, datetime.now()),
        ('EURCHF', 'EUR', 'CHF', 0.965, 0.945, datetime.now()),
        ('EURCZK', 'EUR', 'CZK', 25.10, 25.25, datetime.now()),
        ('EURHUF', 'EUR', 'HUF', 395.0, 401.5, datetime.now())
    ]
    conn.executemany("""
    INSERT OR REPLACE INTO dim_fx_rates
    (currency_pair, base_currency, quote_currency, plan_rate, current_rate, updated_at)
    VALUES (?, ?, ?, ?, ?, ?);
    """, rates)

    row_count = conn.execute("SELECT count(*) FROM dim_subsidiaries").fetchone()[0]
    print(f"[OK] Database initialized successfully. dim_subsidiaries rows: {row_count}")
    conn.close()

if __name__ == "__main__":
    init_database()
