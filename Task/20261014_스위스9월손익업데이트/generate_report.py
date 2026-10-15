# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json
import os
import re

excel_file = "★Swiss_ P&L Analysis_NERP_New_FROM 202301_TO_202609.xlsb"
template_file = "report_template.html"
output_file = "Swiss_TV_Profitability_Report.html"

print("Loading raw data from Excel (this may take 20-30 seconds)...")
df_raw = pd.read_excel(excel_file, sheet_name='Raw', engine='pyxlsb')
print(f"Raw data loaded. Shape: {df_raw.shape}")

# Rename columns to avoid encoding issues
col_mapping = {}
for col in df_raw.columns:
    if 'Qty(' in col:
        col_mapping[col] = 'Qty_Actual'
    elif 'Gross Sales(' in col:
        col_mapping[col] = 'GrossSales_Actual'
    elif 'Net Sales(' in col:
        col_mapping[col] = 'NetSales_Actual'

df_raw = df_raw.rename(columns=col_mapping)

# Identify Launch Year column at index 20
launch_year_col = df_raw.columns[20]
df_raw = df_raw.rename(columns={launch_year_col: 'Launch_Year'})

# Fill NaNs with 0 to prevent NaN propagation during row-wise addition
gap_cols = [
    'PL Gap', 'COGS Gap', 'COGS_Allowance for Return',
    'Variable PL Gap', 'Variable COGS Gap', 'Variable COGS_Allowance for Return'
]
for col in gap_cols:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].fillna(0)

df_raw['Total_Gap'] = df_raw['PL Gap'] + df_raw['COGS Gap'] - df_raw['COGS_Allowance for Return']
df_raw['Variable_Total_Gap'] = df_raw['Variable PL Gap'] + df_raw['Variable COGS Gap'] - df_raw['Variable COGS_Allowance for Return']

df_raw['COI_Fundamental'] = df_raw['Operating Income'] + df_raw['Total_Gap']
df_raw['MP_Fundamental'] = df_raw['Marginal Profit'] + df_raw['Variable_Total_Gap']

# Fill NaN values for rebate calculations
rebate_cols = ['Trade Term (Sell In)', 'Non Trade Term (Sell In)', 'Non Trade Term (Sell Out)']
for col in rebate_cols:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].fillna(0)

# Fill other required columns
other_fill_cols = [
    'Material Cost', 'Variable COGS', 'Variable SG&A', 'Fixed COGS', 'Fixed SG&A',
    'Variable Selling_Promotion', 'Variable Selling_Transportation', 
    'Variable Selling_Commission & Charge', 'Variable SVC',
    'Fixed Selling_Advertising', 'Fixed Selling_Commission & Charge', 'Fixed Selling_Labor',
    'Fixed Admin', 'Fixed R&D', 'Fixed SVC', 'Fixed Selling_Others'
]
for col in other_fill_cols:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].fillna(0)

# Auto-detect latest month
latest_year = int(df_raw['Year'].max())
latest_month = int(df_raw[df_raw['Year'] == latest_year]['Month'].max())
print(f"Latest Month detected: {latest_year}.{latest_month:02d}")

# Helper filters
def get_mtd_data(df, year, month):
    return df[(df['Year'] == year) & (df['Month'] == month)]

def get_ytd_data(df, year, max_month):
    return df[(df['Year'] == year) & (df['Month'] <= max_month)]

# Metric calculator (Original)
def calc_metrics(df_slice, is_fundamental=False):
    qty = float(df_slice['Qty_Actual'].sum())
    sales = float(df_slice['Net Sales'].sum())
    gross_sales = float(df_slice['GrossSales_Actual'].sum())
    net_sales_actual = float(df_slice['NetSales_Actual'].sum())
    cogs = float(df_slice['COGS'].sum())
    s_d = float(df_slice['Sales Deduction'].sum())
    sga = float(df_slice['SG&A'].sum())
    
    if is_fundamental:
        mp = float(df_slice['MP_Fundamental'].sum())
        coi = float(df_slice['COI_Fundamental'].sum())
    else:
        mp = float(df_slice['Marginal Profit'].sum())
        coi = float(df_slice['Operating Income'].sum())

    asp = net_sales_actual / qty if qty > 0 else 0
    mp_rate = mp / sales if sales > 0 else 0
    coi_rate = coi / sales if sales > 0 else 0
    sd_rate = abs(s_d) / gross_sales if gross_sales > 0 else 0
    cogs_rate = cogs / sales if sales > 0 else 0
    sga_rate = sga / sales if sales > 0 else 0
    
    # Rebate rates (Sales Deduction Detail)
    tt_val = float(df_slice['Trade Term (Sell In)'].sum())
    nttsi_val = float(df_slice['Non Trade Term (Sell In)'].sum())
    nttso_val = float(df_slice['Non Trade Term (Sell Out)'].sum())
    
    tt_rate = abs(tt_val) / gross_sales if gross_sales > 0 else 0
    nttsi_rate = abs(nttsi_val) / gross_sales if gross_sales > 0 else 0
    nttso_rate = abs(nttso_val) / gross_sales if gross_sales > 0 else 0

    return {
        'qty': qty,
        'sales': sales,
        'gross_sales': gross_sales,
        'asp': asp,
        'mp': mp_rate,
        'coi': coi_rate,
        'sd': sd_rate,
        'cogs': cogs_rate,
        'sga': sga_rate,
        'coi_val': coi,
        'mp_val': mp,
        'sd_val': s_d,
        'cogs_val': cogs,
        'sga_val': sga,
        'fixed_cogs': float(df_slice['Fixed COGS'].sum()),
        'fixed_sga': float(df_slice['Fixed SG&A'].sum()),
        'tt_rate': tt_rate,
        'nttsi_rate': nttsi_rate,
        'nttso_rate': nttso_rate
    }

# 1. Compute KPIs (Original)
def compute_kpis(df, year, month, is_fundamental=False):
    mtd_this = calc_metrics(get_mtd_data(df, year, month), is_fundamental)
    mtd_last = calc_metrics(get_mtd_data(df, year - 1, month), is_fundamental)
    ytd_this = calc_metrics(get_ytd_data(df, year, month), is_fundamental)
    ytd_last = calc_metrics(get_ytd_data(df, year - 1, month), is_fundamental)
    
    def make_yoy(val_this, val_last, is_rate=False):
        if is_rate:
            return val_this - val_last
        return (val_this - val_last) / val_last if val_last > 0 else None

    return {
        'mtd': {
            'qty': mtd_this['qty'], 'qty_yoy': make_yoy(mtd_this['qty'], mtd_last['qty']),
            'sales': mtd_this['sales'], 'sales_yoy': make_yoy(mtd_this['sales'], mtd_last['sales']),
            'asp': mtd_this['asp'], 'asp_yoy': make_yoy(mtd_this['asp'], mtd_last['asp']),
            'mp': mtd_this['mp'], 'mp_yoy': make_yoy(mtd_this['mp'], mtd_last['mp'], True),
            'coi': mtd_this['coi'], 'coi_yoy': make_yoy(mtd_this['coi'], mtd_last['coi'], True),
            'sd': mtd_this['sd'], 'sd_yoy': make_yoy(mtd_this['sd'], mtd_last['sd'], True)
        },
        'ytd': {
            'qty': ytd_this['qty'], 'qty_yoy': make_yoy(ytd_this['qty'], ytd_last['qty']),
            'sales': ytd_this['sales'], 'sales_yoy': make_yoy(ytd_this['sales'], ytd_last['sales']),
            'asp': ytd_this['asp'], 'asp_yoy': make_yoy(ytd_this['asp'], ytd_last['asp']),
            'mp': ytd_this['mp'], 'mp_yoy': make_yoy(ytd_this['mp'], ytd_last['mp'], True),
            'coi': ytd_this['coi'], 'coi_yoy': make_yoy(ytd_this['coi'], ytd_last['coi'], True),
            'sd': ytd_this['sd'], 'sd_yoy': make_yoy(ytd_this['sd'], ytd_last['sd'], True)
        }
    }

# 2. Compute Monthly Trend (Original)
def get_monthly_trend(df, latest_year, latest_month, is_fundamental=False):
    trend_list = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            metrics = calc_metrics(get_mtd_data(df, y, m), is_fundamental)
            trend_list.append({
                'year': y, 'month': m,
                'sales': metrics['sales'], 'mp': metrics['mp'], 'coi': metrics['coi'],
                'sd': metrics['sd'], 'tt': metrics['tt_rate'], 'nttsi': metrics['nttsi_rate'], 'nttso': metrics['nttso_rate']
            })
    return trend_list

# 3. YTD comparisons (Original)
def get_ytd_compare(df, max_month, is_fundamental=False):
    compare_list = []
    for y in [2023, 2024, 2025, 2026]:
        metrics = calc_metrics(get_ytd_data(df, y, max_month), is_fundamental)
        compare_list.append({
            'year': y, 'qty': metrics['qty'], 'sales': metrics['sales'],
            'mp': metrics['mp'], 'coi': metrics['coi'], 'sd': metrics['sd']
        })
    return compare_list

