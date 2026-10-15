/**
 * Injects 2026 LG TV Product Lineup & Spec Database into master_data_bundle.json
 */
const fs = require('fs');
const path = require('path');

const bundlePath = path.join(__dirname, '..', 'public', 'master_data_bundle.json');
const bundle = JSON.parse(fs.readFileSync(bundlePath, 'utf8'));

const productLineup2026 = {
  title: "2026 LG TV European Product Lineup & Architecture Spec DB",
  version: "v7.5.0 1 (2026.06.24)",
  updatedAt: "2026-09-21",
  strategicPositioning: {
    overview: "2026년 유럽 TV 라인업은 초프리미엄 OLED 리더십(G6/C6/W6/B6)을 공고히 하는 동시에, 차세대 초고화질 LCD 기술인 Micro RGB(MRGB 95B, 9MB, 85B)를 신규 도입하여 100인치~50인치 전 구간에 걸친 프리미엄 지배력을 완성했습니다.",
    segments: [
      {
        segment: "4K OLED",
        brand: "LG OLED evo / OLED",
        tagline: "완벽한 블랙과 무한대 명암비의 독보적 화질 리더십",
        seriesList: ["OLED W6 (무선 플래그십)", "OLED G6 (갤러리 디자인 evo)", "OLED C6 (올라운드 베스트셀러 evo)", "OLED B6 (합리적 프리미엄 진입 모델)"],
        highlight: "α11 AI Processor 4K Gen3 with Dual AI Engine 탑재(G6/C6/W6), 165Hz VRR 게이밍 지원"
      },
      {
        segment: "4K Micro RGB (MRGB)",
        brand: "LG Micro RGB",
        tagline: "초미세 RGB LED 백라이트로 구현하는 LCD 최고봉의 색재현율 및 완벽 명암비",
        seriesList: ["MRGB 95B (100/86/75\")", "MRGB 9MB (86/75/65\" Zero Connect 무선)", "MRGB 85B (86/75/65/55/50\")"],
        highlight: "최상위 100인치 및 초대형 라인업 전개, α11/α8 AI 프로세서 탑재, 165Hz/144Hz VRR 지원"
      },
      {
        segment: "4K QNED MiniLED / QNED",
        brand: "LG QNED evo / QNED",
        tagline: "Quantum Dot + NanoCell 기술과 미니LED 백라이트의 정점",
        seriesList: ["115QNED90B (115인치 초대형 거함)", "100/86/75/65/55/50 QNED85B", "QNED82B / QNED8MB", "QNED80B / QNED70B"],
        highlight: "115인치/100인치 초대형 세그먼트 공략, α8/α7 AI Processor 탑재"
      },
      {
        segment: "4K NanoCell / UHD",
        brand: "LG NanoCell / UHD",
        tagline: "합리적 가격대의 고품질 대화면 라인업",
        seriesList: ["98/85/75/65/55/50/43 NU85", "NU80 (ODM)", "LB70 / LB65 (FHD/HD)"],
        highlight: "98인치 엔트리 대화면 및 43~32인치 서브 TV 대응"
      }
    ]
  },
  mrgbLineup: [
    {
      modelCode: "MRGB95B",
      series: "LG Micro RGB 95 Series (최상위 플래그십)",
      displayType: "4K Micro RGB",
      sizes: ["100\"", "86\"", "75\""],
      backlight: "Micro RGB (초미세 RGB 독립 백라이트)",
      refreshRate: "120Hz Native (VRR 165Hz 지원)",
      processor: "α11 AI Processor 4K Gen3 with Dual AI Engine",
      audio: "40W 2.2ch, Dolby Atmos 지원",
      features: "초대형 100인치 플래그십, 완벽 명암 제어, Dual AI 화질/음질 엔진, WebOS 26"
    },
    {
      modelCode: "MRGB9MB",
      series: "LG Micro RGB 9M Series (무선 Zero Connect 하이엔드)",
      displayType: "4K Micro RGB",
      sizes: ["86\"", "75\"", "65\""],
      backlight: "Mini RGB",
      refreshRate: "120Hz Native (VRR 144Hz 지원)",
      processor: "α11 AI Processor 4K Gen3 with Dual AI Engine",
      audio: "20W 2.0ch, Dolby Atmos 지원",
      features: "Zero Connect 무선 AV 전송 박스 지원, 케이블리스 깔끔한 인테리어 설치 특화"
    },
    {
      modelCode: "86/75/65MRGB85B",
      series: "LG Micro RGB 85 Series (대형 프리미엄 볼륨)",
      displayType: "4K Micro RGB",
      sizes: ["86\"", "75\"", "65\""],
      backlight: "Mini RGB",
      refreshRate: "120Hz Native (VRR 144Hz 지원)",
      processor: "α8 AI Processor 4K Gen3",
      audio: "20W 2.0ch, Dolby Atmos 지원",
      features: "유럽 주요 유통 주력 프리미엄 라인업, 뛰어난 가격 경쟁력 및 화질 밸런스"
    },
    {
      modelCode: "55/50MRGB85B",
      series: "LG Micro RGB 85 Series (중형 대중화 프리미엄)",
      displayType: "4K Micro RGB",
      sizes: ["55\"", "50\""],
      backlight: "Mini RGB",
      refreshRate: "120Hz Native (VRR 144Hz 지원)",
      processor: "α8 AI Processor 4K Gen3",
      audio: "20W 2.0ch, Dolby Atmos 지원",
      features: "거실/서재 타깃 고화질 RGB 백라이트 LCD, 144Hz 콘솔/PC 게이밍 최적화"
    }
  ],
  oledLineup: [
    {
      modelCode: "OLEDW6",
      series: "OLED W6 Wallpaper / Wireless",
      sizes: ["83\"", "77\""],
      processor: "α11 AI Processor 4K Gen3 (Dual AI Engine)",
      refreshRate: "120Hz (VRR 165Hz)"
    },
    {
      modelCode: "OLED97/83/77/65/55/48G6",
      series: "OLED evo G6 Series (갤러리)",
      sizes: ["97\"", "83\"", "77\"", "65\"", "55\"", "48\""],
      processor: "α11 AI Processor 4K Gen3 (Dual AI Engine)",
      refreshRate: "120Hz (VRR 165Hz)"
    },
    {
      modelCode: "OLED83/77/65/55/48/42C6",
      series: "OLED evo C6 Series (올라운드)",
      sizes: ["83\"", "77\"", "65\"", "55\"", "48\"", "42\""],
      processor: "α11 AI Processor 4K Gen3 (Dual AI Engine)",
      refreshRate: "120Hz (VRR 165Hz)"
    },
    {
      modelCode: "OLEDB6E",
      series: "OLED B6 Series (스탠다드)",
      sizes: ["83\"", "77\"", "65\"", "55\"", "48\""],
      processor: "α8 AI Processor 4K Gen3",
      refreshRate: "120Hz (VRR 120Hz)"
    }
  ]
};

if (!bundle.datasets) bundle.datasets = {};
bundle.datasets.productLineup2026 = productLineup2026;

fs.writeFileSync(bundlePath, JSON.stringify(bundle, null, 2), 'utf8');
console.log('✅ Successfully injected 2026 Product Lineup (MRGB, OLED, QNED) into master_data_bundle.json');
