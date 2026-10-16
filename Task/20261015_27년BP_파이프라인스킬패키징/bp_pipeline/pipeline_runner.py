# -*- coding: utf-8 -*-
"""
pipeline_runner.py:
Unified Master CLI Pipeline Runner for 2027 Business Plan (BP).
Supports audit, simulation (dry-run), and apply modes.
"""
import os
import sys
import shutil
import argparse
import time
from collections import defaultdict
import openpyxl
from pyxlsb import open_workbook

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.clean_cut_manager import CleanCutManager
from modules.volume_allocator import VolumeAllocator
from modules.price_sd_calibrator import PriceSDCalibrator
from modules.excel_block_writer import ExcelBlockWriter
from modules.audit_validator import AuditValidator

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_BASE_DIR = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\14. 사업계획_27년"
DEFAULT_INPUT_XLSB = os.path.join(DEFAULT_BASE_DIR, "● 260917 27년 BP rawdata_1차_요청+수량가이드수정_TD 0929.xlsb")
DEFAULT_PLAN_XLSX = os.path.join(DEFAULT_BASE_DIR, "사업계획 수립_20260928_TD.xlsx")
DEFAULT_H1_XLSB = os.path.join(DEFAULT_BASE_DIR, "저장", "● 260917 27년 BP rawdata_1차_요청+수량가이드수정_TD_before_h1rebalance.xlsb")

def safe_float(v):
    if v is None: return 0.0
    try: return float(v)
    except: return 0.0

def load_rows(xlsb_path):
    rows = []
    with open_workbook(xlsb_path) as wb:
        with wb.get_sheet('②모델별RAW') as sheet:
            for idx, r in enumerate(sheet.rows()):
                if idx < 15: continue
                vals = [c.v for c in r]
                if len(vals) > 23 and str(vals[9]).strip() == '02.유럽':
                    sub_code = str(vals[11]).strip() if vals[11] else ''
                    ctr_code = str(vals[15]).strip() if vals[15] else ''
                    sub_key = 'Swiss' if sub_code == 'LGEDG' and ctr_code == 'Swiss' else sub_code.replace('LGE', '')
                    blu = str(vals[16]).strip().upper() if vals[16] else ''
                    prod = str(vals[17]).strip().upper() if vals[17] else ''
                    inch = AuditValidator.safe_inch(vals[18])
                    model = str(vals[19]).strip() if vals[19] else ''
                    dist_no = str(vals[6]).strip() if vals[6] else ''
                    yr = '26' if '26' in str(vals[22]) else '27'
                    tool = str(vals[23]).strip().upper() if vals[23] else ''
                    seg = AuditValidator.get_segment(blu, prod, tool)

                    m_qty = [int(round(safe_float(vals[40+m]))) for m in range(12)]
                    fx_rates = [safe_float(vals[28+m]) or 1.0 for m in range(12)]
                    base_gp = [safe_float(vals[57+m]) for m in range(12)]
                    base_sd = [safe_float(vals[69+m]) for m in range(12)]

                    rows.append({
                        'row': idx + 1,
                        'sub_key': sub_key,
                        'blu': blu,
                        'prod': prod,
                        'inch': inch,
                        'tool': tool,
                        'model': model,
                        'yr': yr,
                        'dist_no': dist_no,
                        'seg': seg,
                        'm_qty': m_qty,
                        'fx_rates': fx_rates,
                        'base_gp': base_gp,
                        'base_sd': base_sd
                    })
    return rows

