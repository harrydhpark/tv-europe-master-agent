import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Create workbook
wb = openpyxl.Workbook()

# Sheet 1: 55인치 & 65인치 OLED 비교 요약 (Price Gap & ATA Guide)
ws1 = wb.active
ws1.title = "OLED_PriceGap_ATA_요약"
ws1.views.sheetView[0].showGridLines = True

# Sheet 2: 스페인 MediaMarkt 모델별 상세 가격
ws2 = wb.create_sheet(title="스페인_MediaMarkt_RAW")
ws2.views.sheetView[0].showGridLines = True

# Color palette
NAVY_HEADER = "1B365D"
TEAL_HEADER = "008080"
LIGHT_GRAY = "F8FAFC"
ZEBRA_ROW = "F1F5F9"
ALERT_RED = "DC2626"
SAFE_GREEN = "16A34A"
WARN_AMBER = "D97706"
BORDER_GRAY = "CBD5E1"

font_title = Font(name="맑은 고딕", size=14, bold=True, color="1B365D")
font_subtitle = Font(name="맑은 고딕", size=10, italic=True, color="475569")
font_sec = Font(name="맑은 고딕", size=11, bold=True, color="1B365D")
font_th = Font(name="맑은 고딕", size=10, bold=True, color="FFFFFF")
font_data = Font(name="맑은 고딕", size=9.5)
font_bold = Font(name="맑은 고딕", size=9.5, bold=True)
font_num = Font(name="Segoe UI", size=9.5)
font_num_bold = Font(name="Segoe UI", size=9.5, bold=True)

fill_navy = PatternFill("solid", fgColor=NAVY_HEADER)
fill_teal = PatternFill("solid", fgColor=TEAL_HEADER)
fill_zebra = PatternFill("solid", fgColor=ZEBRA_ROW)
fill_red_light = PatternFill("solid", fgColor="FEE2E2")
fill_green_light = PatternFill("solid", fgColor="DCFCE7")
fill_amber_light = PatternFill("solid", fgColor="FEF3C7")

thin_side = Side(border_style="thin", color=BORDER_GRAY)
med_side = Side(border_style="medium", color=NAVY_HEADER)
double_side = Side(border_style="double", color=NAVY_HEADER)
border_cell = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
border_header = Border(left=thin_side, right=thin_side, top=med_side, bottom=med_side)
border_total = Border(left=thin_side, right=thin_side, top=thin_side, bottom=double_side)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

# Title Header
ws1["A1"] = "스페인 MediaMarkt 55\"/65\" OLED 최저가 변동, Price Gap 및 ATA 승인 가이드라인 비교"
ws1["A1"].font = font_title
ws1["A2"] = "기준 시점: 2026년 9월 최신 (2026-09-29 조사) | 통화: EUR (€) | 원천: 04. Price Tracker & 260619 ATA 가이드 v1.0"
ws1["A2"].font = font_subtitle

# Table 1: 55" OLED 비교 매트릭스
ws1["A4"] = "1. 55인치 OLED 최저가 변동, 대 삼성 Price Gap 및 ATA Guide 최저 승인선"
ws1["A4"].font = font_sec

headers_55 = [
    "구분", "라인업", "LG 모델명", "LG 최저가 (€)", "대응 삼성 모델", "삼성 최저가 (€)", 
    "Price Gap (€)", "Price Gap (%)", "ATA 가이드 기준선", "ATA 최저승인 가능선 (€)", "ATA 판정", "비고 및 프로모션"
]

for col_idx, h in enumerate(headers_55, 1):
    cell = ws1.cell(5, col_idx, h)
    cell.font = font_th
    cell.fill = fill_navy if col_idx <= 8 else fill_teal
    cell.alignment = align_center
    cell.border = border_header

data_55 = [
    ["신모델 볼륨", "B6 vs S90H", "OLED55B65LA", 1001.33, "TQ55S90HAEXXC", 1299.00, -297.67, "-22.9%", "C6대비 $200 Gap / S85비 100", 1099.00, "초과할인(하한이탈)", "온라인 한정 단독 특가 (-33% 인하)"],
    ["신모델 파생", "B6E vs S90H", "OLED55B6ELC", 1499.00, "TQ55S90HAEXXC", 1299.00, 200.00, "+15.4%", "B6대비 $100 Gap 이내", 1199.00, "승인가능", "정가 유지 상태 (프로모션 미적용)"],
    ["신모델 메인", "C6 vs S90H", "OLED55C66", 1596.00, "TQ55S90HAEXXC", 1299.00, 297.00, "+22.9%", "S90비 ATA Index 100~105", 1299.00, "승인가능 (대응필요)", "삼 S90H Back to School(-35%) 대응시 €1,299 승인가능"],
    ["신모델 메인", "C6(캐시백) vs S90H", "OLED55C65LA", 1749.00, "TQ55S90HAEXXC", 1299.00, 450.00, "+34.6%", "S90비 ATA Index 100~105", 1299.00, "승인가능", "판매가 €1,899, 캐시백 €150 적용 시 실체감가"],
    ["신모델 프리미엄", "G6 vs S95H", "OLED55G66LS", 1599.00, "TQ55S95HFTXXC", 2299.00, -700.00, "-30.4%", "S95H 대비 프리미엄 유지", 1999.00, "초우량 승인", "판매가 €1,799, 캐시백 €200 적용. 삼 S95H 압도"],
    ["신모델 프리미엄", "G6 vs S99H", "OLED55G64LW", 2199.00, "TQ55S99HATXXC", 2299.00, -100.00, "-4.3%", "S99H(OneConnect) 동등대응", 2199.00, "승인가능", "삼 S99H(€2,499 - 캐시백€200=€2,299)와 1:1 대등"]
]

