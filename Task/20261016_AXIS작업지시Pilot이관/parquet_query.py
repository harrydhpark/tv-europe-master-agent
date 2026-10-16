# -*- coding: utf-8 -*-
"""
Parquet 라이브 쿼리 엔진 (watch_bridge.js에서 호출)
범용 P&L 데이터 쿼리: 세그먼트별, 거래선별, 모델별, 월별 손익 집계

Usage:
  python parquet_query.py --sub SWISS --year 2026 --period YTD
  python parquet_query.py --sub SWISS --year 2026 --period YTD --segment MRGB
  python parquet_query.py --sub SWISS --year 2026 --period YTD --segment MRGB --groupby account
  python parquet_query.py --sub SWISS --year 2026 --month 8 --groupby segment
  python parquet_query.py --sub AG --year 2026 --period YTD --groupby model --segment OLED --top 10
"""

import argparse
import json
import os
import sys
import pandas as pd
import numpy as np

# ── Subsidiary → P&L folder mapping ──
SUB_FOLDER_MAP = {
    'AG': '01. AG', 'BN': '02. BN', 'CK': '03. CK', 'DG': '04. DG',
    'SWISS': '05. Swiss', 'ES': '06. ES', 'FS': '07. FS', 'HS': '08. HS',
    'IS': '09. IS', 'LA': '10. LA', 'MK': '11. MK', 'PL': '12. PL',
    'PT': '13. PT', 'RO': '14. RO', 'SW': '15. SW', 'UK': '16. UK',
    'RA': '17. RA', 'AK': '18. AK', 'UR': '19. UR'
}

SUB_NAMES = {
    'AG': '오스트리아 (LGEAG)', 'BN': '베네룩스 (LGEBN)', 'CK': '체코/슬로바키아 (LGECK)',
    'DG': '독일 (LGEDG)', 'SWISS': '스위스 (Swiss)', 'ES': '스페인 (LGEES)',
    'FS': '프랑스 (LGEFS)', 'HS': '그리스 (LGEHS)', 'IS': '이탈리아 (LGEIS)',
    'LA': '발틱 (LGELA)', 'MK': '헝가리 (LGEMK)', 'PL': '폴란드 (LGEPL)',
    'PT': '포르투갈 (LGEPT)', 'RO': '루마니아 (LGERO)', 'SW': '스웨덴/노르딕 (LGESW)',
    'UK': '영국 (LGEUK)', 'RA': '러시아 (LGERA)', 'AK': '카자흐스탄 (LGEAK)',
    'UR': '우크라이나 (LGEUR)'
}

# P&L base directory (relative to this script's parent: 99. Master Agent)
PNL_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '05. TV P&L Analysis', '법인별'))


def find_parquet(sub_code):
    """Find raw_data.parquet for given subsidiary, or auto-build using DataEngineer if missing."""
    folder = SUB_FOLDER_MAP.get(sub_code.upper())
    if not folder:
        return None
    folder_path = os.path.join(PNL_BASE, folder)
    parquet_path = os.path.join(folder_path, 'cache', 'raw_data.parquet')
    if os.path.exists(parquet_path):
        return parquet_path

    # Auto-build cache via DataEngineer if XLSB source exists
    try:
        pnl_root = os.path.abspath(os.path.join(PNL_BASE, '..'))
        if pnl_root not in sys.path:
            sys.path.insert(0, pnl_root)
        from core.data_engineer import DataEngineer
        print(f"[ParquetQuery] Building Parquet cache for {sub_code} from XLSB source...", file=sys.stderr)
        engineer = DataEngineer(folder_path, sub_code)
        engineer.load_data()
        if os.path.exists(parquet_path):
            print(f"[ParquetQuery] Successfully built and cached Parquet for {sub_code}!", file=sys.stderr)
            return parquet_path
    except Exception as e:
        print(f"[ParquetQuery] Failed auto-building parquet for {sub_code}: {e}", file=sys.stderr)

    return None


def safe_div(a, b):
    """Safe division returning 0 for zero divisor."""
    return float(a / b) if b != 0 else 0.0


