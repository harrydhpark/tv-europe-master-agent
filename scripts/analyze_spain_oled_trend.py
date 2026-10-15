import sqlite3
import pandas as pd

db_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\04. Price Tracker\data\price_history.db"
con = sqlite3.connect(db_path)

query = '''
    SELECT date, manufacturer, display_size_inch, model_code, selling_price, original_price, promo_text
    FROM daily_prices
    WHERE country = 'ES' 
      AND display_size_inch IN (55, 65)
      AND (
          (manufacturer = 'LG' AND (model_code LIKE 'OLED55%' OR model_code LIKE 'OLED65%'))
          OR (manufacturer = 'SAMSUNG' AND (model_code LIKE 'TQ55S%' OR model_code LIKE 'TQ65S%' OR model_code LIKE 'QE55S%' OR model_code LIKE 'QE65S%'))
      )
    ORDER BY date, display_size_inch, manufacturer, selling_price
'''

df = pd.read_sql_query(query, con)
print(f"Total pure OLED records: {len(df)}")

def classify_oled(row):
    m = row['model_code'].upper()
    size = row['display_size_inch']
    man = row['manufacturer'].upper()
    if man == 'LG':
        if 'B6' in m: return f"LG OLED {size}B6"
        if 'C6' in m: return f"LG OLED {size}C6"
        if 'G6' in m: return f"LG OLED {size}G6"
        if 'B5' in m or 'B4' in m: return f"LG OLED {size}B(Old)"
        if 'C5' in m or 'C4' in m: return f"LG OLED {size}C(Old)"
        if 'G5' in m or 'G4' in m: return f"LG OLED {size}G(Old)"
        if 'M5' in m or 'M6' in m: return f"LG OLED {size}M"
        return f"LG OLED {size}Other"
    else:
        if 'S85' in m or 'S83' in m or 'S82' in m: return f"Sam OLED {size}S85"
        if 'S90' in m or 'S92' in m or 'S93' in m or 'S94' in m: return f"Sam OLED {size}S90"
        if 'S95' in m: return f"Sam OLED {size}S95"
        if 'S99' in m: return f"Sam OLED {size}S99"
        return f"Sam OLED {size}Other"

df['series'] = df.apply(classify_oled, axis=1)

print("\n--- Pure OLED Min Price by Date & Series (EUR) ---")
pivot = df.groupby(['date', 'series'])['selling_price'].min().unstack()
print(pivot.dropna(how='all').to_string())

# Print all models on 2026-09-29
print("\n--- All Pure OLED Models in Spain MediaMarkt on 2026-09-29 ---")
latest = df[df['date'] == '2026-09-29'].sort_values(['display_size_inch', 'manufacturer', 'selling_price'])
print(latest[['manufacturer', 'display_size_inch', 'series', 'model_code', 'selling_price', 'original_price', 'promo_text']].to_string(index=False))
