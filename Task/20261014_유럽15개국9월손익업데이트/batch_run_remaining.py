# -*- coding: utf-8 -*-
"""
Batch Runner for Updating Remaining European Subsidiaries with 2026.09 Actuals
Excludes: RA, AK, UR (per user instruction) and DG (no 202609 file)
Already updated: Swiss, CK
Remaining to update: ['PL', 'RO', 'LA', 'SW', 'HS', 'IS', 'FS', 'PT', 'MK', 'BN', 'AG', 'UK', 'ES']
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Set base dir
BASE_DIR = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def process_single_country(country_code):
    """Worker function for running PnLPipeline on a single country"""
    import sys, os
    BASE_DIR = r"D:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis"
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from core.pipeline import PnLPipeline

    pipeline = PnLPipeline()
    t0 = time.time()
    try:
        res = pipeline.run_country(country_code, force_reload=False)
        elapsed = time.time() - t0
        return {
            'code': country_code,
            'success': res.get('success', False),
            'elapsed': elapsed,
            'error': res.get('error', None),
            'report': res.get('report_path', None)
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            'code': country_code,
            'success': False,
            'elapsed': elapsed,
            'error': str(e),
            'report': None
        }

def main():
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except Exception:
            pass

    from core.pipeline import PnLPipeline

    # Excluded: RA, AK, UR (and DG)
    # Remaining: 13 subsidiaries
    # Ordered roughly from smaller to larger for balanced throughput
    target_countries = ['PL', 'RO', 'LA', 'SW', 'HS', 'IS', 'FS', 'PT', 'MK', 'BN', 'AG', 'UK', 'ES']

    print(f"\n{'='*75}")
    print(f"[BATCH] Starting parallel execution for {len(target_countries)} countries:")
    print(f"[BATCH] Target: {', '.join(target_countries)}")
    print(f"[BATCH] Max Workers: 2 (Safe RAM & CPU allocation)")
    print(f"{'='*75}\n")

    batch_t0 = time.time()
    results = []

    # Run with 2 workers in parallel
    with ProcessPoolExecutor(max_workers=2) as executor:
        future_to_code = {executor.submit(process_single_country, code): code for code in target_countries}
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                res = future.result()
                results.append(res)
                status = "SUCCESS" if res['success'] else f"FAILED: {res['error']}"
                print(f"[BATCH DONE] [{code:<4}] {status} in {res['elapsed']:.1f}s (Total completed: {len(results)}/{len(target_countries)})")
            except Exception as exc:
                print(f"[BATCH FAIL] [{code:<4}] Generated an exception: {exc}")
                results.append({'code': code, 'success': False, 'elapsed': 0, 'error': str(exc)})

    total_elapsed = time.time() - batch_t0
    print(f"\n{'='*75}")
    print(f"[BATCH SUMMARY] Completed {len(results)} countries in {total_elapsed/60:.1f} minutes")
    print(f"{'='*75}")
    for r in results:
        stat = "PASS" if r['success'] else "FAIL"
        err = f" ({r['error']})" if r.get('error') else ""
        print(f"  {r['code']:<6} | {stat:<4} | {r['elapsed']:>6.1f}s{err}")

    # Rebuild index.html
    print(f"\n[BATCH] Rebuilding Executive Portal (index.html)...")
    pipeline = PnLPipeline()
    pipeline.update_index_portal()
    print(f"[BATCH] All operations completed successfully!\n")

if __name__ == '__main__':
    main()