for row_idx, row_data in enumerate(data_55, 6):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws1.cell(row_idx, col_idx, val)
        cell.font = font_data
        cell.border = border_cell
        if col_idx in [1, 2, 5]:
            cell.alignment = align_center
        elif col_idx in [3, 9, 12]:
            cell.alignment = align_left
        elif col_idx in [4, 6, 7, 10]:
            cell.alignment = align_right
            cell.font = font_num_bold if col_idx in [4, 6, 7] else font_num
            if isinstance(val, (int, float)):
                cell.number_format = "#,##0.00"
        elif col_idx == 8:
            cell.alignment = align_right
            cell.font = font_num_bold
        elif col_idx == 11:
            cell.alignment = align_center
            cell.font = font_bold
            if "초과" in str(val):
                cell.fill = fill_amber_light
                cell.font = Font(name="맑은 고딕", size=9.5, bold=True, color="B45309")
            elif "승인" in str(val):
                cell.fill = fill_green_light
                cell.font = Font(name="맑은 고딕", size=9.5, bold=True, color="15803D")

# Table 2: 65" OLED 비교 매트릭스
start_r2 = 14
ws1.cell(start_r2, 1, "2. 65인치 OLED 최저가 변동, 대 삼성 Price Gap 및 ATA Guide 최저 승인선").font = font_sec

for col_idx, h in enumerate(headers_55, 1):
    cell = ws1.cell(start_r2 + 1, col_idx, h)
    cell.font = font_th
    cell.fill = fill_navy if col_idx <= 8 else fill_teal
    cell.alignment = align_center
    cell.border = border_header

data_65 = [
    ["신모델 볼륨", "B6 vs S90H", "OLED65B6ELC", 1146.65, "TQ65S90HAEXXC", 2299.00, -1152.35, "-50.1%", "C6대비 $200 Gap / S85비 100", 1499.00, "초과할인(하한이탈)", "정가 €1,349 대비 -15% 인하. 삼 S90H 정가복귀로 갭 극대화"],
    ["신모델 메인", "C6 vs S90H", "OLED65C65LA", 1529.00, "TQ65S90HAEXXC", 2299.00, -770.00, "-33.5%", "S90비 ATA Index 100~105", 1599.00, "승인가능 (Floor근접)", "판매가 €1,729, 캐시백 €200 적용 시 실체감가 €1,529"],
    ["신모델 메인", "C6(일반) vs S90H", "OLED65C66", 2212.90, "TQ65S90HAEXXC", 2299.00, -86.10, "-3.7%", "S90비 ATA Index 100~105", 1599.00, "승인가능", "캐시백/할인 없는 스탠다드 판매가. 삼 S90H와 대등 수준"],
    ["신모델 무선", "M5(무선) vs S99H", "OLED65M59LA", 1699.00, "TQ65S99HATXXC", 2099.00, -400.00, "-19.1%", "S99H(OneConnect) 대비 우위", 1899.00, "초우량 승인", "판매가 €2,099, 캐시백 €400. 삼 S99H(€2,299-€200) 대비 €400 우위"],
    ["신모델 프리미엄", "G6 vs S99H", "OLED65G64LW", 1899.00, "TQ65S99HATXXC", 2099.00, -200.00, "-9.5%", "S99H 대비 동등/프리미엄", 1999.00, "승인가능", "판매가 €2,199, 캐시백 €300 적용. 삼 플래그십 공세 완벽 방어"],
    ["신모델 프리미엄", "G6(스탠드) vs S95H", "OLED65G66LS", 2228.90, "TQ65S95HFTXXC", 3199.00, -970.10, "-30.3%", "S95H 대비 프리미엄 유지", 2199.00, "승인가능", "삼 S95H(€3,499 - 캐시백€300=€3,199) 대비 €970 가격 경쟁력"]
]

