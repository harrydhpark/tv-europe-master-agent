const fs = require('fs');
const p = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';
const c = fs.readFileSync(p, 'utf8');

console.log('File size:', c.length);
console.log('Has drawer:', c.includes('id="sc01-result-drawer"'));
console.log('Has toggle func:', c.includes('function toggleScenario01Result'));
console.log('Has download func:', c.includes('function downloadScenario01Excel'));
console.log('Has Romania LGERO:', c.includes('루마니아 (LGERO)'));
console.log('Has Base64 string:', c.includes('const SC01_EXCEL_BASE64'));
