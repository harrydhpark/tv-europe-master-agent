# -*- coding: utf-8 -*-
"""
volume_allocator.py:
Handles volume shifting, Q1 OLED alignment, UHD Giant carryover restoration,
and strategic segment volume conservation.
"""
from collections import defaultdict
from .clean_cut_manager import CleanCutManager

class VolumeAllocator:
    @classmethod
    def revert_uhd_giant(cls, cur_rows, h1_rows):
        """
        Restores UHD Giant (98"+) to H1 target.
        Compensates non-98" models in same sub/seg/dist in M05~M12.
        """
        cur_map = {r['row']: r for r in cur_rows}
        
        for r_h1 in h1_rows:
            if r_h1['blu'] == 'UHD' and r_h1['inch'] >= 98:
                r_cur = cur_map.get(r_h1['row'])
                if not r_cur: continue
                
                diff_m = [r_h1['m_qty'][m] - r_cur['m_qty'][m] for m in range(12)]
                tot_diff = sum(diff_m)
                if tot_diff != 0:
                    sub = r_h1['sub_key']
                    seg = r_h1['seg']
                    dist = r_h1['dist_no']
                    
                    candidates = [r for r in cur_rows if r['sub_key'] == sub and r['seg'] == seg and r['dist_no'] == dist and r['inch'] < 98]
                    if not candidates:
                        candidates = [r for r in cur_rows if r['sub_key'] == sub and r['seg'] == seg and r['inch'] < 98]
                        
                    delta = sum(r_h1['m_qty']) - sum(r_cur['m_qty'])
                    for m in range(12):
                        r_cur['m_qty'][m] = r_h1['m_qty'][m]
                        
                    cand_adjust = -delta
                    h2_cand = sum(sum(r['m_qty'][4:]) for r in candidates)
                    if h2_cand > 0:
                        allocated = 0
                        for m in range(4, 11):
                            m_weight = sum(r['m_qty'][m] for r in candidates) / h2_cand
                            m_amt = int(round(cand_adjust * m_weight))
                            if m_amt > 0:
                                best_c = max(candidates, key=lambda x: x['m_qty'][m])
                                best_c['m_qty'][m] += m_amt
                            elif m_amt < 0:
                                rem_deduct = -m_amt
                                for c in sorted(candidates, key=lambda x: x['m_qty'][m], reverse=True):
                                    sub_amt = min(rem_deduct, c['m_qty'][m])
                                    c['m_qty'][m] -= sub_amt
                                    rem_deduct -= sub_amt
                                    if rem_deduct == 0: break
                            allocated += m_amt
                            
                        rem_final = cand_adjust - allocated
                        if rem_final > 0:
                            best_c = max(candidates, key=lambda x: x['m_qty'][11])
                            best_c['m_qty'][11] += rem_final
                        elif rem_final < 0:
                            rem_deduct = -rem_final
                            for c in sorted(candidates, key=lambda x: x['m_qty'][11], reverse=True):
                                sub_amt = min(rem_deduct, c['m_qty'][11])
                                c['m_qty'][11] -= sub_amt
                                rem_deduct -= sub_amt
                                if rem_deduct == 0: break
                    elif candidates:
                        best_c = candidates[0]
                        best_c['m_qty'][11] += cand_adjust

    @classmethod
    def match_q1_oled(cls, cur_rows, q1_oled_targets, subs):
        """
        Shifts Q1 OLED excess proportionally within small OLED (<77") models per segment
        (G시리즈, CB시리즈), keeping 77"↑, 97", and 8 strategic segment totals 100% invariant.
        """
        cur_map = {r['row']: r for r in cur_rows}
        oled_26_to_27_map = {}
        for r in cur_rows:
            if r['blu'] == 'OLED' and r['yr'] == '26':
                cands = [c for c in cur_rows if c['blu'] == 'OLED' and c['yr'] == '27' and c['sub_key'] == r['sub_key'] and c['seg'] == r['seg'] and c['inch'] == r['inch'] and c['dist_no'] == r['dist_no']]
                if not cands:
                    cands = [c for c in cur_rows if c['blu'] == 'OLED' and c['yr'] == '27' and c['sub_key'] == r['sub_key'] and c['seg'] == r['seg'] and c['inch'] == r['inch']]
                if not cands:
                    cands = [c for c in cur_rows if c['blu'] == 'OLED' and c['yr'] == '27' and c['sub_key'] == r['sub_key'] and c['seg'] == r['seg']]
                if cands:
                    best_c = max(cands, key=lambda x: sum(x['m_qty'][4:]))
                    oled_26_to_27_map[r['row']] = best_c['row']

        for s in subs:
            tgt_q1 = q1_oled_targets.get(s, 0)
            cur_q1 = sum(sum(r['m_qty'][:3]) for r in cur_rows if r['sub_key'] == s and r['blu'] == 'OLED')
            delta_s = cur_q1 - tgt_q1
            
            if delta_s != 0:
                seg_q1_vols = {}
                for seg in ['G시리즈', 'CB시리즈']:
                    v = sum(sum(r['m_qty'][:3]) for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['yr'] == '26' and r['inch'] < 77)
                    seg_q1_vols[seg] = v
                tot_small_q1 = sum(seg_q1_vols.values())
                
                for seg, seg_v in seg_q1_vols.items():
                    if tot_small_q1 <= 0: continue
                    seg_delta = int(round(delta_s * (seg_v / tot_small_q1)))
                    if seg == 'CB시리즈':
                        seg_delta = delta_s - sum(int(round(delta_s * (seg_q1_vols[g] / tot_small_q1))) for g in ['G시리즈'])
                        
                    seg_rows = [r for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['yr'] == '26' and r['inch'] < 77 and sum(r['m_qty'][:3]) > 0 and oled_26_to_27_map.get(r['row'])]
                    seg_cur_q1 = sum(sum(r['m_qty'][:3]) for r in seg_rows)
                    
                    if seg_delta != 0 and seg_cur_q1 > 0:
                        allocated = 0
                        for r in seg_rows:
                            r_q1 = sum(r['m_qty'][:3])
                            r_shift = int(round(seg_delta * (r_q1 / seg_cur_q1)))
                            if seg_delta > 0: r_shift = min(r_shift, r_q1)
                            
                            if r_shift != 0:
                                rem_red = r_shift
                                if r_shift > 0:
                                    for m in range(3):
                                        m_sub = min(rem_red, int(round(r_shift * (r['m_qty'][m] / r_q1)))) if r_q1 > 0 else 0
                                        r['m_qty'][m] -= m_sub
                                        rem_red -= m_sub
                                    if rem_red > 0:
                                        for m in range(3):
                                            can_sub = min(rem_red, r['m_qty'][m])
                                            r['m_qty'][m] -= can_sub
                                            rem_red -= can_sub
                                            if rem_red == 0: break
                                else:
                                    to_add = -r_shift
                                    for m in range(3):
                                        m_add = int(round(to_add * (r['m_qty'][m] / r_q1))) if r_q1 > 0 else to_add // 3
                                        r['m_qty'][m] += m_add
                                        rem_red -= m_add
                                    r['m_qty'][2] += rem_red
                                    
                                actual_shifted = r_shift - rem_red
                                allocated += actual_shifted
                                
                                c_27 = cur_map[oled_26_to_27_map[r['row']]]
                                h2_vol = sum(c_27['m_qty'][4:])
                                if actual_shifted > 0:
                                    add_rem = actual_shifted
                                    for m in range(4, 11):
                                        m_add = int(round(actual_shifted * (c_27['m_qty'][m] / h2_vol))) if h2_vol > 0 else actual_shifted // 8
                                        c_27['m_qty'][m] += m_add
                                        add_rem -= m_add
                                    c_27['m_qty'][11] += add_rem
                                elif actual_shifted < 0:
                                    ded_rem = -actual_shifted
                                    for m in range(11, 3, -1):
                                        can_ded = min(ded_rem, c_27['m_qty'][m])
                                        c_27['m_qty'][m] -= can_ded
                                        ded_rem -= can_ded
                                        if ded_rem == 0: break
                                    if ded_rem > 0:
                                        r['m_qty'][2] -= ded_rem
                                        actual_shifted += ded_rem
                                        
                        seg_q1_now = sum(sum(r['m_qty'][:3]) for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['yr'] == '26' and r['inch'] < 77)
                        target_seg_q1 = seg_cur_q1 - seg_delta
                        diff_seg = seg_q1_now - target_seg_q1
                        if diff_seg != 0 and seg_rows:
                            best_r = max(seg_rows, key=lambda x: sum(x['m_qty'][:3]))
                            best_r['m_qty'][2] -= diff_seg
                            c_27 = cur_map[oled_26_to_27_map[best_r['row']]]
                            c_27['m_qty'][11] += diff_seg

    @classmethod
    def enforce_clean_cut(cls, cur_rows):
        """
        Enforces Clean-Cut: 26yr non-carryover models must have 0 in M05~M12.
        Moves any leftover into M04.
        """
        for r in cur_rows:
            if r['yr'] == '26' and not CleanCutManager.is_carryover_model(r['model'], r['blu']):
                for m in range(4, 12):
                    if r['m_qty'][m] > 0:
                        r['m_qty'][3] += r['m_qty'][m]
                        r['m_qty'][m] = 0

    @classmethod
    def rebalance_strategic_segments(cls, cur_rows, strat_targets, subs):
        """
        Ensures 128 strategic segment combinations exactly match target.
        """
        for s in subs:
            for seg in ['W시리즈', 'G시리즈', 'CB시리즈', 'Micro RGB', 'Mini RGB', 'QNED', '일반UHD', 'FHD']:
                act = sum(sum(r['m_qty']) for r in cur_rows if r['sub_key'] == s and r['seg'] == seg)
                tgt = strat_targets.get((s, seg), 0)
                diff = act - tgt
                if diff != 0:
                    cands = [r for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['inch'] < 77 and r['yr'] == '27']
                    if not cands: cands = [r for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['inch'] < 77]
                    if not cands: cands = [r for r in cur_rows if r['sub_key'] == s and r['seg'] == seg and r['inch'] < 98]
                    if cands:
                        best_c = max(cands, key=lambda x: sum(x['m_qty'][4:]))
                        best_c['m_qty'][11] -= diff