def print_audit_report(report):
    print("=" * 80)
    print("AUDIT & VERIFICATION REPORT")
    print("=" * 80)
    print(f"1. Total European Volume: {report['total_volume']:,} units (Diff: {report['total_volume_diff']:+,})")
    print(f"2. Q1 OLED Total        : {report['q1_oled_total']:,} units (Diff: {report['q1_oled_total_diff']:+,})")
    q1_perfect = "100% PERFECT" if all(d==0 for d in report['q1_oled_diff_by_sub'].values()) else "MISMATCH"
    print(f"   -> Q1 OLED Country Match: {q1_perfect}")
    print(f"3. UHD Giant (98\"+)     : {report['uhd_giant_total']:,} units (Diff: {report['uhd_giant_total_diff']:+,})")
    giant_perfect = "100% PERFECT" if all(d==0 for d in report['uhd_giant_diff_by_sub'].values()) else "MISMATCH"
    print(f"   -> UHD Giant Country Match: {giant_perfect}")
    print(f"4. OLED 97\"             : {report['oled_97_total']:,} units (Diff: {report['oled_97_diff']:+,})")
    print(f"5. OLED 77\"↑            : {report['oled_77up_total']:,} units (Diff: {report['oled_77up_diff']:+,})")
    strat_text = "100% EXACT MATCH (0 mismatches)" if report['strat_mismatches'] == 0 else f"{report['strat_mismatches']} MISMATCHES"
    print(f"6. Strategic Segments   : {strat_text}")
    print(f"7. Gross Sales (USD)    : ${report['total_gross_m']:.2f}M")
    print(f"8. Net Sales (USD)      : ${report['total_net_m']:.2f}M (Diff: ${report['net_diff_m']:+.4f}M)")
    print(f"9. SD Rate (%)          : {report['total_sd_rate']:.4f}% (Target: 28.0000%)")
    print(f"10. Clean-Cut Violations: 27yr in M1~4: {report['clean_cut_violations_27yr_m1_m4']} | 26yr in M5~12: {report['clean_cut_violations_26yr_m5_m12']}")
    print(f"11. Missing Price / SD  : Missing GP: {report['missing_gp_count']} | Missing SD: {report['missing_sd_count']}")
    print("=" * 80)
    overall = "★ PASS (100% PERFECT)" if report['is_perfect'] else "FAIL (DISCREPANCIES DETECTED)"
    print(f"OVERALL STATUS: {overall}")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="2027 Business Plan (BP) Pipeline Runner")
    parser.add_argument("--mode", choices=["audit", "simulate", "apply"], default="audit",
                        help="Execution mode: audit (inspect current file), simulate (in-memory dry run), apply (inject to XLSB)")
    parser.add_argument("--input", default=DEFAULT_INPUT_XLSB, help="Path to input XLSB file")
    parser.add_argument("--output", default=None, help="Path to output XLSB file (defaults to in-place replacement with backup)")
    parser.add_argument("--plan", default=DEFAULT_PLAN_XLSX, help="Path to Business Plan XLSX targets file")
    parser.add_argument("--h1_source", default=DEFAULT_H1_XLSB, help="Path to H1 baseline XLSB for giant revert")
    parser.add_argument("--no_backup", action="store_true", help="Skip creating backup before apply")

    args = parser.parse_args()
    input_file = args.input
    plan_file = args.plan

    print(f"Running BP Pipeline in [{args.mode.upper()}] mode...")
    print(f"Target XLSB: {input_file}")
    print(f"Plan Targets: {plan_file}")

    if not os.path.exists(input_file):
        print(f"Error: Input XLSB not found: {input_file}")
        sys.exit(1)

    validator = AuditValidator(input_file, plan_file)

    if args.mode == "audit":
        report = validator.run_audit()
        print_audit_report(report)
        return

    # Simulation or Apply Mode
    print("\nLoading current data rows...")
    cur_rows = load_rows(input_file)
    print(f"Loaded {len(cur_rows)} Europe rows.")

    h1_rows = []
    if os.path.exists(args.h1_source):
        print(f"Loading H1 baseline from {os.path.basename(args.h1_source)}...")
        h1_rows = load_rows(args.h1_source)

    print("\nExecuting Pipeline Steps:")
    # Step 1: Revert UHD Giant
    if h1_rows:
        print("  1. Reverting UHD Giant (98\"+) to exact H1 target...")
        VolumeAllocator.revert_uhd_giant(cur_rows, h1_rows)

    # Step 1.5: Extend Carryover GP & SD
    print("  2. Extending carryover prices for 98NU900 & 115QNED...")
    for r in cur_rows:
        if CleanCutManager.is_carryover_model(r['model'], r['blu']):
            r['base_gp'], r['base_sd'] = CleanCutManager.extend_carryover_prices(r['base_gp'], r['base_sd'])

    # Step 2: Match Q1 OLED
    print("  3. Matching Q1 OLED quantities (small OLED shift)...")
    VolumeAllocator.match_q1_oled(cur_rows, validator.q1_oled_targets, validator.subs)

    # Step 2.5: Enforce Clean-Cut
    print("  4. Enforcing strict Clean-Cut (0 in M05~M12 for 26yr)...")
    VolumeAllocator.enforce_clean_cut(cur_rows)

    # Step 3: Rebalance Strategic Segments
    print("  5. Re-balancing 8 strategic segments (128 combinations)...")
    VolumeAllocator.rebalance_strategic_segments(cur_rows, validator.strat_targets, validator.subs)

    # Step 4: Calibrate GP & SD
    print("  6. Calibrating GP prices and SD rates (Net $2,545.20M, SD 28.00%)...")
    PriceSDCalibrator.calibrate(cur_rows, validator.target_financials, validator.subs)

    print("\nIn-Memory Simulation complete.")

    if args.mode == "simulate":
        print("Dry-run finished successfully. No files were modified.")
        return

    if args.mode == "apply":
        target_out = args.output if args.output else input_file
        if not args.no_backup:
            backup_file = input_file.replace(".xlsb", "_backup.xlsb")
            print(f"Creating backup: {os.path.basename(backup_file)}...")
            shutil.copy2(input_file, backup_file)

        start_row = cur_rows[0]['row']
        end_row = cur_rows[-1]['row']
        qty_block = [r['m_qty'] for r in cur_rows]
        gp_block = [r['base_gp'] for r in cur_rows]
        sd_block = [r['base_sd'] for r in cur_rows]

        print(f"Injecting blocks into {os.path.basename(target_out)} (Rows {start_row} to {end_row})...")
        ExcelBlockWriter.write_blocks(target_out, start_row, end_row, qty_block, gp_block, sd_block)
        print("Injection complete. Running post-apply independent audit...")

        post_validator = AuditValidator(target_out, plan_file)
        post_report = post_validator.run_audit()
        print_audit_report(post_report)

if __name__ == "__main__":
    main()