# 4. Waterfall YoY bridge (Original)
def get_waterfall(df, latest_year, max_month, is_fundamental=False):
    ytd_this = calc_metrics(get_ytd_data(df, latest_year, max_month), is_fundamental)
    ytd_last = calc_metrics(get_ytd_data(df, latest_year - 1, max_month), is_fundamental)
    
    qty_this = ytd_this['qty']
    qty_last = ytd_last['qty']
    
    coi_this = ytd_this['coi_val']
    coi_last = ytd_last['coi_val']
    
    volume_effect = (qty_this - qty_last) * (coi_last / qty_last if qty_last > 0 else 0)
    
    gross_asp_this = ytd_this['gross_sales'] / qty_this if qty_this > 0 else 0
    gross_asp_last = ytd_last['gross_sales'] / qty_last if qty_last > 0 else 0
    price_effect = qty_this * (gross_asp_this - gross_asp_last)
    
    sd_unit_this = ytd_this['sd_val'] / qty_this if qty_this > 0 else 0
    sd_unit_last = ytd_last['sd_val'] / qty_last if qty_last > 0 else 0
    sd_effect = qty_this * (sd_unit_this - sd_unit_last)
    
    var_cogs_this = float(get_ytd_data(df, latest_year, max_month)['Variable COGS'].sum())
    var_cogs_last = float(get_ytd_data(df, latest_year - 1, max_month)['Variable COGS'].sum())
    var_cogs_unit_this = var_cogs_this / qty_this if qty_this > 0 else 0
    var_cogs_unit_last = var_cogs_last / qty_last if qty_last > 0 else 0
    var_cogs_effect = -qty_this * (var_cogs_unit_this - var_cogs_unit_last)
    
    fixed_this = ytd_this['fixed_cogs'] + ytd_this['fixed_sga']
    fixed_last = ytd_last['fixed_cogs'] + ytd_last['fixed_sga']
    fixed_oh_effect = -(fixed_this - fixed_last)
    
    delta_coi = coi_this - coi_last
    explained = volume_effect + price_effect + sd_effect + var_cogs_effect + fixed_oh_effect
    other_gap_effect = delta_coi - explained
    
    return {
        'last_coi': coi_last, 'volume': volume_effect, 'price': price_effect,
        'sd': sd_effect, 'var_cogs': var_cogs_effect, 'fixed_oh': fixed_oh_effect,
        'other_gap': other_gap_effect, 'this_coi': coi_this
    }

# 5. BLU Mix Share (Original)
def get_blu_mix_detail(df, latest_year, max_month, is_fundamental=False):
    ytd_data = get_ytd_data(df, latest_year, max_month)
    ytd_last = get_ytd_data(df, latest_year - 1, max_month)
    
    total_metrics = calc_metrics(ytd_data, is_fundamental)
    total_qty = total_metrics['qty']
    total_sales = total_metrics['sales']
    
    blu_list = []
    for blu in ['OLED', 'QNED', 'MRGB', 'UHD', 'FHD']:
        blu_df = ytd_data[ytd_data['BLU'] == blu]
        blu_last_df = ytd_last[ytd_last['BLU'] == blu]
        
        m_blu = calc_metrics(blu_df, is_fundamental)
        m_blu_last = calc_metrics(blu_last_df, is_fundamental)
        
        qty = m_blu['qty']
        sales = m_blu['sales']
        
        blu_list.append({
            'blu': blu,
            'qty': qty,
            'qty_share': qty / total_qty if total_qty > 0 else 0,
            'sales': sales,
            'sales_share': sales / total_sales if total_sales > 0 else 0,
            'qty_yoy': (qty - m_blu_last['qty']) / m_blu_last['qty'] if m_blu_last['qty'] > 0 else None
        })
        
    model_groups = ytd_data.groupby('Model')
    model_list = []
    for model_name, group in model_groups:
        metrics = calc_metrics(group, is_fundamental)
        if metrics['qty'] <= 0: continue
        model_list.append({
            'model': model_name,
            'qty': metrics['qty'],
            'sales': metrics['sales'],
            'mp': metrics['mp'],
            'coi_val': metrics['coi_val'],
            'coi': metrics['coi']
        })
    model_list.sort(key=lambda x: x['sales'], reverse=True)
    top_models = model_list[:15]
    
    return {'blu_mix': blu_list, 'top_models': top_models}

# 6. Series Detail (Original)
def get_series_detail(df, latest_year, max_month, is_fundamental=False):
    ytd_data = get_ytd_data(df, latest_year, max_month)
    series_groups = ytd_data.groupby(['Launch_Year', 'Tool'])
    series_list = []
    
    for (ly, tool), group in series_groups:
        if ly not in ['Y26', 'Y25']: continue
        metrics = calc_metrics(group, is_fundamental)
        if metrics['qty'] <= 0: continue
        series_list.append({
            'launch_year': ly,
            'series': tool,
            'qty': metrics['qty'],
            'sales': metrics['sales'],
            'asp': metrics['asp'],
            'cogs': metrics['cogs'],
            'sga': metrics['sga'],
            'mp': metrics['mp'],
            'coi_val': metrics['coi_val'],
            'coi': metrics['coi'],
            'sd': metrics['sd']
        })
        
    series_list.sort(key=lambda x: (x['launch_year'], x['sales']), reverse=True)
    return series_list

# New model-level profitability data compilation
def get_model_detail_report(df, latest_year, latest_month, is_ytd=False, is_fundamental=False):
    if is_ytd:
        df_slice = get_ytd_data(df, latest_year, latest_month)
    else:
        df_slice = get_mtd_data(df, latest_year, latest_month)
        
    df_filtered = df_slice[df_slice['Launch_Year'].isin(['Y26', 'Y25'])]
    df_filtered = df_filtered.dropna(subset=['Model'])
    
    model_groups = df_filtered.groupby(['Launch_Year', 'BLU', 'Model'])
    model_list = []
    
    for (ly, blu, model_name), group in model_groups:
        metrics = calc_metrics(group, is_fundamental)
        if metrics['qty'] <= 0:
            continue
        model_list.append({
            'launch_year': ly,
            'segment': blu,
            'model': model_name,
            'qty': metrics['qty'],
            'asp': metrics['asp'],
            'gross_sales': metrics['gross_sales'],
            'net_sales': metrics['sales'],
            'cogs_rate': metrics['cogs'],
            'sga_rate': metrics['sga'],
            'mp_rate': metrics['mp'],
            'coi_val': metrics['coi_val'],
            'coi_rate': metrics['coi'],
            'row_type': 'detail'
        })
        
    model_list.sort(key=lambda x: x['net_sales'], reverse=True)
    return model_list[:30]

def parse_series_pivot(df, is_ytd=False):
    cols = list(range(14)) if not is_ytd else list(range(23, 37))
    df_part = df.iloc[:, cols]
    
    headers = [str(x).strip() for x in df_part.iloc[4]]
    df_clean = df_part.iloc[5:].copy()
    df_clean.columns = headers
    
    launch_year_col = headers[0]
    segment_col = headers[1]
    tool_col = headers[2]
    
    df_clean['Launch_Year_Filled'] = df_clean[launch_year_col].ffill()
    df_clean['OLED_UHD_Filled'] = df_clean[segment_col].ffill()
    
    parsed_rows = []
    for idx, row in df_clean.iterrows():
        ly_filled = row['Launch_Year_Filled']
        ly_orig = row[launch_year_col]
        
        if pd.isna(ly_filled):
            continue
            
        ly_filled_str = str(ly_filled).strip()
        
        if not (ly_filled_str.startswith('Y26') or ly_filled_str.startswith('Y25')):
            continue
            
        is_summary = False
        row_type = 'detail'
        
        ly_orig_str = str(ly_orig) if pd.notna(ly_orig) else ''
        if pd.notna(ly_orig) and any(x in ly_orig_str for x in ['요약', 'summary', 'Ұ', '요', '약']):
            is_summary = True
            row_type = 'summary'
            launch_year = ly_orig_str.replace(' 요약', '').replace('요약', '').strip()
            segment = ''
            tool = '요약'
        else:
            launch_year = ly_filled_str
            segment = row['OLED_UHD_Filled']
            tool = row[tool_col]
            if pd.isna(tool):
                orig_seg = row[segment_col]
                orig_seg_str = str(orig_seg) if pd.notna(orig_seg) else ''
                if pd.notna(orig_seg) and any(x in orig_seg_str for x in ['요약', 'Ұ', '요', '약']):
                    tool = orig_seg_str.replace(' 요약', '').replace('요약', '').strip() + ' 소계'
                    row_type = 'segment_summary'
                else:
                    continue
        
        qty = row['Sales Qty(제상품)']
        asp = row['N.ASP($)']
        gross_sales = row['합계 : Gross Sales']
        net_sales = row['Net Sales(제상품)'] if not is_ytd else row['합계 : Net Sales']
        cogs_rate = row['COGS(%)']
        sga_rate = row['SG&A(%)']
        mp = row['MP']
        mp_rate = row['MP(%)']
        coi = row['COI']
        coi_rate = row['COI(%)']
        
        def clean_val(v):
            try:
                v_f = float(v)
                if pd.isna(v_f) or v_f == float('inf') or v_f == float('-inf'):
                    return 0.0
                return v_f
            except:
                return 0.0

        parsed_rows.append({
            'launch_year': launch_year,
            'segment': '' if pd.isna(segment) else str(segment).strip(),
            'tool': '' if pd.isna(tool) else str(tool).strip(),
            'qty': clean_val(qty),
            'asp': clean_val(asp),
            'gross_sales': clean_val(gross_sales),
            'net_sales': clean_val(net_sales),
            'cogs_rate': clean_val(cogs_rate),
            'sga_rate': clean_val(sga_rate),
            'mp': clean_val(mp),
            'mp_rate': clean_val(mp_rate),
            'coi': clean_val(coi),
            'coi_rate': clean_val(coi_rate),
            'row_type': row_type
        })
        
    return parsed_rows

