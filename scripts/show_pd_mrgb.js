const duckdb = require('duckdb');
const path = require('path');
const db = new duckdb.Database(path.resolve(__dirname, '../data/master_analytics.duckdb'), duckdb.OPEN_READONLY);

const sqlPD = `
  SELECT slide_id, report_name, report_date, meeting_type, slide_no, slide_title, content_text, tables_markdown, speaker_notes
  FROM fact_strategic_slides
  WHERE (meeting_type = 'PD회의' OR report_name LIKE '%PD%')
    AND (
      UPPER(slide_title) LIKE '%MRGB%' OR UPPER(content_text) LIKE '%MRGB%' OR UPPER(tables_markdown) LIKE '%MRGB%'
      OR UPPER(slide_title) LIKE '%MICRO RGB%' OR UPPER(content_text) LIKE '%MICRO RGB%'
    )
  ORDER BY report_date DESC, slide_no ASC;
`;

db.all(sqlPD, (err, rowsPD) => {
  if (err) { console.error(err); return; }
  console.log('Total PD MRGB Slides:', rowsPD.length);
  rowsPD.forEach((r, idx) => {
    console.log(`\n======================================================================`);
    console.log(`[#${idx+1}] ${r.report_name} (Date: ${r.report_date}) | Slide ${r.slide_no}: ${r.slide_title}`);
    console.log(`======================================================================`);
    console.log(`[Content]:\n${r.content_text}`);
    if (r.tables_markdown) {
      console.log(`\n[Table]:\n${r.tables_markdown}`);
    }
    if (r.speaker_notes) {
      console.log(`\n[Notes]:\n${r.speaker_notes}`);
    }
  });
});
