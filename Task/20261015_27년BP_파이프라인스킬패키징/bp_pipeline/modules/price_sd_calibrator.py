# -*- coding: utf-8 -*-
"""
price_sd_calibrator.py:
Calibrates GP prices and SD rates to ensure exact Net Sales ($2,545.20M),
Gross Sales ($3,534.98M), and overall SD Rate of 28.00% across Europe.
"""
from collections import defaultdict

class PriceSDCalibrator:
    BASE_SD_MAP = {
        'AG': 0.270, 'BN': 0.264, 'CK': 0.234, 'DG': 0.374, 'Swiss': 0.278,
        'ES': 0.245, 'FS': 0.304, 'HS': 0.175, 'IS': 0.313, 'LA': 0.120,
        'MK': 0.140, 'PL': 0.295, 'PT': 0.296, 'RO': 0.241, 'SW': 0.166,
        'UK': 0.310
    }

    @classmethod
    def calibrate(cls, cur_rows, target_financials, subs, tot_net_target=2545.20e6, tot_sd_target=0.2800):
        tot_gross_target = tot_net_target / (1.0 - tot_sd_target)

        sum_plan_net = sum(target_financials[s]['net'] for s in subs)
        scale_net_ttl = tot_net_target / sum_plan_net
        sub_target_net = {s: target_financials[s]['net'] * scale_net_ttl for s in subs}

        def get_gross_for_alpha(alpha):
            g_sum = 0.0
            for s in cls.BASE_SD_MAP:
                t_sd = cls.BASE_SD_MAP[s] * alpha
                g_sum += sub_target_net[s] / (1.0 - t_sd)
            return g_sum

        low, high = 0.98, 1.05
        for _ in range(60):
            mid = (low + high) / 2
            if get_gross_for_alpha(mid) < tot_gross_target:
                low = mid
            else:
                high = mid
        alpha_opt = (low + high) / 2
        calib_sd_map = {s: cls.BASE_SD_MAP[s] * alpha_opt for s in cls.BASE_SD_MAP}

        # Calculate current net with new SD map
        cur_sub_net = defaultdict(float)
        for r in cur_rows:
            s = r['sub_key']
            new_sd = calib_sd_map[s]
            for m in range(12):
                q = r['m_qty'][m]
                gp = r['base_gp'][m]
                fx = r['fx_rates'][m]
                gsp = gp / fx if fx else gp
                n = q * gsp * (1.0 - new_sd)
                cur_sub_net[s] += n

        # Scale GP to match sub_target_net exactly
        gp_multipliers = {}
        for s in subs:
            if cur_sub_net[s] > 0:
                gp_multipliers[s] = sub_target_net[s] / cur_sub_net[s]
            else:
                gp_multipliers[s] = 1.0

        for r in cur_rows:
            s = r['sub_key']
            mult = gp_multipliers[s]
            new_sd = calib_sd_map[s]
            for m in range(12):
                if r['base_gp'][m] > 0:
                    r['base_gp'][m] = round(r['base_gp'][m] * mult, 2)
                if r['m_qty'][m] > 0:
                    r['base_sd'][m] = round(new_sd, 4)
                elif r['base_sd'][m] <= 0:
                    r['base_sd'][m] = round(new_sd, 4)

        return {
            'alpha_opt': alpha_opt,
            'gp_multipliers': gp_multipliers,
            'calib_sd_map': calib_sd_map
        }