# 7. Account Performance (Original)
def get_account_detail(df, latest_year, max_month, is_ytd=True, is_fundamental=False):
    if is_ytd:
        df_slice = get_ytd_data(df, latest_year, max_month)
    else:
        df_slice = get_mtd_data(df, latest_year, max_month)
        
    total_metrics = calc_metrics(df_slice, is_fundamental)
    total_sales = total_metrics['sales']
    
    channels = df_slice['ACCOUNT_NAME'].unique().tolist()
    channel_list = []
    
    for ch in channels:
        if pd.isna(ch): continue
        ch_df = df_slice[df_slice['ACCOUNT_NAME'] == ch]
        m_ch = calc_metrics(ch_df, is_fundamental)
        
        if m_ch['sales'] <= 0: continue
        
        channel_list.append({
            'channel': ch.replace('CH_', ''),
            'sales': m_ch['sales'],
            'sales_share': m_ch['sales'] / total_sales if total_sales > 0 else 0,
            'qty': m_ch['qty'],
            'asp': m_ch['asp'],
            'sd': m_ch['sd'],
            'mp': m_ch['mp'],
            'coi': m_ch['coi']
        })
        
    channel_list.sort(key=lambda x: x['sales'], reverse=True)
    return channel_list

# 8. P&L detail monthly (Original)
def get_pnl_detail_monthly(df, latest_year, latest_month, is_fundamental=False):
    pnl_records = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            metrics = calc_metrics(get_mtd_data(df, y, m), is_fundamental)
            pnl_records.append({
                'year': y, 'month': m,
                'qty': metrics['qty'],
                'gross_sales': metrics['gross_sales'],
                'sales': metrics['sales'],
                'sd_val': metrics['sd_val'],
                'sd_rate': metrics['sd'],
                'asp': metrics['asp'],
                'cogs_val': metrics['cogs_val'],
                'cogs_rate': metrics['cogs'],
                'mp_val': metrics['mp_val'],
                'mp_rate': metrics['mp'],
                'sga_val': metrics['sga_val'],
                'sga_rate': metrics['sga'],
                'coi_val': metrics['coi_val'],
                'coi_rate': metrics['coi']
            })
    return pnl_records

# 9. Current Month P&L (Original)
def get_current_month_pnl(df, latest_year, latest_month, is_fundamental=False):
    this_mtd = calc_metrics(get_mtd_data(df, latest_year, latest_month), is_fundamental)
    last_mtd = calc_metrics(get_mtd_data(df, latest_year - 1, latest_month), is_fundamental)
    
    keys = ['qty', 'gross_sales', 'sd_val', 'sales', 'cogs_val', 'mp_val', 'sga_val', 'coi_val']
    labels = {
        'qty': '판매량 (Units)',
        'gross_sales': 'Gross Sales (K$)',
        'sd_val': 'Sales Deduction (K$)',
        'sales': 'Net Sales (K$)',
        'cogs_val': 'COGS (K$)',
        'mp_val': 'Marginal Profit (K$)',
        'sga_val': 'SG&A (K$)',
        'coi_val': 'Operating Income (K$)'
    }
    
    rows = []
    for k in keys:
        v_this = this_mtd[k]
        v_last = last_mtd[k]
        diff = v_this - v_last
        yoy = diff / abs(v_last) if v_last != 0 else None
        rows.append({
            'item': labels[k],
            'this_val': v_this,
            'last_val': v_last,
            'diff': diff,
            'yoy': yoy
        })
        
    rates = ['sd', 'mp', 'coi']
    rate_labels = {
        'sd': 'S/D Ratio (%)',
        'mp': 'MP Ratio (%)',
        'coi': 'COI Ratio (%)'
    }
    for r in rates:
        v_this = this_mtd[r]
        v_last = last_mtd[r]
        diff = v_this - v_last
        rows.append({
            'item': rate_labels[r],
            'this_val': v_this,
            'last_val': v_last,
            'diff': None,
            'yoy': diff
        })
        
    return rows


# ==========================================
# New S1-S6 P&L Structure calculations
# ==========================================

def calc_pnl_structure(df_slice):
    qty = float(df_slice['Qty_Actual'].sum())
    gross_sales = float(df_slice['GrossSales_Actual'].sum())
    sd_val = float(df_slice['Sales Deduction'].sum())
    net_sales = float(df_slice['Net Sales'].sum())
    net_sales_actual = float(df_slice['NetSales_Actual'].sum())
    
    # Cost items
    material_cost = float(df_slice['Material Cost'].sum())
    var_cogs = float(df_slice['Variable COGS'].sum())
    var_oh = var_cogs - material_cost
    
    # Variable SG&A components
    promotion = float(df_slice['Variable Selling_Promotion'].sum())
    transport = float(df_slice['Variable Selling_Transportation'].sum())
    commission_var = float(df_slice['Variable Selling_Commission & Charge'].sum())
    svc_var = float(df_slice['Variable SVC'].sum())
    
    var_sga = float(df_slice['Variable SG&A'].sum())
    others_var = var_sga - (promotion + transport + commission_var + svc_var)
    
    # MP = Net Sales - Variable Cost
    mp_val = net_sales - (var_cogs + var_sga)
    
    # Fixed overheads
    fixed_adv = float(df_slice['Fixed Selling_Advertising'].sum())
    fixed_comm = float(df_slice['Fixed Selling_Commission & Charge'].sum())
    fixed_labor = float(df_slice['Fixed Selling_Labor'].sum())
    fixed_admin = float(df_slice['Fixed Admin'].sum())
    fixed_rd = float(df_slice['Fixed R&D'].sum())
    fixed_svc = float(df_slice['Fixed SVC'].sum())
    
    fixed_oh_total = float(df_slice['Fixed COGS'].sum()) + float(df_slice['Fixed SG&A'].sum())
    others_fixed = fixed_oh_total - (fixed_adv + fixed_comm + fixed_labor + fixed_admin + fixed_rd + fixed_svc)
    
    # COI
    coi_val = mp_val - fixed_oh_total
    
    asp = net_sales_actual / qty if qty > 0 else 0
    mp_rate = mp_val / net_sales if net_sales > 0 else 0
    coi_rate = coi_val / net_sales if net_sales > 0 else 0
    sd_rate = abs(sd_val) / gross_sales if gross_sales > 0 else 0
    
    mat_rate = material_cost / net_sales if net_sales > 0 else 0
    var_oh_rate = var_oh / net_sales if net_sales > 0 else 0
    promo_rate = promotion / net_sales if net_sales > 0 else 0
    trans_rate = transport / net_sales if net_sales > 0 else 0
    comm_var_rate = commission_var / net_sales if net_sales > 0 else 0
    svc_var_rate = svc_var / net_sales if net_sales > 0 else 0
    others_var_rate = others_var / net_sales if net_sales > 0 else 0
    
    fixed_cogs_rate = float(df_slice['Fixed COGS'].sum()) / net_sales if net_sales > 0 else 0
    fixed_sga_rate = float(df_slice['Fixed SG&A'].sum()) / net_sales if net_sales > 0 else 0
    
    return {
        'qty': qty, 'gross_sales': gross_sales, 'sd_val': sd_val, 'net_sales': net_sales, 'asp': asp,
        'mp_val': mp_val, 'coi_val': coi_val, 'mp_rate': mp_rate, 'coi_rate': coi_rate, 'sd_rate': sd_rate,
        'material_cost': material_cost, 'var_oh': var_oh, 'promotion': promotion, 'transport': transport,
        'commission_var': commission_var, 'svc_var': svc_var, 'others_var': others_var,
        'fixed_adv': fixed_adv, 'fixed_comm': fixed_comm, 'fixed_labor': fixed_labor,
        'fixed_admin': fixed_admin, 'fixed_rd': fixed_rd, 'fixed_svc': fixed_svc, 'others_fixed': others_fixed,
        'fixed_oh_total': fixed_oh_total, 'mat_rate': mat_rate, 'var_oh_rate': var_oh_rate,
        'promo_rate': promo_rate, 'trans_rate': trans_rate, 'comm_var_rate': comm_var_rate,
        'svc_var_rate': svc_var_rate, 'others_var_rate': others_var_rate,
        'fixed_cogs_rate': fixed_cogs_rate, 'fixed_sga_rate': fixed_sga_rate
    }

