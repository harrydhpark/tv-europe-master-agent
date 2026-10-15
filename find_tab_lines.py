with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="tab-db"' in line:
        print(f"Start: Line {i+1}")
    if 'TAB 5:' in line:
        print(f"End TAB 4 / Start TAB 5: Line {i+1}")
