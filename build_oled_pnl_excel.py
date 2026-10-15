# -*- coding: utf-8 -*-
"""
Generates the Executive Excel Workbook for 2026 YTD OLED Series Profitability
"""
import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CSV_PATH = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\scratch_oled_pnl_summary.csv"
OUTPUT_EXCEL = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\2026_OLED_Series_Profitability_by_Country.xlsx"

def build_excel():
    df = pd.read_csv(CSV_PATH)
    
    # Calculate Europe 16 Aggregate
    df_eu16 = df[df['Code'] != 'RA']
    eu_agg = df_eu16.groupby('Series').agg({
        'Net Sales': 'sum',
        'Operating Income (COI)': 'sum',
        'Marginal Profit (MP)': 'sum',
        'Qty': 'sum'
    }).reset_index()
    
    ttl_sales = eu_agg.loc[eu_agg['Series'] == 'Total OLED', 'Net Sales'].values[0]
    eu_agg['Code'] = 'EU16'
    eu_agg['Country'] = '유럽 16개국 합계 (Pan-Europe 16 Total)'
    eu_agg['Folder'] = '00. Europe 16 Total'
    eu_agg['Currency'] = 'USD'
    eu_agg['Sales Mix%'] = (eu_agg['Net Sales'] / ttl_sales * 100)
    eu_agg['COI%'] = (eu_agg['Operating Income (COI)'] / eu_agg['Net Sales'] * 100)
    eu_agg['MP%'] = (eu_agg['Marginal Profit (MP)'] / eu_agg['Net Sales'] * 100)
    eu_agg['ASP'] = (eu_agg['Net Sales'] / eu_agg['Qty'])
    
    # Combine
    df_full = pd.concat([eu_agg, df], ignore_index=True)
    
    # Create Excel Writer
    with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
        # Sheet 1: Pivot Mix & Margins
        pvt_mix = df.pivot(index=['Code', 'Country'], columns='Series', values='Sales Mix%')[['W', 'G', 'C', 'B', 'Total OLED']].round(1)
        pvt_coi = df.pivot(index=['Code', 'Country'], columns='Series', values='COI%')[['W', 'G', 'C', 'B', 'Total OLED']].round(1)
        pvt_mp = df.pivot(index=['Code', 'Country'], columns='Series', values='MP%')[['W', 'G', 'C', 'B', 'Total OLED']].round(1)
        
        # Combined Matrix
        matrix_rows = []
        for code in df_full['Code'].unique():
            sub = df_full[df_full['Code'] == code]
            cname = sub['Country'].iloc[0]
            curr = sub['Currency'].iloc[0]
            
            row_data = {'Code': code, '법인/지점명': cname, '통화': curr}
            for s in ['W', 'G', 'C', 'B', 'Total OLED']:
                s_row = sub[sub['Series'] == s]
                if len(s_row) > 0:
                    row_data[f'{s}_비중(%)'] = s_row['Sales Mix%'].values[0]
                    row_data[f'{s}_COI(%)'] = s_row['COI%'].values[0]
                    row_data[f'{s}_MP(%)'] = s_row['MP%'].values[0]
                    row_data[f'{s}_매출($)'] = s_row['Net Sales'].values[0]
                else:
                    row_data[f'{s}_비중(%)'] = 0.0
                    row_data[f'{s}_COI(%)'] = 0.0
                    row_data[f'{s}_MP(%)'] = 0.0
                    row_data[f'{s}_매출($)'] = 0.0
            matrix_rows.append(row_data)
            
        df_matrix = pd.DataFrame(matrix_rows)
        df_matrix.to_excel(writer, sheet_name='OLED_시리즈별_수익성_종합매트릭스', index=False)
        
        # Sheet 2: Pivots
        pvt_mix.reset_index().to_excel(writer, sheet_name='1.매출비중(Mix%)_Pivot', index=False)
        pvt_coi.reset_index().to_excel(writer, sheet_name='2.영업이익율(COI%)_Pivot', index=False)
        pvt_mp.reset_index().to_excel(writer, sheet_name='3.한계이익율(MP%)_Pivot', index=False)
        
        # Sheet 3: Full DB
        df_full.to_excel(writer, sheet_name='Raw_Summary_DB', index=False)
        
    print(f"Excel workbook created: {OUTPUT_EXCEL}")

if __name__ == '__main__':
    build_excel()