def get_kpis_pnl_structure(df, year, month):
    mtd_this = calc_pnl_structure(get_mtd_data(df, year, month))
    mtd_last = calc_pnl_structure(get_mtd_data(df, year - 1, month))
    ytd_this = calc_pnl_structure(get_ytd_data(df, year, month))
    ytd_last = calc_pnl_structure(get_ytd_data(df, year - 1, month))
    
    def diff_val(this_v, last_v):
        return this_v - last_v
    def yoy_pct(this_v, last_v):
        return (this_v - last_v) / last_v if last_v != 0 else 0
        
    return {
        'qty': {'mtd': mtd_this['qty'], 'ytd': ytd_this['qty'], 'yoy_mtd': yoy_pct(mtd_this['qty'], mtd_last['qty']), 'yoy_ytd': yoy_pct(ytd_this['qty'], ytd_last['qty'])},
        'sales': {'mtd': mtd_this['net_sales'], 'ytd': ytd_this['net_sales'], 'yoy_mtd': yoy_pct(mtd_this['net_sales'], mtd_last['net_sales']), 'yoy_ytd': yoy_pct(ytd_this['net_sales'], ytd_last['net_sales'])},
        'asp': {'mtd': mtd_this['asp'], 'ytd': ytd_this['asp'], 'yoy_mtd': yoy_pct(mtd_this['asp'], mtd_last['asp']), 'yoy_ytd': yoy_pct(ytd_this['asp'], ytd_last['asp'])},
        'mp': {'mtd': mtd_this['mp_rate'], 'ytd': ytd_this['mp_rate'], 'yoy_mtd': diff_val(mtd_this['mp_rate'], mtd_last['mp_rate']), 'yoy_ytd': diff_val(ytd_this['mp_rate'], ytd_last['mp_rate'])},
        'coi': {'mtd': mtd_this['coi_rate'], 'ytd': ytd_this['coi_rate'], 'yoy_mtd': diff_val(mtd_this['coi_rate'], mtd_last['coi_rate']), 'yoy_ytd': diff_val(ytd_this['coi_rate'], ytd_last['coi_rate'])},
        'sd': {'mtd': mtd_this['sd_rate'], 'ytd': ytd_this['sd_rate'], 'yoy_mtd': diff_val(mtd_this['sd_rate'], mtd_last['sd_rate']), 'yoy_ytd': diff_val(ytd_this['sd_rate'], ytd_last['sd_rate'])}
    }

def get_monthly_trend_new(df, latest_year, latest_month):
    trend_list = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            res = calc_pnl_structure(get_mtd_data(df, y, m))
            has_adjust = False
            adjust_msg = ""
            if y == 2025 and m == 6:
                has_adjust = True
                adjust_msg = "'25.6월 반품충당금 환입액이 대거 반영되어 일시적으로 COI가 과대 계상됨."
            elif y == 2025 and m == 11:
                has_adjust = True
                adjust_msg = "'25.11월 변동O/H 환입(약 $350K) 반영되어 실질 수익성이 높게 나타남."
            elif y == 2026 and m == 1:
                has_adjust = True
                adjust_msg = "2026년 신모델 출시 전 구모델(Y25) 클리어런스 판촉 강화로 S/D%가 일시 상승함."
                
            trend_list.append({
                'year': y, 'month': m,
                'month_str': f"{str(y)[2:]}.{m:02d}",
                'sales': res['net_sales'],
                'coi_val': res['coi_val'],
                'mp_rate': res['mp_rate'],
                'coi_rate': res['coi_rate'],
                'is_loss': res['coi_val'] < 0,
                'has_adjust': has_adjust,
                'adjust_msg': adjust_msg
            })
    return trend_list

def get_waterfall_new(df, latest_year, latest_month):
    mtd_this = calc_pnl_structure(get_mtd_data(df, latest_year, latest_month))
    ytd_this = calc_pnl_structure(get_ytd_data(df, latest_year, latest_month))
    
    def make_steps(res):
        return [
            {'label': 'Net Sales', 'val': res['net_sales'], 'rate': 1.0, 'type': 'total'},
            {'label': '재료비', 'val': -res['material_cost'], 'rate': -res['mat_rate'], 'type': 'cost'},
            {'label': '변동O/H', 'val': -res['var_oh'], 'rate': -res['var_oh_rate'], 'type': 'cost'},
            {'label': '판촉비', 'val': -res['promotion'], 'rate': -res['promo_rate'], 'type': 'cost'},
            {'label': '물류비', 'val': -res['transport'], 'rate': -res['trans_rate'], 'type': 'cost'},
            {'label': '지급수수료', 'val': -res['commission_var'], 'rate': -res['comm_var_rate'], 'type': 'cost'},
            {'label': 'SVC비', 'val': -res['svc_var'], 'rate': -res['svc_var_rate'], 'type': 'cost'},
            {'label': '기타 변동비', 'val': -res['others_var'], 'rate': -res['others_var_rate'], 'type': 'cost'},
            {'label': 'MP', 'val': res['mp_val'], 'rate': res['mp_rate'], 'type': 'subtotal'},
            {'label': '광고비', 'val': -res['fixed_adv'], 'rate': -(res['fixed_adv']/res['net_sales']), 'type': 'cost'},
            {'label': '지급수수료(고정)', 'val': -res['fixed_comm'], 'rate': -(res['fixed_comm']/res['net_sales']), 'type': 'cost'},
            {'label': '인건비', 'val': -res['fixed_labor'], 'rate': -(res['fixed_labor']/res['net_sales']), 'type': 'cost'},
            {'label': '관리비', 'val': -res['fixed_admin'], 'rate': -(res['fixed_admin']/res['net_sales']), 'type': 'cost'},
            {'label': 'R&D', 'val': -res['fixed_rd'], 'rate': -(res['fixed_rd']/res['net_sales']), 'type': 'cost'},
            {'label': 'SVC(고정)', 'val': -res['fixed_svc'], 'rate': -(res['fixed_svc']/res['net_sales']), 'type': 'cost'},
            {'label': '기타 고정비', 'val': -res['others_fixed'], 'rate': -(res['others_fixed']/res['net_sales']), 'type': 'cost'},
            {'label': 'COI', 'val': res['coi_val'], 'rate': res['coi_rate'], 'type': 'total'}
        ]
        
    return {
        'mtd': make_steps(mtd_this),
        'ytd': make_steps(ytd_this)
    }

def get_cost_structure_stack_new(df, latest_year, latest_month):
    ytd_compare = []
    for y in [2023, 2024, 2025, 2026]:
        res = calc_pnl_structure(get_ytd_data(df, y, latest_month))
        var_sga_rate = res['promo_rate'] + res['trans_rate'] + res['comm_var_rate'] + res['svc_var_rate'] + res['others_var_rate']
        mp_residual_rate = res['mp_rate'] - res['fixed_cogs_rate']
        
        ytd_compare.append({
            'label': f"{y} YTD",
            'material': res['mat_rate'],
            'var_oh': res['var_oh_rate'],
            'var_sga': var_sga_rate,
            'fixed_cogs': res['fixed_cogs_rate'],
            'mp_residual': mp_residual_rate
        })
        
    monthly_stack = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            res = calc_pnl_structure(get_mtd_data(df, y, m))
            var_sga_rate = res['promo_rate'] + res['trans_rate'] + res['comm_var_rate'] + res['svc_var_rate'] + res['others_var_rate']
            mp_residual_rate = res['mp_rate'] - res['fixed_cogs_rate']
            
            monthly_stack.append({
                'label': f"{str(y)[2:]}.{m:02d}",
                'material': res['mat_rate'],
                'var_oh': res['var_oh_rate'],
                'var_sga': var_sga_rate,
                'fixed_cogs': res['fixed_cogs_rate'],
                'mp_residual': mp_residual_rate
            })
            
    return {
        'ytd_compare': ytd_compare,
        'monthly_stack': monthly_stack
    }

def get_heatmap_data_new(df, latest_year, latest_month):
    months = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            res = calc_pnl_structure(get_mtd_data(df, y, m))
            var_sga_rate = res['promo_rate'] + res['trans_rate'] + res['comm_var_rate'] + res['svc_var_rate'] + res['others_var_rate']
            pivot_var_oh_rate = res['var_oh_rate'] + var_sga_rate
            months.append({
                'month_str': f"{str(y)[2:]}.{m:02d}",
                'var_oh': pivot_var_oh_rate,
                'promotion': res['promo_rate'],
                'transport': res['trans_rate'],
                'commission': res['comm_var_rate'],
                'svc': res['svc_var_rate']
            })
    return months

def get_fixed_oh_compare_new(df, latest_year, latest_month):
    y25 = calc_pnl_structure(get_ytd_data(df, 2025, latest_month))
    y26 = calc_pnl_structure(get_ytd_data(df, 2026, latest_month))
    
    items = [
        {'key': 'fixed_adv', 'label': '광고비'},
        {'key': 'fixed_comm', 'label': '지급수수료'},
        {'key': 'fixed_labor', 'label': '인건비'},
        {'key': 'fixed_admin', 'label': '관리비'},
        {'key': 'fixed_rd', 'label': 'R&D'},
        {'key': 'fixed_svc', 'label': 'SVC'},
        {'key': 'others_fixed', 'label': '기타 고정비'}
    ]
    
    compare_rows = []
    for it in items:
        v25 = y25[it['key']]
        v26 = y26[it['key']]
        diff = v26 - v25
        yoy = diff / v25 if v25 != 0 else 0
        compare_rows.append({
            'item': it['label'],
            'val_2025': v25,
            'val_2026': v26,
            'diff': diff,
            'yoy': yoy
        })
        
    return {
        'rows': compare_rows,
        'y25_total': y25['fixed_oh_total'],
        'y26_total': y26['fixed_oh_total']
    }