for row_idx, row_data in enumerate(data_65, start_r2 + 2):
    for col_idx, val in enumerate(row_data, 1):
        cell = ws1.cell(row_idx, col_idx, val)
        cell.font = font_data
        cell.border = border_cell
        if col_idx in [1, 2, 5]:
            cell.alignment = align_center
        elif col_idx in [3, 9, 12]:
            cell.alignment = align_left
        elif col_idx in [4, 6, 7, 10]:
            cell.alignment = align_right
            cell.font = font_num_bold if col_idx in [4, 6, 7] else font_num
            if isinstance(val, (int, float)):
                cell.number_format = "#,##0.00"
        elif col_idx == 8:
            cell.alignment = align_right
            cell.font = font_num_bold
        elif col_idx == 11:
            cell.alignment = align_center
            cell.font = font_bold
            if "초과" in str(val):
                cell.fill = fill_amber_light
                cell.font = Font(name="맑은 고딕", size=9.5, bold=True, color="B45309")
            elif "승인" in str(val):
                cell.fill = fill_green_light
                cell.font = Font(name="맑은 고딕", size=9.5, bold=True, color="15803D")

# Table 3: ATA 가이드라인 핵심 원칙 & 액션 가이드
start_r3 = 24
ws1.cell(start_r3, 1, "3. 스페인 지사(LGEES) ATA Guide 심사 및 전략적 의사결정 권고").font = font_sec

guidelines = [
    ("① C6 시리즈 (55\"/65\")", "55C6는 삼성 S90H 기습 할인(€1,299)에 대응하여 지사에서 €1,299 매칭 인하 요청 시 ATA Index 100 기준 즉시 승인 가능. 65C6는 현재 실체감가 €1,529로 Floor Price(€1,599)에 근접해 있으므로 추가적인 공급가 인하는 엄격 제한하고 매장 POS 번들 판촉으로 전환."),
    ("② B6 시리즈 (55\"/65\")", "현재 55B6(€1,001.33) 및 65B6(€1,146.65)는 온라인 유통의 과도한 할인으로 인해 공식 ATA Floor Price(€1,099 / €1,499)를 하회하고 있음. B시리즈의 추가 하락은 자사 브랜드 가치 및 C시리즈 잠식(Cannibalization)을 유발하므로 추가 출하가 인하는 '승인 불가(Reject)' 조치 필요."),
    ("③ C-B 시리즈 간격 준수", "공식 가이드상 65\"/55\" C-B 간격은 $200 (€180~€200) 유지 원칙. 현재 65인치 갭이 €582로 과도하게 벌어져 있으므로, 65C6(€1,729)로의 업셀링 마케팅을 적극 전개하여 프리미엄 믹스 개선."),
    ("④ G6 / M5 플래그십", "삼성 S99H(원커넥트 박스) 및 S95H 대비 무선 M5(€1,699) 및 G6(€1,899)가 €200~€970의 견고한 가격 우위를 점하고 있어 4분기 프리미엄 OLED 시장 1위 수성 유력.")
]

for g_idx, (title, desc) in enumerate(guidelines, start_r3 + 1):
    ws1.cell(g_idx, 1, title).font = font_bold
    ws1.cell(g_idx, 1).alignment = align_left
    ws1.cell(g_idx, 2, desc).font = font_data
    ws1.cell(g_idx, 2).alignment = align_left
    ws1.merge_cells(start_row=g_idx, start_column=2, end_row=g_idx, end_column=12)

# Auto column widths for Sheet 1
for col in ws1.columns:
    max_len = 0
    col_letter = get_column_letter(col[0].column)
    for cell in col:
        if cell.row in [1, 2, 4, 14, 24] or (cell.row > 24 and col_letter != 'A'):
            continue
        v = str(cell.value or "")
        max_len = max(max_len, len(v))
    ws1.column_dimensions[col_letter].width = max(max_len + 3, 12)

ws1.column_dimensions["A"].width = 16
ws1.column_dimensions["B"].width = 18
ws1.column_dimensions["C"].width = 18
ws1.column_dimensions["E"].width = 18
ws1.column_dimensions["I"].width = 25
ws1.column_dimensions["K"].width = 20
ws1.column_dimensions["L"].width = 38

# Populate Sheet 2: RAW Models
ws2["A1"] = "스페인 MediaMarkt 2026-09-29 OLED 전수 조사 데이터"
ws2["A1"].font = font_title

raw_headers = ["조사일자", "제조사", "화면크기(인치)", "시리즈구분", "모델코드", "판매가격(EUR)", "원가격(EUR)", "할인금액(EUR)", "프로모션 내용"]
for col_idx, h in enumerate(raw_headers, 1):
    c = ws2.cell(3, col_idx, h)
    c.font = font_th
    c.fill = fill_navy
    c.alignment = align_center

