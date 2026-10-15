const fs = require('fs');
const p = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';
const c = fs.readFileSync(p, 'utf8');

console.log('File size:', c.length);
console.log('Has A 법인:', c.includes('A 법인'));
console.log('Has P 법인:', c.includes('P 법인'));
console.log('Has 12.62주:', c.includes('12.62주'));
console.log('Has 24.73주:', c.includes('24.73주'));
console.log('Has LGERO in drawer:', c.includes('LGERO')); 
const m = c.match(/const SC01_EXCEL_BASE64 = "([^"]*)"/);
console.log('Base64 matched:', !!m, 'len:', m ? m[1].length : 0);