def get_ytd_trend_chart_data(df, latest_year, latest_month, is_fundamental=False):
    data = []
    calc_func = calc_fundamental_pnl_structure if is_fundamental else calc_pnl_structure
    
    # 1. 2023 YTD ~ 2026 YTD (latest_month cumulative)
    for y in [2023, 2024, 2025, 2026]:
        res = calc_func(get_ytd_data(df, y, latest_month))
        data.append({
            'year': y,
            'month_str': f"{y} YTD",
            'sales': res['net_sales'],
            'mp_rate': res['mp_fundamental_rate'] if is_fundamental else res['mp_rate'],
            'coi_rate': res['coi_fundamental_rate'] if is_fundamental else res['coi_rate'],
            'is_loss': (res['coi_fundamental'] < 0) if is_fundamental else (res['coi_val'] < 0),
            'is_spacer': False
        })
        
    # 2. Spacer Segment
    data.append({
        'year': None,
        'month_str': '',
        'sales': None,
        'mp_rate': None,
        'coi_rate': None,
        'is_loss': False,
        'is_spacer': True
    })
    
    # 3. 2026.01 YTD ~ 2026.latest_month YTD
    for m in range(1, latest_month + 1):
        res = calc_func(get_ytd_data(df, latest_year, m))
        data.append({
            'year': latest_year,
            'month_str': f"{m:02d}월 누적" if m == 1 else f"{m:02d}월 누계" if m == latest_month else f"{m:02d}월 누적",
            'sales': res['net_sales'],
            'mp_rate': res['mp_fundamental_rate'] if is_fundamental else res['mp_rate'],
            'coi_rate': res['coi_fundamental_rate'] if is_fundamental else res['coi_rate'],
            'is_loss': (res['coi_fundamental'] < 0) if is_fundamental else (res['coi_val'] < 0),
            'is_spacer': False
        })
        
    return data


# ==========================================
# New S3-S4 Fundamental Structure calculations
# ==========================================

def calc_fundamental_pnl_structure(df_slice):
    std = calc_pnl_structure(df_slice)
    
    pl_gap = float(df_slice['PL Gap'].sum())
    cogs_gap = float(df_slice['COGS Gap'].sum())
    cogs_allowance = float(df_slice['COGS_Allowance for Return'].sum())
    total_gap = pl_gap + cogs_gap - cogs_allowance
    
    var_pl_gap = float(df_slice['Variable PL Gap'].sum()) if 'Variable PL Gap' in df_slice.columns else 0
    var_cogs_gap = float(df_slice['Variable COGS Gap'].sum()) if 'Variable COGS Gap' in df_slice.columns else 0
    var_cogs_allowance = float(df_slice['Variable COGS_Allowance for Return'].sum()) if 'Variable COGS_Allowance for Return' in df_slice.columns else 0
    var_total_gap = var_pl_gap + var_cogs_gap - var_cogs_allowance
    
    mp_fundamental = std['mp_val'] + var_total_gap
    coi_fundamental = std['coi_val'] + total_gap
    
    mp_fundamental_rate = mp_fundamental / std['net_sales'] if std['net_sales'] > 0 else 0
    coi_fundamental_rate = coi_fundamental / std['net_sales'] if std['net_sales'] > 0 else 0
    
    return {
        **std,
        'pl_gap': pl_gap,
        'cogs_gap': cogs_gap,
        'cogs_allowance': cogs_allowance,
        'total_gap': total_gap,
        'var_pl_gap': var_pl_gap,
        'var_cogs_gap': var_cogs_gap,
        'var_cogs_allowance': var_cogs_allowance,
        'var_total_gap': var_total_gap,
        'mp_fundamental': mp_fundamental,
        'coi_fundamental': coi_fundamental,
        'mp_fundamental_rate': mp_fundamental_rate,
        'coi_fundamental_rate': coi_fundamental_rate
    }

def get_monthly_trend_fundamental(df, latest_year, latest_month):
    trend_list = []
    for y in [2025, 2026]:
        max_m = latest_month if y == latest_year else 12
        for m in range(1, max_m + 1):
            res = calc_fundamental_pnl_structure(get_mtd_data(df, y, m))
            trend_list.append({
                'year': y, 'month': m,
                'month_str': f"{str(y)[2:]}.{m:02d}",
                'sales': res['net_sales'],
                'coi_val': res['coi_fundamental'],
                'mp_rate': res['mp_fundamental_rate'],
                'coi_rate': res['coi_fundamental_rate'],
                'is_loss': res['coi_fundamental'] < 0
            })
    return trend_list

