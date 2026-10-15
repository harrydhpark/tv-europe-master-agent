const fs = require('fs');

const raw = fs.readFileSync('scripts/extracted_subs_data.json', 'utf8');
const jsonStart = raw.indexOf('[');
const data = JSON.parse(raw.slice(jsonStart));

console.log('=== [2026년 9월 최신 기준: 9/21W 주차 실적 기준 (9/28W 조회)] ===');
console.log('구분 | 법인코드 | 법인명 | 유통재고WOS | 리스크 유형 | 유통재고(대) | Sell-out(대) | OLED신모델(대) | OLED내 신모델비중 | 신모델내 OLED비중 | 전체TV내 OLED신모델');
console.log('-'.repeat(140));

data.forEach(item => {
  const s = item.sep;
  const wos = s.wosTTL !== null && s.wosTTL !== undefined ? s.wosTTL.toFixed(2) : '-';
  let status = '정상 (3~6주)';
  let isRisk = false;
  if (s.wosTTL > 6) {
    status = '과다재고 (>6주)';
    isRisk = true;
  } else if (s.wosTTL < 3) {
    status = '재고부족 (<3주)';
    isRisk = true;
  }

  const tag = isRisk ? '★ 리스크' : '  정상  ';

  console.log([
    tag,
    item.sub.padEnd(7),
    item.name.padEnd(20),
    (wos + '주').padStart(8),
    status.padEnd(14),
    Math.round(s.chInvTTL || 0).toLocaleString().padStart(10),
    Math.round(s.soTTL || 0).toLocaleString().padStart(10),
    Math.round(s.soOledNew || 0).toLocaleString().padStart(10),
    (s.oledNewRatioInOled_SO.toFixed(1) + '%').padStart(16),
    (s.oledRatioInNew_SO.toFixed(1) + '%').padStart(14),
    (s.oledNewRatioInTotal_SO.toFixed(1) + '%').padStart(14)
  ].join(' | '));
});

console.log('\n=== [2026년 8월 마감 실적 기준] ===');
console.log('구분 | 법인코드 | 법인명 | 유통재고WOS | 리스크 유형 | 유통재고(대) | Sell-out(대) | OLED신모델(대) | OLED내 신모델비중 | 신모델내 OLED비중 | 전체TV내 OLED신모델');
console.log('-'.repeat(140));

data.forEach(item => {
  const a = item.aug;
  const wos = a.wosTTL !== null && a.wosTTL !== undefined ? a.wosTTL.toFixed(2) : '-';
  let status = '정상 (3~6주)';
  let isRisk = false;
  if (a.wosTTL > 6) {
    status = '과다재고 (>6주)';
    isRisk = true;
  } else if (a.wosTTL < 3) {
    status = '재고부족 (<3주)';
    isRisk = true;
  }

  const tag = isRisk ? '★ 리스크' : '  정상  ';

  console.log([
    tag,
    item.sub.padEnd(7),
    item.name.padEnd(20),
    (wos + '주').padStart(8),
    status.padEnd(14),
    Math.round(a.chInvTTL || 0).toLocaleString().padStart(10),
    Math.round(a.soTTL || 0).toLocaleString().padStart(10),
    Math.round(a.soOledNew || 0).toLocaleString().padStart(10),
    (a.oledNewRatioInOled_SO.toFixed(1) + '%').padStart(16),
    (a.oledRatioInNew_SO.toFixed(1) + '%').padStart(14),
    (a.oledNewRatioInTotal_SO.toFixed(1) + '%').padStart(14)
  ].join(' | '));
});
