# -*- coding: utf-8 -*-
import json, re, glob, os, sys

BASE_DIR = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from generate_index import countries_info

print(f"| 법인 / 국가 (코드) | 통화 | 2026년 9월(MTD) Sales | 9월 COI% | 9월 MP% | 1~9월(YTD) Sales | YTD COI% | YTD MP% |")
print(f"| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

total_mtd_sales = 0
total_mtd_coi_val = 0
total_ytd_sales = 0
total_ytd_coi_val = 0

for code, info in countries_info.items():
    file_path = os.path.join(BASE_DIR, info['path'].replace('./', ''))
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'<script id="dashboard-data" type="application/json">\s*(.*?)\s*</script>', html, re.DOTALL)
    if not m:
        continue
    data = json.loads(m.group(1))
    
    kpi_ytd = data['DATA']['standard']['kpi']['ytd']
    kpi_mtd = data['DATA']['standard']['kpi']['mtd']
    
    m_s = kpi_mtd['sales']
    m_coi_rate = kpi_mtd['coi']
    m_mp_rate = kpi_mtd.get('mp', 0.0)
    
    y_s = kpi_ytd['sales']
    y_coi_rate = kpi_ytd['coi']
    y_mp_rate = kpi_ytd.get('mp', 0.0)

    total_mtd_sales += m_s
    total_mtd_coi_val += (m_s * m_coi_rate)
    total_ytd_sales += y_s
    total_ytd_coi_val += (y_s * y_coi_rate)
    
    m_sales = f"{int(round(m_s / 1000)):,}K$"
    m_coi = f"{m_coi_rate * 100:.1f}%"
    m_mp = f"{m_mp_rate * 100:.1f}%"
    
    y_sales = f"{y_s / 1000000:.1f}M$"
    y_coi = f"{y_coi_rate * 100:.1f}%"
    y_mp = f"{y_mp_rate * 100:.1f}%"
    
    # Currency
    curr = 'CHF' if code == 'Swiss' else ('GBP' if code == 'UK' else ('SEK' if code == 'SW' else 'EUR'))
    
    print(f"| **{info['name']}** | {curr} | {m_sales} | {m_coi} | {m_mp} | {y_sales} | {y_coi} | {y_mp} |")

avg_mtd_coi = total_mtd_coi_val / total_mtd_sales if total_mtd_sales > 0 else 0
avg_ytd_coi = total_ytd_coi_val / total_ytd_sales if total_ytd_sales > 0 else 0

print(f"| **전체 15개국 합계 (Total)** | USD | **{int(round(total_mtd_sales/1000)):,}K$** | **{avg_mtd_coi*100:.1f}%** | - | **{total_ytd_sales/1000000:.1f}M$** | **{avg_ytd_coi*100:.1f}%** | - |")
