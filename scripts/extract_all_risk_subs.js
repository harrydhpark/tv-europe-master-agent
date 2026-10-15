const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('C:/Users/harry.park/AppData/Local/Temp/temp_raw_data.json', 'utf8').replace(/^\ufeff/, ''));

const subs = [
  'LGEAG', 'LGEBN', 'LGECK', 'LGEDG', 'Swiss', 'LGEES', 
  'LGEFS', 'LGEHS', 'LGEIS', 'LGELA', 'LGEMK', 'LGEPL', 
  'LGEPT', 'LGERO', 'LGESW', 'LGEUK', 'EU'
];

const subNames = {
  'EU': '유럽 본부 (EU TTL)',
  'LGEAG': '오스트리아 (LGEAG)',
  'LGEBN': '베네룩스 (LGEBN)',
  'LGECK': '체코/슬로바키아 (LGECK)',
  'LGEDG': '독일 (LGEDG)',
  'Swiss': '스위스 (Swiss)',
  'LGEES': '스페인 (LGEES)',
  'LGEFS': '프랑스 (LGEFS)',
  'LGEHS': '그리스 (LGEHS)',
  'LGEIS': '이탈리아 (LGEIS)',
  'LGELA': '라트비아/발틱 (LGELA)',
  'LGEMK': '헝가리 (LGEMK)',
  'LGEPL': '폴란드 (LGEPL)',
  'LGEPT': '포르투갈 (LGEPT)',
  'LGERO': '루마니아 (LGERO)',
  'LGESW': '스웨덴/노르딕 (LGESW)',
  'LGEUK': '영국 (LGEUK)'
};

console.log('Subsidiary data analysis...');

const results = [];

subs.forEach(sub => {
  const d = rawData[sub].y26.value;

  // Row index mapping in data26 (where sheetRowNumber = idx + 19 => idx = sheetRowNumber - 19)
  // Col index for 2026: slice(11, 29)
  // 8: Aug (8월), 9: Sep (9월)
  
  const getRow = (rowNum) => d[rowNum - 19].slice(11, 29);

  // WOS & Inventory
  const wosTTL = getRow(31);
  const wosNew = getRow(32);
  const wosOld = getRow(33);
  const chInvTTL = getRow(28);
  const chInvNew = getRow(29);
  const chInvOld = getRow(30);

  // Sell-out
  const soTTL = getRow(24);
  const soNew = getRow(25);
  const soRatio = getRow(26); // 신모델 비중 (전체 TV)
  const soOld = getRow(27);
  const soOledNew = getRow(198); // 신모델 OLED 요약 (GDMI Sell-out)
  const soOledOld = getRow(248); // 구모델 OLED 요약 (GDMI Sell-out)

  // Sell-in
  const siTTL = getRow(19);
  const siOledTTL = getRow(20);
  const siQnedTTL = getRow(21);
  const siNew = getRow(22);
  const siOld = getRow(23);
  const siOledNew = getRow(100); // 신모델 OLED 요약 (Sell-in)
  const siOledOld = getRow(150); // 구모델 OLED 요약 (Sell-in)

  results.push({
    sub,
    name: subNames[sub] || sub,
    // 9월 (Sep, 최신 9/21W 실적 반영)
    sep: {
      wosTTL: wosTTL[9],
      wosNew: wosNew[9],
      wosOld: wosOld[9],
      chInvTTL: chInvTTL[9],
      chInvNew: chInvNew[9],
      chInvOld: chInvOld[9],

      soTTL: soTTL[9],
      soNew: soNew[9],
      soNewRatio: soRatio[9],
      soOledNew: soOledNew[9],
      soOledOld: soOledOld[9],
      soOledTTL: (soOledNew[9] || 0) + (soOledOld[9] || 0),
      // OLED 내 신모델 비중 (Sell-out)
      oledNewRatioInOled_SO: ((soOledNew[9] || 0) + (soOledOld[9] || 0)) > 0 
        ? ((soOledNew[9] || 0) / ((soOledNew[9] || 0) + (soOledOld[9] || 0))) * 100 
        : 0,
      // 신모델 중 OLED 비중 (Sell-out)
      oledRatioInNew_SO: (soNew[9] || 0) > 0 
        ? ((soOledNew[9] || 0) / (soNew[9] || 0)) * 100 
        : 0,
      // 전체 TV 중 OLED 신모델 비중 (Sell-out)
      oledNewRatioInTotal_SO: (soTTL[9] || 0) > 0 
        ? ((soOledNew[9] || 0) / (soTTL[9] || 0)) * 100 
        : 0,

      siTTL: siTTL[9],
      siOledTTL: siOledTTL[9],
      siNew: siNew[9],
      siOledNew: siOledNew[9],
      siOledOld: siOledOld[9],
      // OLED 내 신모델 비중 (Sell-in)
      oledNewRatioInOled_SI: (siOledTTL[9] || 0) > 0 
        ? ((siOledNew[9] || 0) / (siOledTTL[9] || 0)) * 100 
        : 0,
      // 신모델 중 OLED 비중 (Sell-in)
      oledRatioInNew_SI: (siNew[9] || 0) > 0 
        ? ((siOledNew[9] || 0) / (siNew[9] || 0)) * 100 
        : 0
    },
    // 8월 (Aug)
    aug: {
      wosTTL: wosTTL[8],
      wosNew: wosNew[8],
      wosOld: wosOld[8],
      chInvTTL: chInvTTL[8],
      chInvNew: chInvNew[8],
      chInvOld: chInvOld[8],

      soTTL: soTTL[8],
      soNew: soNew[8],
      soNewRatio: soRatio[8],
      soOledNew: soOledNew[8],
      soOledOld: soOledOld[8],
      soOledTTL: (soOledNew[8] || 0) + (soOledOld[8] || 0),
      oledNewRatioInOled_SO: ((soOledNew[8] || 0) + (soOledOld[8] || 0)) > 0 
        ? ((soOledNew[8] || 0) / ((soOledNew[8] || 0) + (soOledOld[8] || 0))) * 100 
        : 0,
      oledRatioInNew_SO: (soNew[8] || 0) > 0 
        ? ((soOledNew[8] || 0) / (soNew[8] || 0)) * 100 
        : 0,
      oledNewRatioInTotal_SO: (soTTL[8] || 0) > 0 
        ? ((soOledNew[8] || 0) / (soTTL[8] || 0)) * 100 
        : 0,

      siTTL: siTTL[8],
      siOledTTL: siOledTTL[8],
      siNew: siNew[8],
      siOledNew: siOledNew[8],
      siOledOld: siOledOld[8],
      oledNewRatioInOled_SI: (siOledTTL[8] || 0) > 0 
        ? ((siOledNew[8] || 0) / (siOledTTL[8] || 0)) * 100 
        : 0,
      oledRatioInNew_SI: (siNew[8] || 0) > 0 
        ? ((siOledNew[8] || 0) / (siNew[8] || 0)) * 100 
        : 0
    }
  });
});

fs.writeFileSync('scripts/extracted_subs_data.json', JSON.stringify(results, null, 2), 'utf8');
console.log('Saved to scripts/extracted_subs_data.json successfully.');

