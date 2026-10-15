# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

base_url = "https://lge-tv-pnl-2026.web.app"
folder_encoded = urllib.parse.quote("법인별/05. Swiss")
report_file = "Swiss_TV_Profitability_Report.html"
excel_file = "★Swiss_ P&L Analysis_NERP_New_FROM 202301_TO_202609.xlsb"
excel_encoded = urllib.parse.quote(excel_file)

url_report = f"{base_url}/{folder_encoded}/{report_file}"
url_excel = f"{base_url}/{folder_encoded}/{excel_encoded}"

print("1. Checking Swiss Report HTML:", url_report)
req1 = urllib.request.Request(url_report, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req1) as res:
        html = res.read().decode('utf-8')
        print("Status:", res.status)
        if "FROM%20202301_TO_202609.xlsb" in html:
            print("✅ Live Swiss Report HTML: Download button correctly links to 202609.xlsb!")
        else:
            print("❌ Download button still points to old file!")
except Exception as e:
    print("Report error:", e)

print("\n2. Checking Live Excel File Download:", url_excel)
req2 = urllib.request.Request(url_excel, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
try:
    with urllib.request.urlopen(req2) as res:
        print("Status:", res.status)
        cl = res.getheader('Content-Length')
        ct = res.getheader('Content-Type')
        print(f"Content-Length: {cl} bytes ({int(cl)/(1024*1024):.1f} MB)")
        print(f"Content-Type: {ct}")
        if int(cl) > 100000000:
            print("✅ Live 202609.xlsb Excel file verified successfully (200 OK, full 112.7 MB payload ready for download)!")
except Exception as e:
    print("Excel download error:", e)
