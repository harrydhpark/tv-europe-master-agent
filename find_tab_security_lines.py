with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="tab-security"' in line:
        print(f"Start Security: Line {i+1}")
    if 'TAB 6:' in line or 'id="tab-ops"' in line:
        print(f"End Security / Start Next: Line {i+1}")
