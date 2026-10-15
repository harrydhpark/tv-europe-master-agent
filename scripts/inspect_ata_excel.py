import openpyxl

wb_path = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\10. 수익성 Simulator\Simulator\★손익 Simulator_26년 7월차 선행_1차.xlsx"
wb = openpyxl.load_workbook(wb_path, read_only=True)
with open("sheets_pnl_sim.txt", "w", encoding="utf-8") as f:
    for name in wb.sheetnames:
        f.write(name + "\n")
print("Saved PnL Sim sheet names")