def aggregate_group(group_df):
    """Aggregate P&L metrics for a group of rows."""
    qty = int(group_df['Sales Qty'].sum())
    gross = float(group_df['Gross Sales'].sum())
    sd = float(group_df['Sales Deduction'].sum())
    net_sales = float(group_df['Net Sales'].sum())
    mp = float(group_df['Marginal Profit'].sum())
    coi = float(group_df['Operating Income'].sum())
    material = float(group_df['Material Cost'].sum()) if 'Material Cost' in group_df.columns else 0
    cogs = float(group_df['COGS'].sum()) if 'COGS' in group_df.columns else 0

    return {
        'qty': qty,
        'gross_sales': round(gross, 1),
        'sales_deduction': round(sd, 1),
        'net_sales': round(net_sales, 1),
        'marginal_profit': round(mp, 1),
        'operating_income': round(coi, 1),
        'material_cost': round(material, 1),
        'cogs': round(cogs, 1),
        'sd_pct': round(safe_div(abs(sd), gross) * 100, 2),
        'mp_pct': round(safe_div(mp, net_sales) * 100, 2),
        'opm_pct': round(safe_div(coi, net_sales) * 100, 2),
        'cogs_pct': round(safe_div(cogs, net_sales) * 100, 2),
    }


def run_query(args):
    sub_code = args.sub.upper()
    parquet_path = find_parquet(sub_code)

    if not parquet_path:
        return {
            'success': False,
            'error': f'Parquet 캐시 파일이 없습니다: {sub_code} ({SUB_FOLDER_MAP.get(sub_code, "unknown")})',
            'subsidiary': sub_code
        }

    df = pd.read_parquet(parquet_path)

    # ── Filter by year ──
    year = args.year or int(df['Year'].max())
    df_year = df[df['Year'] == year].copy()
    df_filtered = df_year.copy()

    # ── Filter by period ──
    latest_month = int(df_year['Month'].max()) if len(df_year) > 0 else 8
    requested_month = args.month
    actual_month = args.month
    if args.month:
        df_month = df_filtered[df_filtered['Month'] == args.month]
        if len(df_month) > 0:
            df_filtered = df_month
            period_label = f'{year}년 {args.month}월'
        else:
            actual_month = latest_month
            df_filtered = df_filtered[df_filtered['Month'] == latest_month]
            period_label = f'{year}년 {latest_month}월 최신 결산 기준 (요청: {args.month}월)'
    elif args.period == 'YTD':
        period_label = f'{year}년 누적 (1~{latest_month}월 YTD)'
    elif args.period == 'L3M':
        start_month = max(1, latest_month - 2)
        df_filtered = df_filtered[df_filtered['Month'] >= start_month]
        period_label = f'{year}년 최근 3개월 ({start_month}~{latest_month}월)'
    elif args.period == 'L6M':
        start_month = max(1, latest_month - 5)
        df_filtered = df_filtered[df_filtered['Month'] >= start_month]
        period_label = f'{year}년 최근 6개월 ({start_month}~{latest_month}월)'
    elif args.period == 'MTD':
        df_filtered = df_filtered[df_filtered['Month'] == latest_month]
        period_label = f'{year}년 {latest_month}월 (MTD)'
    else:
        period_label = f'{year}년 전체'

    # ── Filter by segment ──
    segment_filter = args.segment
    if segment_filter:
        seg_upper = segment_filter.upper()
        seg_map = {
            'OLED': 'OLED', 'QNED': 'QNED', 'MRGB': 'MRGB',
            'UHD': 'UHD', 'FHD': 'FHD', '올레드': 'OLED',
            'LCD': 'UHD', 'MINILED': 'MRGB', 'MICRO': 'MRGB',
            'OTHERS': 'Others'
        }
        actual_seg = seg_map.get(seg_upper, segment_filter)
        df_filtered = df_filtered[df_filtered['Segment'] == actual_seg]
        period_label += f' | 세그먼트: {actual_seg}'

    # ── Filter by account ──
    if args.account:
        df_filtered = df_filtered[df_filtered['Clean_Account'].str.contains(args.account, case=False, na=False)]
        period_label += f' | 거래선: {args.account}'

    if len(df_filtered) == 0:
        return {
            'success': True,
            'subsidiary': sub_code,
            'subsidiary_name': SUB_NAMES.get(sub_code, sub_code),
            'subsidiary_kr': SUB_NAMES.get(sub_code, sub_code),
            'period': period_label,
            'row_count': 0,
            'total': None,
            'breakdown': [],
            'message': '해당 조건에 맞는 데이터가 없습니다.'
        }

    # ── Calculate Total ──
    total = aggregate_group(df_filtered)
    total['label'] = '전체 합계 (Total)'

    # ── GroupBy breakdown ──
    breakdown = []
    groupby = args.groupby or 'segment'

    if groupby == 'segment':
        groups = df_filtered.groupby('Segment')
    elif groupby == 'account':
        groups = df_filtered.groupby('Clean_Account')
    elif groupby == 'model':
        groups = df_filtered.groupby('Model')
    elif groupby == 'series':
        groups = df_filtered.groupby('Series')
    elif groupby == 'inch':
        groups = df_filtered.groupby('Inch')
    elif groupby == 'month':
        groups = df_filtered.groupby('Month')
    else:
        groups = None

    if groups is not None:
        for name, grp in groups:
            row = aggregate_group(grp)
            lbl = str(name) if groupby != 'month' else f'{year}년 {int(name)}월'
            row['label'] = lbl
            row[groupby] = lbl
            row['qty_share_pct'] = round(safe_div(row['qty'], total['qty']) * 100, 1)
            row['share_pct'] = round(safe_div(row['net_sales'], total['net_sales']) * 100, 1)
            breakdown.append(row)

        breakdown.sort(key=lambda x: x['net_sales'], reverse=True)
        if args.top and args.top > 0:
            breakdown = breakdown[:args.top]

    # ── Top Accounts Breakdown (always include top 8 accounts for profitability reports) ──
    account_breakdown = []
    if 'Clean_Account' in df_filtered.columns:
        for acc_name, grp in df_filtered.groupby('Clean_Account'):
            arow = aggregate_group(grp)
            arow['label'] = str(acc_name)
            arow['account'] = str(acc_name)
            arow['qty_share_pct'] = round(safe_div(arow['qty'], total['qty']) * 100, 1)
            arow['share_pct'] = round(safe_div(arow['net_sales'], total['net_sales']) * 100, 1)
            account_breakdown.append(arow)
        account_breakdown.sort(key=lambda x: x['net_sales'], reverse=True)
        account_breakdown = account_breakdown[:8]

    # ── Monthly Trend across the full year (1..latest_month) ──
    monthly_trend = []
    for month_num, grp in df_year.groupby('Month'):
        m = aggregate_group(grp)
        m['month'] = int(month_num)
        m['label'] = f'{year}.{int(month_num):02d}'
        monthly_trend.append(m)
    monthly_trend.sort(key=lambda x: x['month'])

    # ── Available Segments & Accounts for context ──
    available_segments = sorted(df_filtered['Segment'].unique().tolist()) if 'Segment' in df_filtered.columns else []
    available_accounts = sorted(df_filtered['Clean_Account'].unique().tolist()) if 'Clean_Account' in df_filtered.columns else []

    result = {
        'success': True,
        'subsidiary': sub_code,
        'subsidiary_name': SUB_NAMES.get(sub_code, sub_code),
        'subsidiary_kr': SUB_NAMES.get(sub_code, sub_code),
        'period': period_label,
        'year': year,
        'latest_month': latest_month,
        'requested_month': requested_month,
        'actual_month': actual_month,
        'row_count': len(df_filtered),
        'total': total,
        'groupby': groupby,
        'filters': {
            'groupby': groupby,
            'month': actual_month,
            'requested_month': requested_month,
            'period': args.period
        },
        'breakdown': breakdown,
        'account_breakdown': account_breakdown,
        'monthly_trend': monthly_trend,
        'available_segments': available_segments,
        'available_accounts': available_accounts[:20],
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='Parquet P&L Live Query Engine')
    parser.add_argument('--sub', required=True, help='Subsidiary code (e.g., SWISS, AG, DG)')
    parser.add_argument('--year', type=int, default=None, help='Target year (default: latest)')
    parser.add_argument('--month', type=int, default=None, help='Target month (1-12)')
    parser.add_argument('--period', default='YTD', choices=['YTD', 'MTD', 'L3M', 'L6M'], help='Period filter')
    parser.add_argument('--segment', default=None, help='Segment filter (OLED, MRGB, QNED, UHD, FHD)')
    parser.add_argument('--account', default=None, help='Account/customer filter (partial match)')
    parser.add_argument('--groupby', default=None, choices=['segment', 'account', 'model', 'series', 'inch', 'month', 'none'], help='GroupBy dimension')
    parser.add_argument('--top', type=int, default=None, help='Top N results for groupby')

    args = parser.parse_args()
    result = run_query(args)

    # Output ASCII-safe JSON to stdout so Node.js JSON.parse works across all Windows codepages
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
