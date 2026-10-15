const fs = require('fs');

const raw = fs.readFileSync('scripts/extracted_subs_data.json', 'utf8');
const jsonStart = raw.indexOf('[');
const data = JSON.parse(raw.slice(jsonStart));

console.log('=== [각 법인별 유통재고 신/구 WOS 및 재고량 상세 (9월 기준)] ===');
console.log('법인코드 | 법인명 | 전체WOS | 신모델WOS | 구모델WOS | 전체재고 | 신모델재고 | 구모델재고 | 신모델재고비중');
console.log('-'.repeat(120));

data.forEach(item => {
  const s = item.sep;
  const wTTL = s.wosTTL ? s.wosTTL.toFixed(2) : '-';
  const wNew = s.wosNew ? s.wosNew.toFixed(2) : '-';
  const wOld = s.wosOld ? s.wosOld.toFixed(2) : '-';
  const invTTL = Math.round(s.chInvTTL || 0);
  const invNew = Math.round(s.chInvNew || 0);
  const invOld = Math.round(s.chInvOld || 0);
  const newRatio = invTTL > 0 ? ((invNew / invTTL) * 100).toFixed(1) + '%' : '-';

  console.log([
    item.sub.padEnd(7),
    item.name.padEnd(20),
    (wTTL + '주').padStart(8),
    (wNew + '주').padStart(8),
    (wOld + '주').padStart(8),
    invTTL.toLocaleString().padStart(10),
    invNew.toLocaleString().padStart(10),
    invOld.toLocaleString().padStart(10),
    newRatio.padStart(12)
  ].join(' | '));
});