def get_waterfall_fundamental(df, latest_year, latest_month):
    mtd_this = calc_fundamental_pnl_structure(get_mtd_data(df, latest_year, latest_month))
    ytd_this = calc_fundamental_pnl_structure(get_ytd_data(df, latest_year, latest_month))
    
    def make_steps(res):
        return [
            {'label': 'Net Sales', 'val': res['net_sales'], 'rate': 1.0, 'type': 'total'},
            {'label': '재료비', 'val': -res['material_cost'], 'rate': -res['mat_rate'], 'type': 'cost'},
            {'label': '변동O/H', 'val': -res['var_oh'], 'rate': -res['var_oh_rate'], 'type': 'cost'},
            {'label': '판촉비', 'val': -res['promotion'], 'rate': -res['promo_rate'], 'type': 'cost'},
            {'label': '물류비', 'val': -res['transport'], 'rate': -res['trans_rate'], 'type': 'cost'},
            {'label': '지급수수료', 'val': -res['commission_var'], 'rate': -res['comm_var_rate'], 'type': 'cost'},
            {'label': 'SVC비', 'val': -res['svc_var'], 'rate': -res['svc_var_rate'], 'type': 'cost'},
            {'label': '기타 변동비', 'val': -res['others_var'], 'rate': -res['others_var_rate'], 'type': 'cost'},
            {'label': 'MP (Standard)', 'val': res['mp_val'], 'rate': res['mp_rate'], 'type': 'subtotal'},
            {'label': '광고비', 'val': -res['fixed_adv'], 'rate': -(res['fixed_adv']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': '지급수수료(고정)', 'val': -res['fixed_comm'], 'rate': -(res['fixed_comm']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': '인건비', 'val': -res['fixed_labor'], 'rate': -(res['fixed_labor']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': '관리비', 'val': -res['fixed_admin'], 'rate': -(res['fixed_admin']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': 'R&D', 'val': -res['fixed_rd'], 'rate': -(res['fixed_rd']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': 'SVC(고정)', 'val': -res['fixed_svc'], 'rate': -(res['fixed_svc']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': '기타 고정비', 'val': -res['others_fixed'], 'rate': -(res['others_fixed']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': 'COI (Standard)', 'val': res['coi_val'], 'rate': res['coi_rate'], 'type': 'subtotal'},
            {'label': 'PL Gap', 'val': res['pl_gap'], 'rate': (res['pl_gap']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost' if res['pl_gap'] < 0 else 'effect'},
            {'label': 'COGS Gap', 'val': res['cogs_gap'], 'rate': (res['cogs_gap']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost' if res['cogs_gap'] < 0 else 'effect'},
            {'label': 'COGS Allowance', 'val': -res['cogs_allowance'], 'rate': -(res['cogs_allowance']/res['net_sales']) if res['net_sales'] > 0 else 0, 'type': 'cost'},
            {'label': 'COI (Fundamental)', 'val': res['coi_fundamental'], 'rate': res['coi_fundamental_rate'], 'type': 'total'}
        ]
        
    return {
        'mtd': make_steps(mtd_this),
        'ytd': make_steps(ytd_this)
    }


# ==========================================
# New BLU Profitability Dashboard Data Engine
# ==========================================

def get_blu_dashboard_data(df, latest_year, latest_month):
    large_col = df.columns[17] # 'ʴ(OLED)'
    
    # helper for slice metrics
    def calc_blu_metrics(df_slice):
        qty = float(df_slice['Qty_Actual'].sum())
        sales = float(df_slice['Net Sales'].sum())
        coi = float(df_slice['Operating Income'].sum())
        mp = float(df_slice['Marginal Profit'].sum())
        fixed_oh = float(df_slice['Fixed COGS'].sum()) + float(df_slice['Fixed SG&A'].sum())
        
        net_sales_actual = float(df_slice['NetSales_Actual'].sum())
        asp = net_sales_actual / qty if qty > 0 else 0
        
        gross_sales = float(df_slice['GrossSales_Actual'].sum())
        sd_val = float(df_slice['Sales Deduction'].sum())
        sd_rate = abs(sd_val) / gross_sales if gross_sales > 0 else 0
        
        mp_rate = mp / sales if sales > 0 else 0
        coi_rate = coi / sales if sales > 0 else 0
        fixed_rate = fixed_oh / sales if sales > 0 else 0
        bep_sales = fixed_oh / mp_rate if mp_rate > 0 else 0
        
        return {
            'qty': qty, 'sales': sales, 'coi': coi, 'mp': mp,
            'mp_rate': mp_rate, 'coi_rate': coi_rate, 'fixed_rate': fixed_rate, 'bep_sales': bep_sales,
            'fixed_oh': fixed_oh, 'asp': asp, 'sd': sd_rate
        }
        
    # Standard P&L Slice helpers
    mtd_this = df[(df['Year'] == latest_year) & (df['Month'] == latest_month)]
    mtd_last = df[(df['Year'] == latest_year - 1) & (df['Month'] == latest_month)]
    ytd_this = df[(df['Year'] == latest_year) & (df['Month'] <= latest_month)]
    ytd_last = df[(df['Year'] == latest_year - 1) & (df['Month'] <= latest_month)]
    
    m_mtd_this = calc_blu_metrics(mtd_this)
    m_mtd_last = calc_blu_metrics(mtd_last)
    m_ytd_this = calc_blu_metrics(ytd_this)
    m_ytd_last = calc_blu_metrics(ytd_last)
    
    # S1 KPIs
    def make_kpi_row(key, m_this, m_last, is_rate=False):
        val_this = m_this[key]
        val_last = m_last[key]
        if is_rate:
            diff = val_this - val_last
            yoy = diff
        else:
            diff = val_this - val_last
            yoy = diff / val_last if val_last != 0 else 0
        return {'val': val_this, 'diff': diff, 'yoy': yoy}
        
    s1_data = {
        'mtd': {
            'qty': make_kpi_row('qty', m_mtd_this, m_mtd_last),
            'sales': make_kpi_row('sales', m_mtd_this, m_mtd_last),
            'asp': make_kpi_row('asp', m_mtd_this, m_mtd_last),
            'mp': make_kpi_row('mp_rate', m_mtd_this, m_mtd_last, True),
            'coi': make_kpi_row('coi_rate', m_mtd_this, m_mtd_last, True),
            'sd': make_kpi_row('sd', m_mtd_this, m_mtd_last, True),
            'bep': make_kpi_row('bep_sales', m_mtd_this, m_mtd_last),
            'fixed': make_kpi_row('fixed_rate', m_mtd_this, m_mtd_last, True)
        },
        'ytd': {
            'qty': make_kpi_row('qty', m_ytd_this, m_ytd_last),
            'sales': make_kpi_row('sales', m_ytd_this, m_ytd_last),
            'asp': make_kpi_row('asp', m_ytd_this, m_ytd_last),
            'mp': make_kpi_row('mp_rate', m_ytd_this, m_ytd_last, True),
            'coi': make_kpi_row('coi_rate', m_ytd_this, m_ytd_last, True),
            'sd': make_kpi_row('sd', m_ytd_this, m_ytd_last, True),
            'bep': make_kpi_row('bep_sales', m_ytd_this, m_ytd_last),
            'fixed': make_kpi_row('fixed_rate', m_ytd_this, m_ytd_last, True)
        }
    }
    
    # BLU categorizers
    blu_conds = {
        'OLED': lambda s: s['OLED/UHD'] == 'OLED',
        'QNED': lambda s: s['QNED'] == 'QNED',
        'MRGB': lambda s: s['QNED'] == 'MRGB',
        'UHD': lambda s: (s['OLED/UHD'] == 'UHD') & (s['QNED'] != 'QNED') & (s['QNED'] != 'MRGB'),
        'FHD': lambda s: s['OLED/UHD'] == 'FHD',
        'Others': lambda s: s['OLED/UHD'] == 'Others'
    }
    
    # S2 & S3 & S4 & S6 data YTD
    s2_data = {'ytd': {}, 'mtd': {}}
    s3_data_ytd = []
    s3_data_mtd = []
    s4_data = []
    s6_data = []
    tie_out_data = []
    
    tot_ytd_sales = m_ytd_this['sales']
    tot_mtd_sales = m_mtd_this['sales']
    
    ex_others_sales_ytd = 0
    ex_others_coi_ytd = 0
    ex_others_sales_mtd = 0
    ex_others_coi_mtd = 0
    
    for name, cond_func in blu_conds.items():
        df_blu_ytd = ytd_this[cond_func(ytd_this)]
        df_blu_mtd = mtd_this[cond_func(mtd_this)]
        
        m_blu_ytd = calc_blu_metrics(df_blu_ytd)
        m_blu_mtd = calc_blu_metrics(df_blu_mtd)
        
        s2_data['ytd'][name] = m_blu_ytd['sales'] / tot_ytd_sales if tot_ytd_sales > 0 else 0
        s2_data['mtd'][name] = m_blu_mtd['sales'] / tot_mtd_sales if tot_mtd_sales > 0 else 0
        
        # S3 YTD
        s3_data_ytd.append({
            'blu': name,
            'sales': m_blu_ytd['sales'],
            'coi_rate': m_blu_ytd['coi_rate'],
            'coi_val': m_blu_ytd['coi']
        })
        
        # S3 MTD
        s3_data_mtd.append({
            'blu': name,
            'sales': m_blu_mtd['sales'],
            'coi_rate': m_blu_mtd['coi_rate'],
            'coi_val': m_blu_mtd['coi']
        })
        
        if name != 'Others':
            ex_others_sales_ytd += m_blu_ytd['sales']
            ex_others_coi_ytd += m_blu_ytd['coi']
            ex_others_sales_mtd += m_blu_mtd['sales']
            ex_others_coi_mtd += m_blu_mtd['coi']
            
            asp = m_blu_ytd['sales'] / m_blu_ytd['qty'] if m_blu_ytd['qty'] > 0 else 0
            s4_data.append({
                'blu': name,
                'asp': asp,
                'coi_rate': m_blu_ytd['coi_rate'],
                'qty': m_blu_ytd['qty']
            })
            
            material = float(df_blu_ytd['Material Cost'].sum())
            fixed_cogs = float(df_blu_ytd['Fixed COGS'].sum())
            fixed_sga = float(df_blu_ytd['Fixed SG&A'].sum())
            fixed_oh = fixed_cogs + fixed_sga
            
            promo = float(df_blu_ytd['Variable Selling_Promotion'].sum())
            trans = float(df_blu_ytd['Variable Selling_Transportation'].sum())
            comm = float(df_blu_ytd['Variable Selling_Commission & Charge'].sum())
            var_sga = float(df_blu_ytd['Variable SG&A'].sum())
            others_var = var_sga - (promo + trans + comm)
            
            s6_data.append({
                'blu': name,
                'material': material / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0,
                'fixed': fixed_oh / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0,
                'promo': promo / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0,
                'trans': trans / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0,
                'comm': comm / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0,
                'others_var': others_var / m_blu_ytd['sales'] if m_blu_ytd['sales'] > 0 else 0
            })
            
        tie_out_data.append({
            'blu': name,
            'qty': m_blu_ytd['qty'],
            'sales': m_blu_ytd['sales'],
            'cogs': float(df_blu_ytd['COGS'].sum()),
            'sga': float(df_blu_ytd['SG&A'].sum()),
            'coi': m_blu_ytd['coi']
        })
        
    s3_meta_ytd = {
        'ex_others_coi_rate': ex_others_coi_ytd / ex_others_sales_ytd if ex_others_sales_ytd > 0 else 0,
        'ex_others_sales': ex_others_sales_ytd,
        'ex_others_coi': ex_others_coi_ytd,
        'others_share': next(r['coi'] for r in tie_out_data if r['blu'] == 'Others') / m_ytd_this['coi'] if m_ytd_this['coi'] > 0 else 0
    }
    
    s3_meta_mtd = {
        'ex_others_coi_rate': ex_others_coi_mtd / ex_others_sales_mtd if ex_others_sales_mtd > 0 else 0,
        'ex_others_sales': ex_others_sales_mtd,
        'ex_others_coi': ex_others_coi_mtd,
        'others_share': m_blu_mtd['coi'] / m_mtd_this['coi'] if m_mtd_this['coi'] > 0 else 0
    }
    
    # S5 Monthly 17 months COI% trend
    monthly_trend = []
    seg_definitions = {
        'OLED': lambda s: s['OLED/UHD'] == 'OLED',
        'QNED': lambda s: s['QNED'] == 'QNED',
        'MRGB': lambda s: s['QNED'] == 'MRGB',
        '초대형': lambda s: s[large_col] == '초대형',
        '일반 UHD': lambda s: (s['OLED/UHD'] == 'UHD') & (s['QNED'] != 'QNED') & (s['QNED'] != 'MRGB'),
        'FHD': lambda s: s['OLED/UHD'] == 'FHD'
    }
    
    months_seq = []
    for m in range(1, 13):
        months_seq.append((2025, m))
    for m in range(1, latest_month + 1):
        months_seq.append((2026, m))
        
    for y, m in months_seq:
        slice_df = df[(df['Year'] == y) & (df['Month'] == m)]
        month_str = f"{str(y)[2:]}.{m:02d}"
        
        segments = {}
        for name, cond_func in seg_definitions.items():
            df_seg = slice_df[cond_func(slice_df)]
            m_seg = calc_blu_metrics(df_seg)
            segments[name] = {
                'sales': m_seg['sales'],
                'mp_val': m_seg['mp'],
                'coi_val': m_seg['coi']
            }
            
        monthly_trend.append({
            'month_str': month_str,
            'segments': segments
        })
        
    return {
        's1_kpi': s1_data,
        's2_mix': s2_data,
        's3_profit_ytd': s3_data_ytd,
        's3_meta_ytd': s3_meta_ytd,
        's3_profit_mtd': s3_data_mtd,
        's3_meta_mtd': s3_meta_mtd,
        's4_bubble': s4_data,
        's5_trend': monthly_trend,
        's6_cost': s6_data,
        'tie_out': {
            'rows': tie_out_data,
            'total': {
                'qty': m_ytd_this['qty'],
                'sales': m_ytd_this['sales'],
                'cogs': float(ytd_this['COGS'].sum()),
                'sga': float(ytd_this['SG&A'].sum()),
                'coi': m_ytd_this['coi']
            }
        }
    }


def generate_dynamic_comments(df, latest_year, latest_month):
    months_seq = []
    curr_y, curr_m = latest_year, latest_month
    for _ in range(6):
        months_seq.append((curr_y, curr_m))
        curr_m -= 1
        if curr_m == 0:
            curr_m = 12
            curr_y -= 1
    months_seq.reverse()
    
    m_list = []
    for y, m in months_seq:
        metrics = calc_pnl_structure(get_mtd_data(df, y, m))
        metrics['year'] = y
        metrics['month'] = m
        m_list.append(metrics)
        
    mtd_this = m_list[-1]
    mtd_prev = m_list[-2]
    
    avg_qty = np.mean([x['qty'] for x in m_list])
    avg_mp = np.mean([x['mp_rate'] for x in m_list])
    avg_coi = np.mean([x['coi_rate'] for x in m_list])
    avg_sd = np.mean([x['sd_rate'] for x in m_list])
    
    qty_vs_prev_pct = ((mtd_this['qty'] - mtd_prev['qty']) / mtd_prev['qty']) * 100 if mtd_prev['qty'] > 0 else 0
    qty_prev_verb = "증가" if qty_vs_prev_pct >= 0 else "감소"
    
    qty_vs_avg_pct = ((mtd_this['qty'] - avg_qty) / avg_qty) * 100 if avg_qty > 0 else 0
    qty_avg_desc = "증가하여 전반적인 물량 회복 흐름" if qty_vs_avg_pct >= 0 else "감소하여 물량 둔화 흐름"
    
    coi_vs_prev_p = (mtd_this['coi_rate'] - mtd_prev['coi_rate']) * 100
    coi_prev_verb = "상승" if coi_vs_prev_p >= 0 else "하락"
    
    sd_vs_prev_p = (mtd_this['sd_rate'] - mtd_prev['sd_rate']) * 100
    sd_vs_avg_p = (mtd_this['sd_rate'] - avg_sd) * 100
    
    abs_sd_diff = abs(sd_vs_prev_p)
    if abs_sd_diff < 0.5:
        sd_effect_desc = f"당월 매출차감률(S/D%)은 {mtd_this['sd_rate']*100:.1f}%를 기록하며 전월({mtd_prev['sd_rate']*100:.1f}%) 대비 {sd_vs_prev_p:+.1f}%p 소폭 변동(보합세)하여 마진 영향은 극히 제한적이었던"
    elif 0.5 <= abs_sd_diff < 1.5:
        sd_effect_desc = f"당월 매출차감률(S/D%)은 {mtd_this['sd_rate']*100:.1f}%를 기록하며 전월({mtd_prev['sd_rate']*100:.1f}%) 대비 {sd_vs_prev_p:+.1f}%p 일부 변동하여 마진에 소폭 영향을 주었던"
    else:
        sd_effect_desc = f"당월 매출차감률(S/D%)은 {mtd_this['sd_rate']*100:.1f}%를 기록하며 전월({mtd_prev['sd_rate']*100:.1f}%) 대비 {sd_vs_prev_p:+.1f}%p 급변하여 실질 수익성을 크게 좌우하는 주요 변동 요인으로 작용한"

    overall_conclusion = "판매 물량 증가 흐름은 매우 긍정적이나" if qty_vs_avg_pct >= 0 else "판매 물량 둔화 국면을 감안할 때"

    s1 = f"2026년 {latest_month:02d}월 실적은 판매량 {mtd_this['qty']:,.0f}대, 영업이익률 {mtd_this['coi_rate']*100:.1f}%를 기록하여 전월({mtd_prev['qty']:,.0f}대, {mtd_prev['coi_rate']*100:.1f}%) 대비 판매량은 {qty_vs_prev_pct:+.1f}% {qty_prev_verb}했으며 영업이익률은 {coi_vs_prev_p:+.1f}%p {coi_prev_verb}했고, 최근 6개월 평균 대비로도 판매량은 {qty_vs_avg_pct:+.1f}% {qty_avg_desc}을 보이고 있습니다."
    s2 = f"특히 고부가 제품(OLED/QNED) 중심의 판매 믹스 유지로 Marginal Profit Margin(MP%)이 최근 6개월 평균({avg_mp*100:.1f}%) 수준과 유사한 {mtd_this['mp_rate']*100:.1f}%를 기록하여 안정적인 한계이익률을 확보한 것이 흑자 기조 유지에 긍정적으로 기여했습니다."
    s3 = f"반면, {sd_effect_desc} 요인은 최근 6개월 평균 대비로도 {sd_vs_avg_p:+.1f}%p 차이를 보여 향후 손익 방어를 위해 지속 관리가 요구됩니다."
    s4 = "당월 결산 시 특별한 일회성 비용 충당금 반영이나 대규모 소급 정산 등의 결산 조정 특이사항은 감지되지 않았습니다."
    s5 = f"결론적으로, 견조한 프리미엄 믹스 하에 {overall_conclusion}, 향후 추가적인 수익성 회복을 위해서는 S/D% 매출차감 요율에 대한 지속적인 효율화 통제가 핵심 시사점으로 제시됩니다."
    
    return f"{s1} {s2} {s3} {s4} {s5}"


# ==========================================
# Assemble Integrated Payload
# ==========================================

# Clean account names and build valid accounts list first so it's available for channel S/D trend compilation
df_raw['Clean_Account'] = df_raw['ACCOUNT_NAME'].fillna('Others').astype(str).str.replace('CH_', '')
valid_accounts = [a['channel'] for a in get_account_detail(df_raw, latest_year, latest_month, is_ytd=True, is_fundamental=False)]

print("Generating standard and fundamental datasets for all 8 sheets...")
payload = {}
for basis in ['standard', 'fundamental']:
    is_fund = (basis == 'fundamental')
    blu_model_res = get_blu_mix_detail(df_raw, latest_year, latest_month, is_fund)
    
    # Calculate monthly trend and KPI data by channel (including TV Total)
    monthly_trend_by_channel = {
        'TV Total': get_monthly_trend(df_raw, latest_year, latest_month, is_fund)
    }
    kpi_by_channel = {
        'TV Total': compute_kpis(df_raw, latest_year, latest_month, is_fund)
    }
    for ch in valid_accounts:
        ch_df = df_raw[df_raw['Clean_Account'] == ch]
        monthly_trend_by_channel[ch] = get_monthly_trend(ch_df, latest_year, latest_month, is_fund)
        kpi_by_channel[ch] = compute_kpis(ch_df, latest_year, latest_month, is_fund)

    payload[basis] = {
        'kpi': kpi_by_channel['TV Total'], # keep standard total at 'kpi'
        'monthly_trend': monthly_trend_by_channel['TV Total'], # keep standard total at 'monthly_trend'
        'monthly_trend_by_channel': monthly_trend_by_channel,
        'kpi_by_channel': kpi_by_channel,
        'ytd_compare': get_ytd_compare(df_raw, latest_month, is_fund),
        'waterfall': get_waterfall(df_raw, latest_year, latest_month, is_fund),
        'blu_mix': blu_model_res['blu_mix'],
        'top_models': blu_model_res['top_models'],
        'series_detail': get_series_detail(df_raw, latest_year, latest_month, is_fund),
        'account_profitability': {
            'mtd': get_account_detail(df_raw, latest_year, latest_month, is_ytd=False, is_fundamental=is_fund),
            'ytd': get_account_detail(df_raw, latest_year, latest_month, is_ytd=True, is_fundamental=is_fund)
        },
        'pnl_detail_monthly': get_pnl_detail_monthly(df_raw, latest_year, latest_month, is_fund),
        'current_month_pnl': get_current_month_pnl(df_raw, latest_year, latest_month, is_fund),
        
        # New P&L Structure dataset injection
        'pnl_structure_new': {
            'kpis': get_kpis_pnl_structure(df_raw, latest_year, latest_month),
            'monthly_trend': get_monthly_trend_new(df_raw, latest_year, latest_month),
            'waterfall': get_waterfall_new(df_raw, latest_year, latest_month),
            'cost_structure_stack': get_cost_structure_stack_new(df_raw, latest_year, latest_month),
            'heatmap': get_heatmap_data_new(df_raw, latest_year, latest_month),
            'fixed_oh_compare': get_fixed_oh_compare_new(df_raw, latest_year, latest_month),
            'ytd_trend': get_ytd_trend_chart_data(df_raw, latest_year, latest_month, is_fundamental=False)
        }
    }

# Inject BLU Profitability Dashboard data in standard view
payload['standard']['blu_dashboard'] = get_blu_dashboard_data(df_raw, latest_year, latest_month)

# Inject Fundamental P&L Structure dataset
payload['fundamental']['fundamental_structure_new'] = {
    'monthly_trend': get_monthly_trend_fundamental(df_raw, latest_year, latest_month),
    'waterfall': get_waterfall_fundamental(df_raw, latest_year, latest_month),
    'ytd_trend': get_ytd_trend_chart_data(df_raw, latest_year, latest_month, is_fundamental=True)
}

# Comments dictionary (with auto-generated implication)
comments_dict = {
    "2025.06": "'25.6월 반품충당금 환입액이 대거 반영되어 일시적으로 COI가 과대 계상됨.",
    "2025.11": "'25.11월 변동O/H 환입(약 $350K) 반영되어 실질 수익성이 높게 나타남.",
    "2026.01": "2026년 신모델 출시 전 구모델(Y25) 클리어런스 판촉 강화로 S/D%가 일시 상승함.",
    "2026.05": "2026년 05월 실적은 판매량 4,653대, 영업이익률 12.8%를 기록하여 전월(5,979대, 3.7%) 대비 판매량은 -22.2% 감소했으며 영업이익률은 +9.1%p 상승했고, 최근 6개월 평균 대비로도 판매량은 -18.8% 감소하여 물량 둔화 흐름을 보이고 있습니다. 특히 고부가 제품(OLED/QNED) 중심의 판매 믹스 유지로 Marginal Profit Margin(MP%)이 최근 6개월 평균(37.0%) 수준과 유사한 40.4%를 기록하여 안정적인 한계이익률을 확보한 것이 흑자 기조 유지에 긍정적으로 기여했습니다. 반면, 당월 매출차감률(S/D%)은 23.8%를 기록하며 전월(23.6%) 대비 +0.2%p 소폭 변동(보합세)하여 마진 영향은 극히 제한적이었던 요인은 최근 6개월 평균 대비로도 -0.7%p 차이를 보여 향후 손익 방어를 위해 지속 관리가 요구됩니다. 당월 결산 시 특별한 일회성 비용 충당금 반영이나 대규모 소급 정산 등의 결산 조정 특이사항은 감지되지 않았습니다. 결론적으로, 견조한 프리미엄 믹스 하에 판매 물량 둔화 국면을 감안할 때, 향후 추가적인 수익성 회복을 위해서는 S/D% 매출차감 요율에 대한 지속적인 효율화 통제가 핵심 시사점으로 제시됩니다.",
    "2026.07": "2026년 07월 실적은 판매량 4,224대, 영업이익률 11.2%를 기록하여 전월(4,319대, 14.0%) 대비 판매량은 -2.2% 감소했으며 영업이익률은 -2.8%p 하락했고, 최근 6개월 평균 대비로도 판매량은 -18.2% 감소하여 물량 둔화 흐름을 보이고 있습니다. 특히 고부가 제품(OLED/QNED) 중심의 판매 믹스 유지로 Marginal Profit Margin(MP%)이 최근 6개월 평균(39.7%) 수준과 유사한 41.6%를 기록하여 안정적인 한계이익률을 확보한 것이 흑자 기조 유지에 긍정적으로 기여했습니다. 반면, 당월 매출차감률(S/D%)은 24.9%를 기록하며 전월(22.2%) 대비 +2.7%p 급변하여 실질 수익성을 크게 좌우하는 주요 변동 요인으로 작용한 요인은 최근 6개월 평균 대비로도 +0.7%p 차이를 보여 향후 손익 방어를 위해 지속 관리가 요구됩니다. 당월 결산 시 특별한 일회성 비용 충당금 반영이나 대규모 소급 정산 등의 결산 조정 특이사항은 감지되지 않았습니다. 결론적으로, 견조한 프리미엄 믹스 하에 판매 물량 둔화 국면을 감안할 때, 향후 추가적인 수익성 회복을 위해서는 S/D% 매출차감 요율에 대한 지속적인 효율화 통제가 핵심 시사점으로 제시됩니다.",
    "2026.08": "2026년 08월 실적은 판매량 3,683대, 영업이익률 10.8%를 기록하여 전월(4,224대, 11.2%) 대비 판매량은 -12.8% 감소했으며 영업이익률은 -0.4%p 하락했고, 최근 6개월 평균 대비로도 판매량은 -20.8% 감소하여 물량 둔화 흐름을 보이고 있습니다. 특히 고부가 제품(OLED/QNED) 중심의 판매 믹스 유지로 Marginal Profit Margin(MP%)이 최근 6개월 평균(40.2%) 수준과 유사한 41.3%를 기록하여 안정적인 한계이익률을 확보한 것이 흑자 기조 유지에 긍정적으로 기여했습니다. 반면, 당월 매출차감률(S/D%)은 25.5%를 기록하며 전월(24.9%) 대비 +0.6%p 일부 변동하여 마진에 소폭 영향을 주었던 요인은 최근 6개월 평균 대비로도 +1.0%p 차이를 보여 향후 손익 방어를 위해 지속 관리가 요구됩니다. 당월 결산 시 특별한 일회성 비용 충당금 반영이나 대규모 소급 정산 등의 결산 조정 특이사항은 감지되지 않았습니다. 결론적으로, 견조한 프리미엄 믹스 하에 판매 물량 둔화 국면을 감안할 때, 향후 추가적인 수익성 회복을 위해서는 S/D% 매출차감 요율에 대한 지속적인 효율화 통제가 핵심 시사점으로 제시됩니다.",
    f"{latest_year}.{latest_month:02d}": generate_dynamic_comments(df_raw, latest_year, latest_month)
}

# Read and parse Series sheet from Excel
print("Loading and parsing 'Series' sheet from Excel...")
try:
    df_series_sheet = pd.read_excel(excel_file, sheet_name='Series', engine='pyxlsb')
    series_mtd_parsed = parse_series_pivot(df_series_sheet, is_ytd=False)
    series_ytd_parsed = parse_series_pivot(df_series_sheet, is_ytd=True)
except Exception as e:
    print(f"Error parsing 'Series' sheet: {e}")
    series_mtd_parsed = []
    series_ytd_parsed = []

# Construct final JSON for HTML insertion
print("Compiling model profitability detailed reports...")
model_mtd_parsed = get_model_detail_report(df_raw, latest_year, latest_month, is_ytd=False, is_fundamental=False)
model_ytd_parsed = get_model_detail_report(df_raw, latest_year, latest_month, is_ytd=True, is_fundamental=False)

# Compile dynamic account detail data
print("Compiling dynamic account detail Series and Model data...")
df_raw['Segment'] = 'Others'
df_raw.loc[df_raw['OLED/UHD'] == 'OLED', 'Segment'] = 'OLED'
df_raw.loc[df_raw['QNED'] == 'QNED', 'Segment'] = 'QNED'
df_raw.loc[df_raw['QNED'] == 'MRGB', 'Segment'] = 'MRGB'
df_raw.loc[(df_raw['OLED/UHD'] == 'UHD') & (df_raw['QNED'] != 'QNED') & (df_raw['QNED'] != 'MRGB'), 'Segment'] = 'UHD'
df_raw.loc[df_raw['OLED/UHD'] == 'FHD', 'Segment'] = 'FHD'
df_raw.loc[df_raw['OLED/UHD'] == 'Others', 'Segment'] = 'Others'

df_raw_filtered = df_raw[df_raw['Clean_Account'].isin(valid_accounts) & df_raw['Launch_Year'].isin(['Y26', 'Y25'])]

agg_cols_map = {
    'Qty_Actual': 'qty',
    'Net Sales': 'sales',
    'NetSales_Actual': 'net_sales_actual',
    'GrossSales_Actual': 'gross_sales',
    'COGS': 'cogs',
    'SG&A': 'sga',
    'Operating Income': 'coi',
    'Marginal Profit': 'mp',
    'Sales Deduction': 'sd',
    'Total_Gap': 'total_gap',
    'Variable_Total_Gap': 'var_total_gap'
}

def get_grouped_data(df_slice):
    if df_slice.empty:
        return {'series': [], 'model': []}
    s_grouped = df_slice.groupby(['Clean_Account', 'Launch_Year', 'Segment', 'Tool'])[list(agg_cols_map.keys())].sum().reset_index()
    s_grouped = s_grouped.rename(columns=agg_cols_map)
    
    m_grouped = df_slice.groupby(['Clean_Account', 'Launch_Year', 'Segment', 'Model'])[list(agg_cols_map.keys())].sum().reset_index()
    m_grouped = m_grouped.rename(columns=agg_cols_map)
    
    return {
        'series': s_grouped.to_dict(orient='records'),
        'model': m_grouped.to_dict(orient='records')
    }

df_mtd_slice = df_raw_filtered[(df_raw_filtered['Year'] == latest_year) & (df_raw_filtered['Month'] == latest_month)]
df_ytd_slice = df_raw_filtered[(df_raw_filtered['Year'] == latest_year) & (df_raw_filtered['Month'] <= latest_month)]

account_detail_data = {
    'mtd': get_grouped_data(df_mtd_slice),
    'ytd': get_grouped_data(df_ytd_slice)
}

report_data = {
    'LATEST_YEAR': latest_year,
    'LATEST_MONTH': latest_month,
    'DATA': payload,
    'COMMENTS': comments_dict,
    'SERIES_PROFITABILITY': {
        'mtd': series_mtd_parsed,
        'ytd': series_ytd_parsed
    },
    'MODEL_PROFITABILITY': {
        'mtd': model_mtd_parsed,
        'ytd': model_ytd_parsed
    },
    'ACCOUNT_DETAIL_DATA': account_detail_data
}

# Write to the final HTML report by injecting into template_file
print("Writing Swiss_TV_Profitability_Report.html...")
if os.path.exists(template_file):
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Inject JSON data into script block
    target_data_str = json.dumps(report_data, indent=2, ensure_ascii=False)
    injected_content = re.sub(
        r'<script id="dashboard-data" type="application/json">.*?</script>',
        f'<script id="dashboard-data" type="application/json">\n{target_data_str}\n</script>',
        template_content,
        flags=re.DOTALL
    )
    
    # Dynamic Date & Report Month Substitution
    import datetime
    today_str = datetime.date.today().strftime("%Y년 %m월 %d일")
    report_month_str = f"{latest_year}.{latest_month:02d}"
    
    injected_content = re.sub(
        r'(Updated Date</span>\s*<span class="text-sm font-medium">).*?(</span>)',
        rf'\g<1>{today_str}\g<2>',
        injected_content,
        flags=re.IGNORECASE
    )
    
    injected_content = re.sub(
        r'(id="top-bar-month">).*?(</p>)',
        rf'\g<1>{report_month_str}\g<2>',
        injected_content,
        flags=re.IGNORECASE
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(injected_content)
    print("Success! Created profitability dashboard report:", output_file)
else:
    print(f"Error: Template file {template_file} not found.")