raw_data = [
    ["2026-09-29", "LG", 55, "LG OLED 55B6", "OLED55B65LA", 1001.33, 1499.90, 498.57, "온라인 특가 할인"],
    ["2026-09-29", "LG", 55, "LG OLED 55B6", "OLED55B6ELC", 1499.00, 1499.00, 0.00, "None"],
    ["2026-09-29", "LG", 55, "LG OLED 55C6", "OLED55C66", 1596.00, 1596.00, 0.00, "None"],
    ["2026-09-29", "LG", 55, "LG OLED 55G6", "OLED55G66LS", 1799.00, 2199.00, 400.00, "Cashback: €200"],
    ["2026-09-29", "LG", 55, "LG OLED 55C6", "OLED55C65LA", 1899.00, 1899.00, 0.00, "Cashback: €150"],
    ["2026-09-29", "LG", 55, "LG OLED 55G6", "OLED55G68LW", 1930.95, 2367.00, 436.05, "None"],
    ["2026-09-29", "LG", 55, "LG OLED 55G6", "OLED55G64LW", 2199.00, 2199.00, 0.00, "None"],
    ["2026-09-29", "SAMSUNG", 55, "Sam OLED 55S90", "TQ55S90HAEXXC", 1299.00, 1999.00, 700.00, "Instant Rebate: -35% (Back to School)"],
    ["2026-09-29", "SAMSUNG", 55, "Sam OLED 55S85", "TQ55S83HAEXXC", 1799.00, 1799.00, 0.00, "Cashback: €200"],
    ["2026-09-29", "SAMSUNG", 55, "Sam OLED 55S95", "TQ55S95HFTXXC", 2299.00, 2299.00, 0.00, "None"],
    ["2026-09-29", "SAMSUNG", 55, "Sam OLED 55S99", "TQ55S99HATXXC", 2499.00, 2499.00, 0.00, "Cashback: €200"],
    ["2026-09-29", "LG", 65, "LG OLED 65B6", "OLED65B6ELC", 1146.65, 1349.00, 202.35, "None"],
    ["2026-09-29", "LG", 65, "LG OLED 65C6", "OLED65C65LA", 1729.00, 2699.00, 970.00, "Cashback: €200; Instant Rebate: -35%"],
    ["2026-09-29", "LG", 65, "LG OLED 65M", "OLED65M59LA", 2099.00, 2999.00, 900.00, "Cashback: €400; Instant Rebate: -30%"],
    ["2026-09-29", "LG", 65, "LG OLED 65G6", "OLED65G64LW", 2199.00, 2799.00, 600.00, "Cashback: €300"],
    ["2026-09-29", "LG", 65, "LG OLED 65C6", "OLED65C66", 2212.90, 2779.00, 566.10, "None"],
    ["2026-09-29", "LG", 65, "LG OLED 65G6", "OLED65G66LS", 2228.90, 2228.90, 0.00, "None"],
    ["2026-09-29", "LG", 65, "LG OLED 65G(Old)", "OLED65G54LW", 2309.00, 2309.00, 0.00, "None"],
    ["2026-09-29", "SAMSUNG", 65, "Sam OLED 65S99", "TQ65S99HATXXC", 2299.00, 3699.00, 1400.00, "Cashback: €200; Instant Rebate: -37%"],
    ["2026-09-29", "SAMSUNG", 65, "Sam OLED 65S90", "TQ65S90HAEXXC", 2599.00, 2599.00, 0.00, "Cashback: €300"],
    ["2026-09-29", "SAMSUNG", 65, "Sam OLED 65S95", "TQ65S95HFTXXC", 3499.00, 3499.00, 0.00, "Cashback: €300"]
]

for r_idx, r_val in enumerate(raw_data, 4):
    for c_idx, val in enumerate(r_val, 1):
        cell = ws2.cell(r_idx, c_idx, val)
        cell.font = font_data
        cell.border = border_cell
        if c_idx in [1, 2, 3, 4]:
            cell.alignment = align_center
        elif c_idx == 5:
            cell.alignment = align_left
        elif c_idx in [6, 7, 8]:
            cell.alignment = align_right
            cell.font = font_num
            cell.number_format = "#,##0.00"
        elif c_idx == 9:
            cell.alignment = align_left

for col in ws2.columns:
    max_len = 0
    col_letter = get_column_letter(col[0].column)
    for cell in col:
        if cell.row < 3: continue
        max_len = max(max_len, len(str(cell.value or "")))
    ws2.column_dimensions[col_letter].width = max(max_len + 3, 12)

excel_save_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\99. Master Agent\스페인_MediaMarkt_55_65_OLED_최저가_PriceGap_ATA비교.xlsx"
wb.save(excel_save_path)
print("Excel generated successfully at:", excel_save_path)
