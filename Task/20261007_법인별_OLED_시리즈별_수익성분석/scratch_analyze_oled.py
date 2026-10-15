# -*- coding: utf-8 -*-
import os
import glob
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis\법인별"

COUNTRY_MAP = {
    '01. AG': ('AG', '오스트리아 (Austria)', 'EUR'),
    '02. BN': ('BN', '베네룩스 (Benelux)', 'EUR'),
    '03. CK': ('CK', '체코 (Czech)', 'EUR'),
    '04. DG': ('DG', '독일 (Germany)', 'EUR'),
    '05. Swiss': ('Swiss', '스위스 (Switzerland)', 'CHF'),
    '06. ES': ('ES', '스페인 (Spain)', 'EUR'),
    '07. FS': ('FS', '프랑스 (France)', 'EUR'),
    '08. HS': ('HS', '그리스 (Greece)', 'EUR'),
    '09. IS': ('IS', '이탈리아 (Italy)', 'EUR'),
    '10. LA': ('LA', '라트비아/발틱 (Latvia)', 'EUR'),
    '11. MK': ('MK', '헝가리 (Hungary)', 'EUR'),
    '12. PL': ('PL', '폴란드 (Poland)', 'EUR'),
    '13. PT': ('PT', '포르투갈 (Portugal)', 'EUR'),
    '14. RO': ('RO', '루마니아 (Romania)', 'EUR'),
    '15. SW': ('SW', '스웨덴/노르딕 (Sweden)', 'SEK'),
    '16. UK': ('UK', '영국 (UK)', 'GBP'),
    '17. RA': ('RA', '러시아 (Russia)', 'USD'),
}

def analyze_parquet_country(cfolder, pq_path):
    cols_to_load = ['Year', 'Month', 'BLU', 'Series', 'Net Sales', 'Operating Income', 'Marginal Profit', 'Qty_Actual']
    # Check if optional columns exist
    df_sample = pd.read_parquet(pq_path)
    actual_cols = [c for c in cols_to_load if c in df_sample.columns]
    for opt in ['OLED/UHD', 'Tool']:
        if opt in df_sample.columns:
            actual_cols.append(opt)
            
    df = df_sample[actual_cols].copy()
    
    # Filter 2026 YTD (Month 1~8)
    df26 = df[(df['Year'] == 2026) & (df['Month'] <= 8)].copy()
    if len(df26) == 0:
        return None
        
    # OLED Filter
    oled_mask = (df26['BLU'].astype(str).str.upper() == 'OLED')
    if 'OLED/UHD' in df26.columns:
        oled_mask |= (df26['OLED/UHD'].astype(str).str.upper() == 'OLED')
    oled = df26[oled_mask].copy()
    
    if len(oled) == 0:
        return None
        
    def map_series(row):
        s = str(row.get('Series', '')).strip().upper()
        t = str(row.get('Tool', '')).strip().upper()
        if s == 'W' or t.startswith('W'): return 'W'
        if s == 'G' or t.startswith('G'): return 'G'
        if s == 'C' or t.startswith('C'): return 'C'
        if s == 'B' or t.startswith('B'): return 'B'
        return '기타(M/T/A/Z)'
        
    oled['Series_Group'] = oled.apply(map_series, axis=1)
    
    agg = oled.groupby('Series_Group').agg({
        'Net Sales': 'sum',
        'Operating Income': 'sum',
        'Marginal Profit': 'sum',
        'Qty_Actual': 'sum'
    })
    
    return agg

def get_dg_data():
    # Extracted from DG Series sheet YTD
    # Y26: G6 (Sales 500,199, MP 213,262, COI 125,227, Qty 299)
    #      C6 (Sales 430,414, MP 180,948, COI 100,431, Qty 347)
    #      B6 (Sales 56,787, MP 23,647, COI 12,860, Qty 46)
    # Y25: M5 (Sales 19,376, MP 9,553, COI 6,307, Qty 7)
    #      G5 (Sales 12,224,462, MP 4,252,387, COI 1,889,615, Qty 8523)
    #      C5 (Sales 27,915,371, MP 6,806,489, COI 1,393,509, Qty 30557)
    #      B5 (Sales 5,499,715, MP 867,849, COI -305,289, Qty 7462)
    data = {
        'G': {'Net Sales': 12724661.0, 'Marginal Profit': 4465649.0, 'Operating Income': 2014842.0, 'Qty_Actual': 8822.0},
        'C': {'Net Sales': 28345785.0, 'Marginal Profit': 6987437.0, 'Operating Income': 1493940.0, 'Qty_Actual': 30904.0},
        'B': {'Net Sales': 5556502.0, 'Marginal Profit': 891496.0, 'Operating Income': -292429.0, 'Qty_Actual': 7508.0},
        '기타(M/T/A/Z)': {'Net Sales': 19376.0, 'Marginal Profit': 9553.0, 'Operating Income': 6307.0, 'Qty_Actual': 7.0},
        'W': {'Net Sales': 0.0, 'Marginal Profit': 0.0, 'Operating Income': 0.0, 'Qty_Actual': 0.0}
    }
    return pd.DataFrame(data).T

