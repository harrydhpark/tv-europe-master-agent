import duckdb

conn = duckdb.connect(':memory:')
conn.execute("INSTALL fts; LOAD fts;")
conn.execute("CREATE TABLE test (id INT, txt VARCHAR);")
conn.execute("INSERT INTO test VALUES (1, '독일 법인 OLED C4 프로모션 방침');")
conn.execute("PRAGMA create_fts_index('test', 'id', 'txt');")
res = conn.execute("""
SELECT id, score 
FROM (
    SELECT *, fts_main_test.match_bm25(id, 'OLED') AS score 
    FROM test
) 
WHERE score IS NOT NULL;
""").fetchall()
print("FTS test result:", res)
