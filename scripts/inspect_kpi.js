const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('C:/Users/harry.park/AppData/Local/Temp/temp_raw_data.json', 'utf8').replace(/^\ufeff/, ''));
const eu = rawData['EU'].y26.value;

console.log('Total rows in y26:', eu.length);
eu.forEach((row, i) => {
  const rowNum = i + 19;
  const labels = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]]
    .filter(x => x !== null && x !== undefined && String(x).trim() !== '')
    .map(x => String(x).trim());
  const str = labels.join(' | ');
  if (str.includes('OLED') || str.includes('신모델') || str.includes('WOS') || str.includes('Ch.Inv') || str.includes('재고') || str.includes('비중')) {
    console.log(`Row ${rowNum}: ${str}`);
  }
});
