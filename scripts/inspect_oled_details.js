const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('C:/Users/harry.park/AppData/Local/Temp/temp_raw_data.json', 'utf8').replace(/^\ufeff/, ''));
const eu = rawData['EU'].y26.value;

console.log('=== Rows 19 to 35 in EU ===');
for (let r = 19; r <= 35; r++) {
  const row = eu[r - 19];
  const label = [row[2], row[3], row[6], row[7], row[8], row[9], row[10]].filter(Boolean).join(' | ');
  const vals = row.slice(11, 29);
  console.log(`Row ${r} [${label}]: Aug=${vals[8]}, Sep=${vals[9]}`);
}

console.log('\n=== Rows around 95-130 in EU ===');
for (let r = 95; r <= 130; r++) {
  const row = eu[r - 19];
  const label = [row[2], row[3], row[6], row[7], row[8], row[9], row[10]].filter(Boolean).join(' | ');
  if (label.includes('OLED') || label.includes('신모델') || label.includes('구모델') || label.includes('요약')) {
    const vals = row.slice(11, 29);
    console.log(`Row ${r} [${label}]: Aug=${vals[8]}, Sep=${vals[9]}`);
  }
}

console.log('\n=== Rows 195 to 255 in EU ===');
for (let r = 195; r <= 255; r++) {
  const row = eu[r - 19];
  const label = [row[2], row[3], row[6], row[7], row[8], row[9], row[10]].filter(Boolean).join(' | ');
  if (label.includes('OLED') || label.includes('요약')) {
    const vals = row.slice(11, 29);
    console.log(`Row ${r} [${label}]: Aug=${vals[8]}, Sep=${vals[9]}`);
  }
}
