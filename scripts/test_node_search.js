const duckdb = require('duckdb');
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/master_analytics.duckdb');
const db = new duckdb.Database(dbPath, duckdb.OPEN_READONLY);

db.all('SELECT count(*) as total_slides FROM fact_strategic_slides', (err, rows) => {
  if (err) console.error('Count Error:', err);
  else console.log('DuckDB slides count:', rows);
});

const sql = `
  SELECT slide_id, report_name, report_date, slide_no, slide_title, score
  FROM (
    SELECT *, fts_main_fact_strategic_slides.match_bm25(slide_id, 'OLED') AS score
    FROM fact_strategic_slides
  )
  WHERE score IS NOT NULL
  ORDER BY score DESC
  LIMIT 3;
`;

db.all(sql, (err, rows) => {
  if (err) console.error('FTS Error:', err);
  else {
    console.log('FTS Sample Results:');
    rows.forEach(r => console.log(`  - [Slide ${r.slide_no}] ${r.report_name} | ${r.slide_title} (BM25: ${r.score.toFixed(3)})`));
  }
});
