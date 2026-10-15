const duckdb = require('duckdb');
const path = require('path');

const dbPath = path.resolve(__dirname, '../data/master_analytics.duckdb');
const db = new duckdb.Database(dbPath, duckdb.OPEN_READONLY);

// 1. Search in PD meetings
const sqlPD = `
  SELECT slide_id, report_name, report_date, meeting_type, slide_no, slide_title, content_text, tables_markdown, speaker_notes
  FROM fact_strategic_slides
  WHERE (meeting_type = 'PD회의' OR report_name LIKE '%PD%')
    AND (
      UPPER(slide_title) LIKE '%MRGB%' OR UPPER(content_text) LIKE '%MRGB%' OR UPPER(tables_markdown) LIKE '%MRGB%' OR UPPER(speaker_notes) LIKE '%MRGB%'
      OR UPPER(slide_title) LIKE '%MICRO RGB%' OR UPPER(content_text) LIKE '%MICRO RGB%'
      OR UPPER(product_tags) LIKE '%MRGB%'
    )
  ORDER BY report_date DESC, slide_no ASC;
`;

// 2. Also search across all meetings just in case to provide complete strategic context
const sqlAll = `
  SELECT slide_id, report_name, report_date, meeting_type, slide_no, slide_title, content_text, tables_markdown, speaker_notes
  FROM fact_strategic_slides
  WHERE UPPER(slide_title) LIKE '%MRGB%' OR UPPER(content_text) LIKE '%MRGB%' OR UPPER(tables_markdown) LIKE '%MRGB%'
  ORDER BY report_date DESC, slide_no ASC;
`;

db.all(sqlPD, (err, rowsPD) => {
  if (err) {
    console.error('PD Query Error:', err);
    return;
  }
  console.log(`=== MRGB in PD Meetings Found: ${rowsPD.length} slides ===`);
  rowsPD.forEach((r, idx) => {
    console.log(`\n--- [PD Slide ${idx + 1}] ${r.report_name} (Date: ${r.report_date}, Slide: ${r.slide_no}) ---`);
    console.log(`Title: ${r.slide_title}`);
    console.log(`Content:\n${r.content_text}`);
    if (r.tables_markdown) console.log(`Tables:\n${r.tables_markdown}`);
    if (r.speaker_notes) console.log(`Notes:\n${r.speaker_notes}`);
  });

  db.all(sqlAll, (err2, rowsAll) => {
    if (err2) {
      console.error('All Query Error:', err2);
      return;
    }
    console.log(`\n=== MRGB in ALL Strategic Meetings Found: ${rowsAll.length} slides ===`);
    rowsAll.forEach((r, idx) => {
      console.log(`[Slide ${idx + 1}] (${r.report_date} ${r.meeting_type}) ${r.report_name} p.${r.slide_no} : ${r.slide_title}`);
    });
  });
});
