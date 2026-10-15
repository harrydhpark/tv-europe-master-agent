# -*- coding: utf-8 -*-
"""
generate_swiss_word_report.py
Generates an Executive Word Report (.docx) for LGE Leadership:
'스위스 법인 TV 손익 심층 분석 및 4P 혁신 개선 과제 (2024~2026.08 YTD)'
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border_left(cell, color_hex="A50034", sz="24"):
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), sz)
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), color_hex)
    tcBorders.append(left)
    for b in ['top', 'bottom', 'right']:
        nb = OxmlElement(f'w:{b}')
        nb.set(qn('w:val'), 'none')
        tcBorders.append(nb)
    tcPr.append(tcBorders)

def add_callout_box(doc, text_list, title="핵심 시사점", border_color="A50034", bg_color="F8FAFC"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_border_left(cell, border_color, sz="28")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"■ {title}")
    run_title.bold = True
    run_title.font.size = Pt(10.5)
    r_color = RGBColor(int(border_color[:2], 16), int(border_color[2:4], 16), int(border_color[4:], 16))
    run_title.font.color.rgb = r_color
    run_title.font.name = "Malgun Gothic"
    
    for line in text_list:
        p_sub = cell.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(2)
        p_sub.paragraph_format.space_after = Pt(2)
        p_sub.paragraph_format.line_spacing = 1.2
        run = p_sub.add_run(line)
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        run.font.name = "Malgun Gothic"

def create_report():
    doc = Document()
    
    # Page setup - A4, 1 inch margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.88)
        section.right_margin = Inches(0.88)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("LG Electronics Europe • TV Sales Management • Swiss Branch P&L & 4P Strategy")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        hrun.font.name = "Malgun Gothic"
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("대외비 (Confidential) - 사내 한정 배포")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)
        frun.font.name = "Malgun Gothic"

    # Title Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    run_tag = title_p.add_run("[경영진 전략 보고]\n")
    run_tag.bold = True
    run_tag.font.size = Pt(11)
    run_tag.font.color.rgb = RGBColor(165, 0, 52) # LGE Crimson
    run_tag.font.name = "Malgun Gothic"
    
    run_title = title_p.add_run("스위스 법인 TV 손익(P&L) 심층 분석 및\n4P 관점의 수익성 혁신 개선 과제")
    run_title.bold = True
    run_title.font.size = Pt(20)
    run_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    run_title.font.name = "Malgun Gothic"

    # Metadata sub-bar
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_before = Pt(2)
    meta_p.paragraph_format.space_after = Pt(16)
    meta_run = meta_p.add_run("• 보고 대상: TV 유럽영업담당 및 경영진   |   • 분석 기간: 2024년 ~ 2026년 8월 누적 (Jan-Aug YTD 동기 비교)\n• 회계 기준: Standard P&L (공식 결산 실적)   |   • 작성 부서: TV 유럽영업 AX 추진 태스크")
    meta_run.font.size = Pt(9)
    meta_run.font.color.rgb = RGBColor(100, 116, 139)
    meta_run.font.name = "Malgun Gothic"

    # Divider line
    div_p = doc.add_paragraph()
    div_p.paragraph_format.space_before = Pt(0)
    div_p.paragraph_format.space_after = Pt(14)
    div_run = div_p.add_run("━" * 58)
    div_run.font.size = Pt(9)
    div_run.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # 1. Executive Summary
    # -------------------------------------------------------------
    h1 = doc.add_heading(level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    h1_run = h1.add_run("1. 경영진 핵심 요약 (Executive Summary)")
    h1_run.bold = True
    h1_run.font.size = Pt(14)
    h1_run.font.color.rgb = RGBColor(165, 0, 52)
    h1_run.font.name = "Malgun Gothic"

    p_exec = doc.add_paragraph()
    p_exec.paragraph_format.line_spacing = 1.3
    p_exec.paragraph_format.space_after = Pt(8)
    r = p_exec.add_run(
        "스위스 법인(Swiss Branch) TV 사업은 2024년 영업이익률 2.27%($711K)의 저수익 국면에서 2025년 10.91%($3,675K), "
        "2026년 8월 누적 기준 13.78%($4,972K)로 3개년 만에 7배에 달하는 비약적인 영업이익 성장을 달성하며 유럽 내 최고 수준의 고수익 거점으로 부상했습니다. "
        "그러나 장부상 호실적의 이면을 정밀 분해한 결과, 구조적 마진 침하와 채널 왜곡이 심화되는 중대한 리스크가 포착되었습니다."
    )
    r.font.size = Pt(10)
    r.font.name = "Malgun Gothic"

    # Callout Box: 2 Major Strategic Risks
    add_callout_box(
        doc,
        [
            "1. 원가 절감 의존 마진 방어의 한계: '26년 영업이익 증가분(+$1,297K) 중 변동원가 절감 효과가 +$1,615K로 이익 성장을 전담했습니다. 반면 순수 판가 효과(Price Effect)는 -$653K로 훼손되었으며 출하 ASP도 $893.2에서 $874.8로 -$18.3 하락했습니다. 향후 원가 절감 여력이 소진될 경우 판가 침하가 이익률 급락으로 직결될 위험이 상존합니다.",
            "2. 대형 양판 유통(MSH / FUST) 적자 고착화: 매출 2위 유통인 MSH(MediaMarkt, 비중 18.5%)는 매출차감률(S/D%)이 38.0%에 달해 COI -6.5%(-$430K 적자)를 기록하고 있으며, FUST(비중 6.5%) 역시 S/D% 38.3%, COI -4.3%(-$100K 적자)로 만성 적자 상태입니다. 단 2개 채널에서만 8개월간 -$530K의 마진 누수가 발생하여 Alltron, EP 등 전문 총판이 벌어들인 고수익을 갉아먹고 있습니다."
        ],
        title="경영진 주목 핵심 리스크 (Key Strategic Alerts)",
        border_color="A50034",
        bg_color="FFF5F5"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # 2. 3-Year P&L Performance Analysis
    # -------------------------------------------------------------
    h2 = doc.add_heading(level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    h2_run = h2.add_run("2. 3개년(2024~2026.08) 누적 손익 실적 비교 및 분해")
    h2_run.bold = True
    h2_run.font.size = Pt(14)
    h2_run.font.color.rgb = RGBColor(165, 0, 52)
    h2_run.font.name = "Malgun Gothic"

    # Subheading 2.1
    h2_1 = doc.add_heading(level=2)
    h2_1.paragraph_format.space_before = Pt(6)
    h2_1.paragraph_format.space_after = Pt(4)
    r = h2_1.add_run("2.1 표준 손익계산서 비교 (Standard P&L Summary)")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    r.font.name = "Malgun Gothic"

    # P&L Table
    pnl_rows = [
        ["손익 계정 항목", "2024년 1~8월", "2025년 1~8월", "2026년 1~8월", "YoY 증감 ('26 vs '25)", "2개년 증감 ('26 vs '24)"],
        ["판매 수량 (Qty, 대)", "41,510", "37,697", "41,239", "+3,542 (+9.4%)", "-271 (-0.7%)"],
        ["Gross Sales (총매출)", "$42,278K", "$44,332K", "$47,425K", "+$3,093K (+7.0%)", "+$5,147K (+12.2%)"],
        ["(-) Sales Deduction (할인/공제)", "$11,005K", "$10,662K", "$11,348K", "+$686K (+6.4%)", "+$343K (+3.1%)"],
        ["    └ 매출차감률 (S/D%)", "26.03%", "24.05%", "23.93%", "-0.12%p 개선", "-2.10%p 개선"],
        ["Net Sales (순매출액)", "$31,273K", "$33,670K", "$36,077K", "+$2,407K (+7.1%)", "+$4,804K (+15.4%)"],
        ["출하 단가 (ASP, $)", "$753.4", "$893.2", "$874.8", "-$18.3 (-2.1%)", "+$121.5 (+16.1%)"],
        ["(-) 재료비 (Material Cost)", "$20,225K (64.7%)", "$19,375K (57.5%)", "$20,368K (56.5%)", "-1.08%p 개선", "-8.21%p 개선"],
        ["(-) COGS (매출원가 합계)", "$22,096K (70.7%)", "$21,204K (63.0%)", "$20,922K (58.0%)", "-4.99%p 개선", "-12.67%p 개선"],
        ["Marginal Profit (한계이익, MP)", "$9,409K (30.1%)", "$12,656K (37.6%)", "$14,354K (39.8%)", "+$1,698K (+2.2%p)", "+$4,945K (+9.7%p)"],
        ["(-) SG&A (판관비 합계)", "$8,466K (27.1%)", "$8,791K (26.1%)", "$10,183K (28.2%)", "+$1,392K (+2.1%p)", "+$1,717K (+1.1%p)"],
        ["Operating Income (영업이익, COI)", "$711K", "$3,675K", "$4,972K", "+$1,297K (+35.3%)", "+$4,261K (7.0배)"],
        ["    └ 영업이익률 (COI%)", "2.27%", "10.91%", "13.78%", "+2.87%p 상승", "+11.51%p 상승"]
    ]

    tbl = doc.add_table(rows=len(pnl_rows), cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    col_widths = [Inches(2.2), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.2), Inches(1.2)]
    for r_idx, row in enumerate(pnl_rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            run = p.add_run(val)
            run.font.name = "Malgun Gothic"
            
            # Formatting styles
            if r_idx == 0:
                set_cell_background(cell, "A50034") # Header Crimson
                run.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx in [5, 9, 11, 12]: # Key totals (Net Sales, MP, COI, COI%)
                set_cell_background(cell, "F1F5F9" if r_idx != 12 else "ECFDF5")
                run.bold = True
                run.font.size = Pt(8.5)
                if r_idx == 12:
                    run.font.color.rgb = RGBColor(5, 150, 105) # Emerald
                elif r_idx == 11:
                    run.font.color.rgb = RGBColor(165, 0, 52)
                else:
                    run.font.color.rgb = RGBColor(15, 23, 42)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Subheading 2.2: Waterfall Bridge
    h2_2 = doc.add_heading(level=2)
    h2_2.paragraph_format.space_before = Pt(6)
    h2_2.paragraph_format.space_after = Pt(4)
    r = h2_2.add_run("2.2 YoY 영업이익 변동 요인 Waterfall Bridge ('25년 누적 vs '26년 누적)")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    r.font.name = "Malgun Gothic"

    wf_text = doc.add_paragraph()
    wf_text.paragraph_format.line_spacing = 1.3
    wf_text.paragraph_format.space_after = Pt(6)
    r = wf_text.add_run(
        "2025년 8월 누적 영업이익 $3,675K에서 2026년 $4,972K로의 +$1,297K 증가 요인을 브릿지 분석한 결과는 다음과 같습니다:\n"
        "• 2025년 8월 누적 영업이익 기저: $3,674.7K\n"
        "  [+] 판매량 효과 (Volume Effect): +$345.3K (수량 37.7K대 → 41.2K대로 +9.4% 증가 기여)\n"
        "  [-] 순수 판가 효과 (Price Effect): -$653.5K (OLED/QNED 출하 단가 침하에 따른 직접 마진 훼손)\n"
        "  [+] 매출차감률 개선 (S/D Effect): +$213.4K (전체 S/D% 24.05% → 23.93%로 -0.12%p 축소 효과)\n"
        "  [+] 변동 제조원가 절감 (Var COGS Effect): +$1,614.6K (패널가 및 재료비 개선의 압도적 마진 방어)\n"
        "  [-] 고정비/기타 경비 증가 (Fixed O/H Effect): -$400.5K (물류비 및 고정 판매관리비 증가 부담)\n"
        "  [+] 결산 보정/기타 Gap: +$178.1K\n"
        "• 2026년 8월 누적 영업이익 달성액: $4,972.2K (최종 +$1,297.5K 성장)"
    )
    r.font.size = Pt(9.5)
    r.font.name = "Malgun Gothic"

    # -------------------------------------------------------------
    # 3. 4P Diagnostic Breakdown
    # -------------------------------------------------------------
    h3 = doc.add_heading(level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    h3_run = h3.add_run("3. 4P 영역별 심층 데이터 진단 (Data-driven 4P Diagnostics)")
    h3_run.bold = True
    h3_run.font.size = Pt(14)
    h3_run.font.color.rgb = RGBColor(165, 0, 52)
    h3_run.font.name = "Malgun Gothic"

    # 3.1 Product
    h3_1 = doc.add_heading(level=2)
    h3_1.paragraph_format.space_before = Pt(4)
    h3_1.paragraph_format.space_after = Pt(4)
    r = h3_1.add_run("3.1 [Product] 제품 세그먼트별 실적 및 인치대별 믹스 진단")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    r.font.name = "Malgun Gothic"

    prod_rows = [
        ["세그먼트", "2024 수량", "2025 수량", "2026 수량", "2026 매출", "매출 비중", "2026 ASP", "2026 S/D%", "2026 COI% (금액)"],
        ["OLED", "17,930대", "18,443대", "20,940대", "$24.10M", "66.8%", "$1,150.8", "24.4%", "9.4% ($2,272K)"],
        ["QNED", "4,162대", "7,536대", "9,695대", "$5.63M", "15.6%", "$580.9", "26.2%", "7.7% ($436K)"],
        ["MRGB (신규)", "-", "-", "647대", "$0.58M", "1.6%", "$890.2", "22.5%", "17.9% ($103K)"],
        ["UHD (엔트리)", "17,207대", "10,003대", "7,709대", "$3.79M", "10.5%", "$491.2", "17.6%", "11.6% ($441K)"],
        ["FHD", "2,211대", "1,715대", "2,248대", "$0.97M", "2.7%", "$430.0", "22.3%", "3.2% ($31K)"],
        ["Others(정산)", "-", "-", "-", "$1.02M", "2.8%", "-", "-", "- ($1,690K)"]
    ]

    tbl_prod = doc.add_table(rows=len(prod_rows), cols=9)
    tbl_prod.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_prod.autofit = False
    p_widths = [Inches(1.2), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.9), Inches(0.7), Inches(0.8), Inches(0.8), Inches(1.2)]
    
    for r_idx, row in enumerate(prod_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_prod.cell(r_idx, c_idx)
            cell.width = p_widths[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(val)
            run.font.name = "Malgun Gothic"
            if r_idx == 0:
                set_cell_background(cell, "334155")
                run.bold = True
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.size = Pt(7.5)
                if r_idx == 1: # OLED
                    set_cell_background(cell, "FAF5FF")
                    run.bold = True if c_idx in [0, 4, 8] else False
                elif r_idx == 3: # MRGB
                    set_cell_background(cell, "ECFDF5")
                    run.bold = True if c_idx in [0, 8] else False
                else:
                    if r_idx % 2 == 1:
                        set_cell_background(cell, "F8FAFC")

    p_p_comm = doc.add_paragraph()
    p_p_comm.paragraph_format.line_spacing = 1.25
    p_p_comm.paragraph_format.space_before = Pt(4)
    p_p_comm.paragraph_format.space_after = Pt(8)
    r = p_p_comm.add_run(
        "• 진단 시사점: OLED는 지점 매출의 66.8%와 영업이익의 46%를 견인하는 핵심 기둥이나, 55형 이하 볼륨 확대로 ASP가 전년 $1,227에서 $1,151로 하락했습니다. "
        "QNED는 9.7K대로 수량이 급증했으나 ASP $581, S/D% 26.2%로 엔트리급 과다 프로모션이 전개되었습니다. "
        "반면 2026년 런칭한 MRGB는 647대 판매, COI% 17.9%로 초고수익 모델로서의 확장 가능성을 입증했습니다."
    )
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(71, 85, 105)
    r.font.name = "Malgun Gothic"

    # 3.2 Place & Promotion: Account Scorecard
    h3_2 = doc.add_heading(level=2)
    h3_2.paragraph_format.space_before = Pt(6)
    h3_2.paragraph_format.space_after = Pt(4)
    r = h3_2.add_run("3.2 [Place & Promotion] 주요 유통 거래선별 손익 성적표 및 리베이트 편차")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    r.font.name = "Malgun Gothic"

    acc_rows = [
        ["유통 거래선", "채널 유형", "2026 판매량", "매출액 (Net)", "매출 비중", "출하 ASP", "S/D% (할인율)", "한계이익률 (MP%)", "영업이익률 (COI%)", "영업이익 금액", "진단 등급"],
        ["Conforama", "대형 양판", "13,124대", "$8,681K", "24.1%", "$662", "21.6%", "38.9%", "12.9%", "+$1,122K", "우량 볼륨"],
        ["MSH (MediaMarkt)", "대형 가전", "8,722대", "$6,657K", "18.5%", "$763", "38.0%", "26.2%", "-6.5%", "-$430K", "심각 적자"],
        ["Alltron", "전문 총판", "4,416대", "$5,136K", "14.2%", "$1,163", "4.0%", "46.5%", "26.3%", "+$1,351K", "최고 효자"],
        ["EP", "전문점", "3,981대", "$4,885K", "13.5%", "$1,227", "5.9%", "44.7%", "23.8%", "+$1,163K", "최고 효자"],
        ["Online (자사몰)", "D2C 온라인", "2,999대", "$3,428K", "9.5%", "$1,143", "21.8%", "41.3%", "15.4%", "+$527K", "고수익 D2C"],
        ["Interdiscount", "전자 양판", "3,375대", "$2,670K", "7.4%", "$791", "32.9%", "33.4%", "2.8%", "+$74K", "저마진 경계"],
        ["FUST", "주방/가전", "3,228대", "$2,343K", "6.5%", "$726", "38.3%", "28.8%", "-4.3%", "-$100K", "만성 적자"]
    ]

    tbl_acc = doc.add_table(rows=len(acc_rows), cols=11)
    tbl_acc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_acc.autofit = False
    a_widths = [Inches(1.3), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8), Inches(0.7)]

    for r_idx, row in enumerate(acc_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_acc.cell(r_idx, c_idx)
            cell.width = a_widths[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx < 2 else (WD_ALIGN_PARAGRAPH.CENTER if c_idx == 10 else WD_ALIGN_PARAGRAPH.RIGHT)
            run = p.add_run(val)
            run.font.name = "Malgun Gothic"
            if r_idx == 0:
                set_cell_background(cell, "334155")
                run.bold = True
                run.font.size = Pt(7.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.size = Pt(7)
                if r_idx in [2, 7]: # MSH, FUST (Red Alert)
                    set_cell_background(cell, "FEF2F2")
                    run.bold = True if c_idx in [0, 6, 8, 9, 10] else False
                    if c_idx in [6, 8, 9]:
                        run.font.color.rgb = RGBColor(220, 38, 38)
                elif r_idx in [3, 4]: # Alltron, EP (Emerald Stars)
                    set_cell_background(cell, "ECFDF5")
                    run.bold = True if c_idx in [0, 6, 8, 9, 10] else False
                    if c_idx in [6, 8, 9]:
                        run.font.color.rgb = RGBColor(5, 150, 105)
                else:
                    if r_idx % 2 == 1:
                        set_cell_background(cell, "F8FAFC")

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------
    # 4. 4P Strategic Roadmap & Action Items
    # -------------------------------------------------------------
    h4 = doc.add_heading(level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)
    h4_run = h4.add_run("4. 4P 혁신 개선 과제 및 실행 로드맵 (Strategic Action Plan)")
    h4_run.bold = True
    h4_run.font.size = Pt(14)
    h4_run.font.color.rgb = RGBColor(165, 0, 52)
    h4_run.font.name = "Malgun Gothic"

    roadmap_items = [
        ("PRODUCT (제품 믹스 고도화)", "OLED 초대형 프리미엄 고착화 & QNED 라인업 재정립", [
            "1. OLED 65형 이상 및 C/G 시리즈 믹스 비중 50% 이상 확대: 인치당 판가 방어 및 프리미엄 사운드바 번들링 판촉 집중.",
            "2. QNED 미니LED 중심 고수익 포지셔닝 전환: 저가 QNED80 공급 쿼터를 축소하고 고마진 QNED85/90 마케팅 펀드 신설.",
            "3. MRGB / 라이프스타일 전시 120개점 확대: 스위스 고소득 인테리어 수요층 공략 (StanbyME, Posé, Easel 등 고수익 라인업 전진 배치)."
        ]),
        ("PRICE (가격 방어력 확립)", "판가 하한선(Floor Price) 가이드라인 엄격 통제", [
            "1. MAP (Minimum Advertised Price) 제도 의무화: 온라인 최저가 덤핑 유통에 대해 마케팅 지원금 자동 유예 페널티 시행.",
            "2. 본사 원가 절감분의 판가 인하 전이 차단: 절감 마진을 법인 영업이익 유보금으로 확보하는 가격 승인 프로세스 구축.",
            "3. 채널별 전용 파생 모델(Derivation) 분리: 대형 양판점(MSH/Conforama)과 전문 총판(Alltron/EP) 스펙 이원화로 가격 비교 방지."
        ]),
        ("PLACE (유통 채널 정상화)", "적자 유통(MSH / FUST) 정상화 및 고수익 총판 공급 우선권", [
            "1. MSH / FUST 비상 수익성 개선 TF 가동: S/D 상한선(Cap) 28% 강제 제한 및 COI +2% 미달 모델 출하 즉각 중단.",
            "2. Alltron / EP 고수익 총판 우대 인센티브: 신제품 2~4주 독점 선공급권 부여 및 분기 목표 달성 성과급(Rebate 2%) 지급.",
            "3. 자사몰(Online D2C) 매출 비중 15% 확대: 전용 설치 및 보증 3년 번들 프로모션을 통해 유통 마진 누수 없는 채널 육성."
        ]),
        ("PROMOTION (판촉 효율 극대화)", "Sell-In 일괄 리베이트 축소 및 실판매(Sell-Out) 연동형 전환", [
            "1. 관행적 Sell-In 기본 리베이트(Trade Term) 2~3%p 삭감: 입점 조건 일괄 보조금을 축소하여 유통 밀어넣기(Push) 차단.",
            "2. 최종 소비자 직접 캐시백 캠페인: 유통 마진 잠식 방지를 위한 '스위스 전국 OLED 캐시백(CHF 200~500)' 직접 환급 캠페인 전환.",
            "3. 유통 Co-Op 광고비 전수 감사 및 회수: 전단/배너 게재 내역 전수 검증 및 ROI 기준 미달 시 차기 지원금 즉시 삭감."
        ])
    ]

    for p_label, p_title, sub_tasks in roadmap_items:
        h4_sub = doc.add_heading(level=2)
        h4_sub.paragraph_format.space_before = Pt(8)
        h4_sub.paragraph_format.space_after = Pt(3)
        r = h4_sub.add_run(f"■ {p_label}: {p_title}")
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(165, 0, 52)
        r.font.name = "Malgun Gothic"

        for task in sub_tasks:
            tp = doc.add_paragraph()
            tp.paragraph_format.space_before = Pt(1)
            tp.paragraph_format.space_after = Pt(2)
            tp.paragraph_format.line_spacing = 1.2
            trun = tp.add_run(task)
            trun.font.size = Pt(9.5)
            trun.font.name = "Malgun Gothic"

    # -------------------------------------------------------------
    # 5. Financial Simulation & Milestones
    # -------------------------------------------------------------
    h5 = doc.add_heading(level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)
    h5_run = h5.add_run("5. 재무적 기대 효과 및 단계별 실행 마일스톤")
    h5_run.bold = True
    h5_run.font.size = Pt(14)
    h5_run.font.color.rgb = RGBColor(165, 0, 52)
    h5_run.font.name = "Malgun Gothic"

    sim_p = doc.add_paragraph()
    sim_p.paragraph_format.line_spacing = 1.3
    sim_p.paragraph_format.space_after = Pt(6)
    r = sim_p.add_run(
        "상기 4P 과제 실행 시 기대되는 재무적 성과는 다음과 같이 산출됩니다:\n"
        "• MSH S/D% 정상화 (38.0% → 28.0% 감축): 연간 +$1,073K 이익 개선 (흑자 전환 COI +3.5%)\n"
        "• FUST S/D% 정상화 (38.3% → 28.0% 감축): 연간 +$391K 이익 개선 (흑자 전환 COI +5.2%)\n"
        "• QNED S/D% 정상화 (26.2% → 20.5% 감축): 연간 +$321K 이익 개선\n"
        "▶ 전사 합산 영업이익 개선 효과: 연간 +$1,785K (스위스 법인 영업이익률 13.78% → 17.15% 도약)"
    )
    r.font.size = Pt(9.5)
    r.font.name = "Malgun Gothic"

    # Milestones table
    mile_rows = [
        ["추진 단계", "시기", "핵심 실행 목표", "세부 조치 내용"],
        ["Phase 1", "'26. 10월", "MSH/FUST 거래 조건 재협상", "S/D 상한선(28%) 통보, 최저 출하가 가이드라인 공표 및 Black Friday 가이드라인 합의"],
        ["Phase 2", "'26. 11~12월", "성수기 Sell-Out 프로모션 전개", "OLED 초대형 스위스 전국 소비자 캐시백 가동, Alltron/EP 독점 모델 집중 판촉"],
        ["Phase 3", "'27. 1분기", "2027년 신모델 라인업/가격 재편", "Y27 신모델 채널 전용 파생 모델 체계 안착, QNED 미니LED 비중 확대, MRGB 매장 120점 확대"],
        ["Phase 4", "'27. 상반기", "COI 15% 이상 상시 고수익 정착", "스위스 법인 연간 매출 $55M+, COI% 15.0% 이상 상시 달성, 자사몰 비중 15% 돌파"]
    ]

    tbl_m = doc.add_table(rows=len(mile_rows), cols=4)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_m.autofit = False
    m_widths = [Inches(1.1), Inches(1.1), Inches(2.1), Inches(2.2)]

    for r_idx, row in enumerate(mile_rows):
        for c_idx, val in enumerate(row):
            cell = tbl_m.cell(r_idx, c_idx)
            cell.width = m_widths[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx < 2 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Malgun Gothic"
            if r_idx == 0:
                set_cell_background(cell, "A50034")
                run.bold = True
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.size = Pt(8)
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")

    # Output path
    output_docx_path = os.path.join(
        r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis\법인별\05. Swiss",
        "스위스_TV_손익분석_및_4P_개선과제_경영진보고서.docx"
    )
    print(f"Saving Word report to {output_docx_path}...")
    doc.save(output_docx_path)
    print("Word report generated successfully!")

if __name__ == "__main__":
    create_report()
