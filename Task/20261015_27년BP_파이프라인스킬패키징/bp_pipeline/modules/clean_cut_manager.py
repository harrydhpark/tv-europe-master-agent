# -*- coding: utf-8 -*-
"""
clean_cut_manager.py:
Manages Clean-Cut rules and Carryover model persistence across M01~M12.
"""

class CleanCutManager:
    CARRYOVERS = {'98NU900B6LB', '115QNED93B6'}

    @classmethod
    def is_27yr_model(cls, model_name):
        if not model_name: return False
        m = str(model_name).upper()
        return ('B7' in m or 'C7' in m or 'G7' in m or 'M7' in m or '97' in m)

    @classmethod
    def is_carryover_model(cls, model_name, blu=None):
        if not model_name: return False
        m = str(model_name).strip()
        if m in cls.CARRYOVERS: return True
        if blu and str(blu).strip() == 'FHD': return True
        return False

    @classmethod
    def extend_carryover_prices(cls, gps, sds):
        """
        Extends M07 price and SD to M08~M12 if missing for carryover models.
        """
        new_gps = list(gps)
        new_sds = list(sds)
        
        m7_gp = new_gps[6]
        m7_sd = new_sds[6]

        for m in range(7, 12):
            if new_gps[m] <= 0 and m7_gp > 0:
                new_gps[m] = m7_gp
            if new_sds[m] <= 0 and m7_sd > 0:
                new_sds[m] = m7_sd
                
        return new_gps, new_sds
