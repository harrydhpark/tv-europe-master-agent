# -*- coding: utf-8 -*-
"""
전 유럽 법인 NERP 원천 XLSB → raw_data.parquet & pnl_datamart.json 고속 일괄 빌더

Usage:
  python batch_build_parquet.py --tier 1
  python batch_build_parquet.py --tier 2
  python batch_build_parquet.py --tier 3
  python batch_build_parquet.py --all
  python batch_build_parquet.py --countries UK ES
"""

import os
import sys
import time
import argparse

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Base paths
MASTER_AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNL_ROOT_DIR = os.path.abspath(os.path.join(MASTER_AGENT_DIR, '..', '05. TV P&L Analysis'))
if PNL_ROOT_DIR not in sys.path:
    sys.path.insert(0, PNL_ROOT_DIR)

from core.data_engineer import DataEngineer
from core.config import SUBSIDIARY_REGISTRY, SUBSIDIARIES_DIR

TIERS = {
    1: ['UK', 'ES', 'BN', 'IS'],
    2: ['PT', 'MK', 'CK', 'HS'],
    3: ['SW', 'LA', 'PL', 'RO', 'RA']
}

def build_single_country(country_code, force_reload=False):
    """Build raw_data.parquet and pnl_datamart.json for a single subsidiary."""
    info = SUBSIDIARY_REGISTRY.get(country_code)
    if not info:
        print(f"❌ [SKIP] Unknown subsidiary code: {country_code}")
        return False, 0, 0, 0

    folder_name = info['folder']
    country_dir = os.path.join(SUBSIDIARIES_DIR, folder_name)
    name_kr = info.get('name_kr', country_code)

    print(f"\n{'='*70}")
    print(f"[START] Processing {name_kr} ({country_code}) in {folder_name}")
    print(f"{'='*70}")

    t_start = time.time()
    try:
        engineer = DataEngineer(country_dir, country_code)

        source_xlsb = engineer.find_source_xlsb()
        if not source_xlsb:
            print(f"[WARNING] No source XLSB found in {folder_name}. Skipping.")
            return False, 0, 0, 0

        xlsb_size_mb = os.path.getsize(source_xlsb) / (1024 * 1024)
        print(f"[SOURCE] {os.path.basename(source_xlsb)} ({xlsb_size_mb:.1f} MB)")

        # 1. Load data & cache to Parquet
        t0 = time.time()
        df = engineer.load_data(force_reload=force_reload)
        t_load = time.time() - t0
        row_count = len(df)
        parquet_size_mb = os.path.getsize(engineer.parquet_path) / (1024 * 1024) if os.path.exists(engineer.parquet_path) else 0

        print(f"[OK] [1/2] Parquet cached: {parquet_size_mb:.1f} MB ({row_count:,} rows) in {t_load:.1f}s")

        # 2. Build datamart JSON
        t1 = time.time()
        engineer.build_datamart(df)
        t_mart = time.time() - t1
        mart_size_kb = os.path.getsize(engineer.datamart_path) / 1024 if os.path.exists(engineer.datamart_path) else 0

        print(f"[OK] [2/2] Datamart JSON built: {mart_size_kb:.1f} KB in {t_mart:.1f}s")

        t_total = time.time() - t_start
        print(f"[COMPLETED] {name_kr} ({country_code}) finished in {t_total:.1f}s!")
        return True, row_count, parquet_size_mb, t_total

    except Exception as e:
        print(f"[ERROR] Failed processing {country_code}: {e}")
        import traceback
        traceback.print_exc()
        return False, 0, 0, 0

def main():
    parser = argparse.ArgumentParser(description="Batch Parquet & Datamart Builder")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], help="Execute specific tier (1: UK/ES/BN/IS, 2: PT/MK/CK/HS, 3: SW/LA/PL/RO/RA)")
    parser.add_argument("--all", action="store_true", help="Execute all 3 tiers sequentially")
    parser.add_argument("--countries", nargs="+", help="Explicit list of country codes (e.g. UK ES)")
    parser.add_argument("--force-reload", action="store_true", help="Force rebuild even if cache exists")

    args = parser.parse_args()

    targets = []
    if args.countries:
        targets = [c.upper() for c in args.countries]
    elif args.tier:
        targets = TIERS[args.tier]
    elif args.all:
        targets = TIERS[1] + TIERS[2] + TIERS[3]
    else:
        print("Defaulting to Tier 1: UK, ES, BN, IS")
        targets = TIERS[1]

    print(f"\n=======================================================")
    print(f"[QUEUE] Batch Parquet Build Queue: {len(targets)} subsidiaries")
    print(f"[TARGETS] {', '.join(targets)}")
    print(f"=======================================================")

    results = []
    t_batch_start = time.time()

    for idx, code in enumerate(targets, 1):
        print(f"\n>>> [{idx}/{len(targets)}] Starting {code}...")
        success, rows, size_mb, duration = build_single_country(code, force_reload=args.force_reload)
        results.append({
            'code': code,
            'success': success,
            'rows': rows,
            'size_mb': size_mb,
            'duration': duration
        })

    t_batch_total = time.time() - t_batch_start

    print(f"\n{'='*75}")
    print(f"[SUMMARY] BATCH EXECUTION ({len(targets)} subsidiaries in {t_batch_total/60:.1f} minutes)")
    print(f"{'='*75}")
    print(f"{'Code':<8} | {'Status':<10} | {'Rows':<12} | {'Parquet Size':<14} | {'Duration':<10}")
    print(f"{'-'*75}")
    for r in results:
        status = "SUCCESS" if r['success'] else "FAILED"
        print(f"{r['code']:<8} | {status:<10} | {r['rows']:<12,} | {r['size_mb']:<11.1f} MB | {r['duration']:<8.1f} s")
    print(f"{'='*75}")

if __name__ == '__main__':
    main()
