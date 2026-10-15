const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('C:/Users/harry.park/AppData/Local/Temp/temp_raw_data.json', 'utf8').replace(/^\ufeff/, ''));

const listEurope = ['LGEAG', 'LGEBN', 'LGECK', 'LGEDG', 'Swiss', 'LGEES', 'LGEFS', 'LGEHS', 'LGEIS', 'LGELA', 'LGEMK', 'LGEPL', 'LGEPT', 'LGERO', 'LGESW', 'LGEUK'];

console.log('=== Checking Column Indices for 2026 in row26 ===');
// Let's inspect row 31 (WOS TTL, which is idx 12 in array, since sheetRowNumber = idx + 19 => idx = 31 - 19 = 12)
const euData = rawData['EU'].y26.value;
const wosRow = euData[31 - 19];
console.log('EU WOS Row length:', wosRow.length);
console.log('EU WOS Row slice(0, 15):', wosRow.slice(0, 15));
console.log('EU WOS Row slice(11, 29):', wosRow.slice(11, 29)); // 18 items!

// In build_dashboard.js:
// const y26_vals = row26.slice(11, 29).map(v => ...);
// colHeaders = ["1월", "2월", "3월", "4월", "5월", "6월", "상반기", "7월", "8월", "9월", "10월", "11월", "12월", "1Q", "2Q", "3Q", "4Q", "TTL"];
// So in y26_vals:
// 0: Jan (1월)
// 1: Feb (2월)
// 2: Mar (3월)
// 3: Apr (4월)
// 4: May (5월)
// 5: Jun (6월)
// 6: 상반기 (H1)
// 7: Jul (7월)
// 8: Aug (8월)
// 9: Sep (9월)
// 10: Oct (10월)
// 11: Nov (11월)
// 12: Dec (12월)
// 13: 1Q
// 14: 2Q
// 15: 3Q
// 16: 4Q
// 17: TTL

console.log('\n=== Checking WOS for all European entities ===');
listEurope.forEach(sub => {
  const d = rawData[sub].y26.value;
  const wos = d[31 - 19].slice(11, 29);
  console.log(`${sub}: Aug(8월)=${wos[8]}, Sep(9월)=${wos[9]}, 3Q=${wos[15]}`);
});
