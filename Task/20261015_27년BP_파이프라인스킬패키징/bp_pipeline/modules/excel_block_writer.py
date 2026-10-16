# -*- coding: utf-8 -*-
"""
excel_block_writer.py:
Injects 2D data blocks into XLSB files using Excel COM.
Enforces xlCalculationManual and SaveCopyAs anti-hang pattern.
"""
import os
import shutil
import win32com.client as win32

class ExcelBlockWriter:
    @classmethod
    def write_blocks(cls, target_xlsb, start_row, end_row, qty_block, gp_block, sd_block, sheet_name='②모델별RAW'):
        """
        Injects Qty, GP, and SD 2D arrays into target_xlsb using SaveCopyAs pattern.
        """
        temp_file = target_xlsb + ".temp.xlsb"
        if os.path.exists(temp_file):
            os.remove(temp_file)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False
        excel.DisplayAlerts = False
        excel.ScreenUpdating = False

        try:
            wb = excel.Workbooks.Open(target_xlsb)
            excel.Calculation = -4135  # xlCalculationManual
            ws = wb.Worksheets(sheet_name)

            range_qty = f"AO{start_row}:AZ{end_row}"
            range_gp  = f"BF{start_row}:BQ{end_row}"
            range_sd  = f"BR{start_row}:CC{end_row}"

            ws.Range(range_qty).Value = qty_block
            ws.Range(range_gp).Value = gp_block
            ws.Range(range_sd).Value = sd_block

            wb.SaveCopyAs(temp_file)
            wb.Close(SaveChanges=False)
        finally:
            excel.Quit()

        shutil.move(temp_file, target_xlsb)
        return True
