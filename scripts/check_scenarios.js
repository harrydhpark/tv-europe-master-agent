const fs = require('fs');
const path = 'd:/TV 유럽영업/15. AX Task/2026 AX 실행과제/00. TV Europe Sales Management Portal/docs/AXIS_System_Architecture_Guide.html';
const html = fs.readFileSync(path, 'utf8');

const sIdx2 = html.indexOf('tab-scenarios', 15000);
const s2Idx = html.indexOf('Scenario 2:', sIdx2);

console.log('sIdx2:', sIdx2, 's2Idx:', s2Idx);
if (s2Idx !== -1) {
    console.log(html.substring(sIdx2 + 2000, s2Idx + 100));
}
