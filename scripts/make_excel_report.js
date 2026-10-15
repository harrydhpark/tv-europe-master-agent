const fs = require('fs');
const path = require('path');

// Run python script to create formatted Excel report using openpyxl
const pyScript = `
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json

with open(r'd:\\TV 유럽영업\\15. AX Task\\2026 AX 실행과제\\99. Master Agent\\scripts\\extracted_subs_data.json', 'r', encoding='utf-8') as f:
    raw = f.read()

start_idx = raw.find('[')
data = json.loads(raw[start_idx:])

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "리스크법인_WOS_OLED요약"

# Ensure gridlines
ws.views.sheetView[0].showGridLines = True

# Palettes
NAVY = "1B365D"
DARK_NAVY = "0F2027"
TEAL = "008080"
LIGHT_BLUE = "F0F4F8"
RISK_RED_BG = "FDE8E8"
RISK_RED_TXT = "C81E1E"
SAFE_GREEN_BG = "DEF7EC"
SAFE_GREEN_TXT = "03543F"
ZEBRA_ROW = "F9FAFB"

font_title = Font(name="Malgun Gothic", size=15, bold=True, color="1B365D")
font_sub = Font(name="Malgun Gothic", size=9, color="555555", italic=True)
font_hdr = Font(name="Malgun Gothic", size=10, bold=True, color="FFFFFF")
font_subhdr = Font(name="Malgun Gothic", size=9, bold=True, color="FFFFFF")
font_data = Font(name="Malgun Gothic", size=9)
font_bold = Font(name="Malgun Gothic", size=9, bold=True)
font_risk = Font(name="Malgun Gothic", size=9, bold=True, color=RISK_RED_TXT)
font_safe = Font(name="Malgun Gothic", size=9, bold=True, color=SAFE_GREEN_TXT)

fill_hdr = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
fill_subhdr = PatternFill(start_color="2C4D75", end_color="2C4D75", fill_type="solid")
fill_zebra = PatternFill(start_color=ZEBRA_ROW, end_color=ZEBRA_ROW, fill_type="solid")
fill_risk = PatternFill(start_color=RISK_RED_BG, end_color=RISK_RED_BG, fill_type="solid")
fill_safe = PatternFill(start_color=SAFE_GREEN_BG, end_color=SAFE_GREEN_BG, fill_type="solid")
fill_total = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D1D5DB'),
    right=Side(style='thin', color='D1D5DB'),
    top=Side(style='thin', color='D1D5DB'),
    bottom=Side(style='thin', color='D1D5DB')
)

# Header Title
ws.merge_cells("A1:M1")
ws["A1"] = "유럽 전 법인 유통재고 주수(WOS) 리스크 진단 및 OLED 신모델 비중 종합 분석"
ws["A1"].font = font_title
ws["A1"].alignment = Alignment(vertical="center")
ws.row_dimensions[1].height = 32

ws.merge_cells("A2:M2")
ws["A2"] = "기준 시점: 2026년 9월 (9/21W 주차 실적 기준, 9/28W 조회) | 출처: LGE Europe Master KPI Sheet & GDMI"
ws["A2"].font = font_sub
ws.row_dimensions[2].height = 18

# Table Headers
headers = [
    "구분", "법인코드", "법인명", "유통재고 WOS", "재고 리스크 판정",
    "유통재고(대)", "신모델 재고(대)", "Sell-out(대)", "OLED 신모델(대)",
    "OLED 내 신모델비중", "신모델 내 OLED비중", "전체TV 내 OLED신모델", "신모델 WOS"
]

for col_num, h_text in enumerate(headers, 1):
    c = ws.cell(row=4, column=col_num, value=h_text)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border
ws.row_dimensions[4].height = 28

# Populate data
row_idx = 5
for item in data:
    sub = item['sub']
    name = item['name']
    s = item['sep']
    
    is_eu = (sub == 'EU')
    wos = s['wosTTL']
    is_risk = (wos > 6 or (wos > 0 and wos < 3)) if wos else False
    risk_label = "정상 (3~6주)"
    if wos and wos > 6:
        risk_label = "과다재고 (>6주)"
    elif wos and wos < 3:
        risk_label = "재고부족 (<3주)"
        
    status_tag = "EU 본부" if is_eu else ("★ 리스크" if is_risk else "정상")

    row_vals = [
        status_tag,
        sub,
        name,
        round(wos, 2) if wos else 0,
        risk_label,
        round(s['chInvTTL'] or 0),
        round(s['chInvNew'] or 0),
        round(s['soTTL'] or 0),
        round(s['soOledNew'] or 0),
        s['oledNewRatioInOled_SO'] / 100.0,
        s['oledRatioInNew_SO'] / 100.0,
        s['oledNewRatioInTotal_SO'] / 100.0,
        round(s['wosNew'] or 0, 2) if s['wosNew'] else 0
    ]

    for col_num, val in enumerate(row_vals, 1):
        c = ws.cell(row=row_idx, column=col_num, value=val)
        c.font = font_data
        c.border = thin_border

        if is_eu:
            c.fill = fill_total
            c.font = font_bold
        elif row_idx % 2 == 0:
            c.fill = fill_zebra

        # Alignments & Number formats
        if col_num in [1, 2, 5]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            if col_num == 5:
                if is_risk:
                    c.fill = fill_risk
                    c.font = font_risk
                elif not is_eu:
                    c.fill = fill_safe
                    c.font = font_safe
        elif col_num == 3:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_num in [4, 13]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '0.00"주"'
            if col_num == 4 and is_risk and not is_eu:
                c.font = font_risk
        elif col_num in [6, 7, 8, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '#,##0"대"'
        elif col_num in [10, 11, 12]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '0.0%'

    ws.row_dimensions[row_idx].height = 22
    row_idx += 1

# Column widths
for col in ws.columns:
    max_len = 0
    col_letter = get_column_letter(col[0].column)
    for cell in col:
        v = str(cell.value or '')
        # count korean double
        k_len = sum(2 if ord(c) > 127 else 1 for c in v)
        max_len = max(max_len, k_len)
    ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

ws.column_dimensions['A'].width = 12
ws.column_dimensions['B'].width = 10
ws.column_dimensions['C'].width = 24
ws.column_dimensions['E'].width = 16

out_path = r'd:\\TV 유럽영업\\15. AX Task\\2026 AX 실행과제\\99. Master Agent\\유럽_법인별_유통재고WOS_OLED신모델비중_요약.xlsx'
wb.save(out_path)
print(f"Report Excel generated successfully at: {out_path}")
`

fs.writeFileSync('scripts/generate_excel_report.py', pyScript, 'utf8');
console.log('Created scripts/generate_excel_report.py');
