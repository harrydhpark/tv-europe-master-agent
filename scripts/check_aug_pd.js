const duckdb = require('duckdb');
const path = require('path');
const db = new duckdb.Database(path.resolve(__dirname, '../data/master_analytics.duckdb'), duckdb.OPEN_READONLY);

const sqlAug = `
  SELECT slide_id, report_name, report_date, meeting_type, slide_no, slide_title, content_text, tables_markdown, speaker_notes
  FROM fact_strategic_slides
  WHERE folder_name LIKE '%0818%' OR report_name LIKE '%0818%' OR report_name LIKE '%0819%'
  ORDER BY slide_no ASC;
`;

db.all(sqlAug, (err, rows) => {
  if (err) { console.error(err); return; }
  console.log('August PD Meeting Slides Count:', rows.length);
  const mrgbMatches = rows.filter(r => 
    r.slide_title.toUpperCase().includes('MRGB') || 
    r.content_text.toUpperCase().includes('MRGB') || 
    (r.tables_markdown && r.tables_markdown.toUpperCase().includes('MRGB')) ||
    r.slide_title.toUpperCase().includes('MICRO') ||
    r.content_text.toUpperCase().includes('MICRO')
  );
  console.log('August PD MRGB Matches:', mrgbMatches.length);
  mrgbMatches.forEach(r => {
    console.log(`\n[Slide ${r.slide_no}] ${r.slide_title}`);
    console.log(r.content_text.substring(0, 300));
    if (r.tables_markdown) console.log(r.tables_markdown.substring(0, 200));
  });

  if (mrgbMatches.length === 0) {
    console.log('\nAll Titles in August PD:');
    rows.forEach(r => console.log(`Slide ${r.slide_no}: ${r.slide_title}`));
  }
});
