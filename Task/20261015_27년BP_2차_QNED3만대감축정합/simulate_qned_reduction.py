# -*- coding: utf-8 -*-
"""
simulate_qned_reduction.py:
In-memory simulation to reduce QNED by exactly 30,001 units across 16 European countries
in '● 261007 27년 BP rawdata_2차_요청_EU회신.xlsb'.
Using Hare-Niemeyer (Largest Remainder) integer allocation to guarantee:
1. Exact integer match to country targets.
2. 0 negative quantities (strictly non-negative).
3. 98"+ models completely untouched.
"""
import sys
from collections import defaultdict
from pyxlsb import open_workbook

sys.stdout.reconfigure(encoding='utf-8')

fn = '● 261007 27년 BP rawdata_2차_요청_EU회신.xlsb'

qned_targets = {
    'AG': 35348, 'BN': 38512, 'CK': 53802, 'DG': 192872,
    'Swiss': 17110, 'ES': 289881, 'FS': 93186, 'HS': 51584,
    'IS': 107763, 'LA': 29927, 'MK': 212688, 'PL': 36791,
    'PT': 81196, 'RO': 74341, 'SW': 129828, 'UK': 402921
}

def safe_f(v):
    try: return float(v or 0)
    except: return 0.0

def safe_inch(v):
    try: return int(round(float(v)))
    except: return 0

# 1. Load Europe rows
rows = []
with open_workbook(fn) as wb:
    with wb.get_sheet('③모델별RAW') as sheet:
        for idx, r in enumerate(sheet.rows()):
            if idx < 17: continue
            vals = [c.v for c in r]
            if len(vals) > 28 and str(vals[21] or '').strip() == '02.유럽':
                row_idx = idx + 1
                sub = str(vals[24] or '').strip()
                ctr = str(vals[27] or '').strip()
                sub_key = 'Swiss' if sub == 'LGEDG' and ctr == 'Swiss' else sub.replace('LGE', '')
                blu = str(vals[28] or '').strip().upper()
                prod = str(vals[29] or '').strip().upper()
                inch = safe_inch(vals[30])
                model = str(vals[31] or '').strip()
                yr = str(vals[34] or '').strip()
                
                m_qty = [int(round(safe_f(vals[52+m]))) for m in range(12)]
                
                rows.append({
                    'row': row_idx,
                    'sub_key': sub_key,
                    'blu': blu,
                    'prod': prod,
                    'inch': inch,
                    'model': model,
                    'yr': yr,
                    'm_qty': m_qty
                })

print(f"Loaded {len(rows)} Europe rows (Row {rows[0]['row']} to Row {rows[-1]['row']}).")

initial_qned = defaultdict(int)
for r in rows:
    if r['prod'] == 'QNED':
        initial_qned[r['sub_key']] += sum(r['m_qty'])

print("\n--- Performing Exact Hare-Niemeyer Reduction in 27yr New Models M05~M12 (<90\") ---")
for s in qned_targets:
    target_reduction = initial_qned[s] - qned_targets[s]
    if target_reduction <= 0:
        continue
    
    cand_rows = [r for r in rows if r['sub_key'] == s and r['prod'] == 'QNED' and r['inch'] < 90 and ('27' in r['yr'] or 'C7' in r['model'] or 'B7' in r['model'])]
    if not cand_rows:
        cand_rows = [r for r in rows if r['sub_key'] == s and r['prod'] == 'QNED' and r['inch'] < 90]
        
    # Eligible cell list: (row_dict, month_index, current_qty)
    cell_refs = []
    for r in cand_rows:
        for m in range(4, 12):
            if r['m_qty'][m] > 0:
                cell_refs.append({
                    'r': r,
                    'm': m,
                    'q': r['m_qty'][m]
                })
                
    total_cand_vol = sum(c['q'] for c in cell_refs)
    if total_cand_vol < target_reduction:
        print(f"ERROR: {s} available volume {total_cand_vol} < needed {target_reduction}")
        continue
        
    # Largest Remainder Method
    for c in cell_refs:
        exact_ded = target_reduction * (c['q'] / total_cand_vol)
        base_ded = int(exact_ded)
        frac = exact_ded - base_ded
        # Cap base_ded at c['q']
        base_ded = min(base_ded, c['q'])
        c['base_ded'] = base_ded
        c['frac'] = frac
        
    current_ded = sum(c['base_ded'] for c in cell_refs)
    remainder_needed = target_reduction - current_ded
    
    # Sort by fraction descending, break ties by current quantity
    cell_refs.sort(key=lambda x: (x['frac'], x['q']), reverse=True)
    
    for c in cell_refs:
        if remainder_needed <= 0:
            break
        if c['q'] > c['base_ded']:
            c['base_ded'] += 1
            remainder_needed -= 1
            
    # Apply deductions
    total_deducted = 0
    for c in cell_refs:
        c['r']['m_qty'][c['m']] -= c['base_ded']
        total_deducted += c['base_ded']
        
    print(f"{s:7s}: Need -{target_reduction:,d} | Deducted: -{total_deducted:,d} | Cells: {len(cell_refs)}")

# 3. Verify Final Results
final_qned = defaultdict(int)
giant_98up = defaultdict(int)
negative_cells = []

for r in rows:
    if r['prod'] == 'QNED':
        final_qned[r['sub_key']] += sum(r['m_qty'])
    if r['inch'] >= 98:
        giant_98up[r['sub_key']] += sum(r['m_qty'])
    for m in range(12):
        if r['m_qty'][m] < 0:
            negative_cells.append((r['row'], r['sub_key'], r['model'], m+1, r['m_qty'][m]))

print("\n--- Final QNED Verification ---")
final_diff = 0
perfect = True
for s in sorted(qned_targets.keys()):
    cur = final_qned[s]
    tgt = qned_targets[s]
    diff = cur - tgt
    final_diff += diff
    status = "OK" if diff == 0 else f"ERR ({diff:+d})"
    if diff != 0: perfect = False
    print(f"{s:7s} | Act: {cur:7,d} | Tgt: {tgt:7,d} | Diff: {diff:+6,d} | {status}")

print(f"TOTAL   | Act: {sum(final_qned.values()):7,d} | Tgt: {sum(qned_targets.values()):7,d} | Diff: {final_diff:+6,d}")
print(f"\nNegative quantity cells: {len(negative_cells)}")
print(f"Total 98\"+ volume: {sum(giant_98up.values()):,d} (Original was 53,521 | Diff: {sum(giant_98up.values()) - 53521:+d})")

if perfect and len(negative_cells) == 0 and sum(giant_98up.values()) == 53521:
    print("\n★ ALL CONSTRAINTS AND TARGETS 100% SATISFIED! ★")
