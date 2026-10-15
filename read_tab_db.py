with open('d:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="tab-db"')
if idx != -1:
    end_idx = text.find('id="tab-', idx + 10)
    print("Found! Length:", end_idx - idx if end_idx != -1 else len(text) - idx)
    with open('tab_db_excerpt.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx:end_idx if end_idx != -1 else idx + 15000])
else:
    print('Not found')