def run():
    all_summary = []
    
    for cfolder in sorted(COUNTRY_MAP.keys()):
        code, name_kr, curr = COUNTRY_MAP[cfolder]
        print(f"Processing {cfolder} ({name_kr})...", flush=True)
        
        if cfolder == '04. DG':
            agg = get_dg_data()
        else:
            pq_path = os.path.join(BASE_DIR, cfolder, "cache", "raw_data.parquet")
            if not os.path.exists(pq_path):
                print(f"  [SKIP] No parquet for {cfolder}")
                continue
            agg = analyze_parquet_country(cfolder, pq_path)
            if agg is None:
                print(f"  [SKIP] No 2026 YTD OLED for {cfolder}")
                continue
                
        ttl_sales = agg['Net Sales'].sum()
        ttl_coi = agg['Operating Income'].sum()
        ttl_mp = agg['Marginal Profit'].sum()
        ttl_qty = agg['Qty_Actual'].sum()
        
        series_order = ['W', 'G', 'C', 'B', '기타(M/T/A/Z)', 'Total OLED']
        for s in series_order:
            if s == 'Total OLED':
                sales = ttl_sales
                coi = ttl_coi
                mp = ttl_mp
                qty = ttl_qty
                mix = 100.0
            elif s in agg.index:
                r = agg.loc[s]
                sales = float(r['Net Sales'])
                coi = float(r['Operating Income'])
                mp = float(r['Marginal Profit'])
                qty = float(r['Qty_Actual'])
                mix = (sales / ttl_sales * 100) if ttl_sales > 0 else 0.0
            else:
                sales = 0.0
                coi = 0.0
                mp = 0.0
                qty = 0.0
                mix = 0.0
                
            coi_pct = (coi / sales * 100) if sales > 0 else 0.0
            mp_pct = (mp / sales * 100) if sales > 0 else 0.0
            asp = (sales / qty) if qty > 0 else 0.0
            
            all_summary.append({
                'Folder': cfolder,
                'Code': code,
                'Country': name_kr,
                'Currency': curr,
                'Series': s,
                'Net Sales': sales,
                'Sales Mix%': mix,
                'Operating Income (COI)': coi,
                'COI%': coi_pct,
                'Marginal Profit (MP)': mp,
                'MP%': mp_pct,
                'Qty': qty,
                'ASP': asp
            })
            
    df_out = pd.DataFrame(all_summary)
    csv_path = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scratch_oled_pnl_summary.csv"
    df_out.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\nSuccessfully generated OLED P&L summary: {csv_path}", flush=True)
    
    # Print Pivot View
    print("\n" + "="*120)
    print(f"{'Code':<6} | {'Country':<18} | {'Series':<6} | {'Net Sales':>14} | {'Sales Mix%':>10} | {'COI%':>8} | {'MP%':>8} | {'Qty':>8}")
    print("="*120)
    for code in df_out['Code'].unique():
        sub = df_out[df_out['Code'] == code]
        cname = sub['Country'].iloc[0]
        curr = sub['Currency'].iloc[0]
        for _, r in sub.iterrows():
            s = r['Series']
            sales_str = f"{r['Net Sales']:,.0f} {curr}"
            print(f"{code:<6} | {cname:<18} | {s:<6} | {sales_str:>14} | {r['Sales Mix%']:>9.1f}% | {r['COI%']:>7.1f}% | {r['MP%']:>7.1f}% | {r['Qty']:>8,.0f}")
        print("-" * 120)

if __name__ == "__main__":
    run()
