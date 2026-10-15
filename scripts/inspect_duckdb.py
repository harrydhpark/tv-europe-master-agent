import duckdb

con = duckdb.connect(r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\data\master_analytics.duckdb", read_only=True)

print("--- fact_prices_daily for ES (Spain) ---")
df_p = con.execute('''
    SELECT * 
    FROM fact_prices_daily 
    WHERE country_code = 'ES'
    ORDER BY survey_date DESC, lg_price
''').df()
print(f"Total ES records in fact_prices_daily: {len(df_p)}")
print(df_p.head(30).to_string())

print("\n--- fact_advance_profit for ES (Spain) ---")
df_ap = con.execute('''
    SELECT * 
    FROM fact_advance_profit 
    WHERE subsidiary_code = 'LGEES' OR subsidiary_code = 'ES'
    LIMIT 30
''').df()
print(f"Total ES records in fact_advance_profit: {len(df_ap)}")
print(df_ap.to_string())
