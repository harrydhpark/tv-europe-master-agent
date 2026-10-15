import sqlite3
import pandas as pd

db_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\04. Price Tracker\data\price_history.db"
con = sqlite3.connect(db_path)

query = '''
    SELECT date, retailer, manufacturer, display_size_inch, base_model, model_code, panel_type, selling_price, original_price, promo_text
    FROM daily_prices
    WHERE country = 'ES' 
      AND display_size_inch IN (55, 65)
      AND (panel_type LIKE '%OLED%' OR base_model LIKE '%OLED%' OR model_code LIKE '%OLED%' OR base_model LIKE '%S90%' OR base_model LIKE '%S85%' OR base_model LIKE '%S95%' OR base_model LIKE '%C4%' OR base_model LIKE '%B4%' OR base_model LIKE '%G4%' OR base_model LIKE '%C5%' OR base_model LIKE '%B5%' OR base_model LIKE '%G5%' OR base_model LIKE '%C6%' OR base_model LIKE '%B6%' OR base_model LIKE '%G6%')
    ORDER BY display_size_inch, base_model, date DESC
'''

df = pd.read_sql_query(query, con)
print(f"Total matching records: {len(df)}")
print("\nUnique Base Models:")
print(df[['manufacturer', 'display_size_inch', 'base_model']].drop_duplicates().to_string())

print("\nLatest Prices (2026-09-29):")
latest_df = df[df['date'] == '2026-09-29'].sort_values(by=['display_size_inch', 'manufacturer', 'selling_price'])
print(latest_df[['manufacturer', 'display_size_inch', 'base_model', 'model_code', 'selling_price', 'original_price', 'promo_text']].to_string())
