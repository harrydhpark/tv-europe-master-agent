const fs = require('fs');
const path = require('path');
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  HeadingLevel,
  AlignmentType,
  BorderStyle,
  WidthType,
  ShadingType,
  Header,
  Footer,
  PageNumber,
  PageBreak
} = require('docx');

// Design Tokens
const COLOR_PRIMARY = "1A365D";   // Deep Executive Navy
const COLOR_SECONDARY = "2B6CB0"; // Classic Blue
const COLOR_ACCENT = "A50034";    // LGE Red Accent
const COLOR_DARK = "2D3748";      // Dark Slate for body
const COLOR_MUTED = "718096";     // Muted Gray
const COLOR_BG_LIGHT = "F7FAFC";  // Light Gray / White smoke
const COLOR_BG_HEADER = "EDF2F7"; // Table Header Gray / Soft Navy
const COLOR_CALLOUT_BG = "EBF8FF";// Soft Blue Callout
const COLOR_ALERT_BG = "FFF5F5";  // Soft Red Alert Box
const COLOR_BORDER = "CBD5E0";    // Crisp Border Gray

const FONT_FAMILY = "Malgun Gothic";

function p(text = "", opts = {}) {
  const {
    bold = false,
    italic = false,
    size = 20, // 10pt (in half-points)
    color = COLOR_DARK,
    spaceBefore = 80,
    spaceAfter = 80,
    align = AlignmentType.LEFT,
    lineSpacing = 280
  } = opts;

  return new Paragraph({
    alignment: align,
    spacing: { before: spaceBefore, after: spaceAfter, line: lineSpacing },
    children: [
      new TextRun({
        text,
        bold,
        italic,
        size,
        color,
        font: FONT_FAMILY
      })
    ]
  });
}

function pMulti(runs, opts = {}) {
  const {
    spaceBefore = 80,
    spaceAfter = 80,
    align = AlignmentType.LEFT,
    lineSpacing = 280
  } = opts;

  return new Paragraph({
    alignment: align,
    spacing: { before: spaceBefore, after: spaceAfter, line: lineSpacing },
    children: runs.map(r => new TextRun({
      text: r.text,
      bold: r.bold || false,
      italic: r.italic || false,
      size: r.size || 20,
      color: r.color || COLOR_DARK,
      font: FONT_FAMILY
    }))
  });
}

function bullet(boldPrefix, text, opts = {}) {
  const { size = 20, color = COLOR_DARK } = opts;
  return new Paragraph({
    spacing: { before: 60, after: 60, line: 260 },
    bullet: { level: 0 },
    children: [
      new TextRun({ text: boldPrefix + " ", bold: true, size, color: COLOR_PRIMARY, font: FONT_FAMILY }),
      new TextRun({ text: text, bold: false, size, color, font: FONT_FAMILY })
    ]
  });
}

function subBullet(boldPrefix, text, opts = {}) {
  const { size = 18, color = COLOR_DARK } = opts;
  return new Paragraph({
    spacing: { before: 40, after: 40, line: 240 },
    bullet: { level: 1 },
    children: [
      new TextRun({ text: boldPrefix + " ", bold: true, size, color: COLOR_SECONDARY, font: FONT_FAMILY }),
      new TextRun({ text: text, bold: false, size, color, font: FONT_FAMILY })
    ]
  });
}

function h1(title) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160 },
    children: [
      new TextRun({
        text: title,
        bold: true,
        size: 32, // 16pt
        color: COLOR_PRIMARY,
        font: FONT_FAMILY
      })
    ]
  });
}

function h2(title) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [
      new TextRun({
        text: title,
        bold: true,
        size: 26, // 13pt
        color: COLOR_SECONDARY,
        font: FONT_FAMILY
      })
    ]
  });
}

function h3(title) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 80 },
    children: [
      new TextRun({
        text: title,
        bold: true,
        size: 22, // 11pt
        color: COLOR_ACCENT,
        font: FONT_FAMILY
      })
    ]
  });
}

function createCallout(title, lines, isAlert = false) {
  const bgColor = isAlert ? COLOR_ALERT_BG : COLOR_CALLOUT_BG;
  const borderColor = isAlert ? COLOR_ACCENT : COLOR_PRIMARY;

  const contentParagraphs = [];
  if (title) {
    contentParagraphs.push(new Paragraph({
      spacing: { before: 40, after: 60 },
      children: [
        new TextRun({ text: title, bold: true, size: 22, color: borderColor, font: FONT_FAMILY })
      ]
    }));
  }

  lines.forEach(l => {
    if (typeof l === 'string') {
      contentParagraphs.push(new Paragraph({
        spacing: { before: 40, after: 40, line: 260 },
        children: [
          new TextRun({ text: "• " + l, size: 19, color: COLOR_DARK, font: FONT_FAMILY })
        ]
      }));
    } else {
      contentParagraphs.push(pMulti(l, { spaceBefore: 40, spaceAfter: 40 }));
    }
  });

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      bottom: { style: BorderStyle.NONE },
      left: { style: BorderStyle.SINGLE, size: 24, color: borderColor }
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            shading: { fill: bgColor, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 180, right: 180 },
            children: contentParagraphs
          })
        ]
      })
    ]
  });
}

function createStyledTable(headers, rows, colWidthPercents) {
  const tableRows = [];

  // Header Row
  const headerCells = headers.map((h, idx) => new TableCell({
    width: { size: colWidthPercents[idx], type: WidthType.PERCENTAGE },
    shading: { fill: COLOR_PRIMARY, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 100, right: 100 },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: h, bold: true, size: 19, color: "FFFFFF", font: FONT_FAMILY })
        ]
      })
    ]
  }));
  tableRows.push(new TableRow({ children: headerCells, tableHeader: true }));

  // Data Rows
  rows.forEach((row, rIdx) => {
    const isEven = rIdx % 2 === 1;
    const bgFill = isEven ? COLOR_BG_LIGHT : "FFFFFF";

    const cells = row.map((cellText, cIdx) => {
      let align = AlignmentType.LEFT;
      if (cIdx === 0 || cellText.length <= 8) align = AlignmentType.CENTER;
      if (/^[0-9,.%Δ\-↑↓]+$/.test(cellText.trim())) align = AlignmentType.RIGHT;

      return new TableCell({
        width: { size: colWidthPercents[cIdx], type: WidthType.PERCENTAGE },
        shading: { fill: bgFill, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
          bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
          left: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER },
          right: { style: BorderStyle.SINGLE, size: 4, color: COLOR_BORDER }
        },
        children: [
          new Paragraph({
            alignment: align,
            spacing: { before: 30, after: 30, line: 240 },
            children: [
              new TextRun({
                text: cellText,
                size: 18,
                bold: cIdx === 0,
                color: cellText.includes("지시") ? COLOR_ACCENT : COLOR_DARK,
                font: FONT_FAMILY
              })
            ]
          })
        ]
      });
    });

    tableRows.push(new TableRow({ children: cells }));
  });

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: tableRows
  });
}

async function buildDocx() {
  console.log("Generating Comprehensive Word Document...");

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: { font: FONT_FAMILY, size: 20, color: COLOR_DARK }
        }
      }
    },
    sections: [
      {
        properties: {
          page: {
            margin: { top: 1200, bottom: 1200, left: 1200, right: 1200 }
          }
        },
        headers: {
          default: new Header({
            children: [
              pMulti([
                { text: "LGE TV 유럽/CIS 영업담당", bold: true, size: 16, color: COLOR_MUTED },
                { text: " | 2026년 전략회의 및 PD회의 종합 분석 보고서", size: 16, color: COLOR_MUTED }
              ], { align: AlignmentType.RIGHT })
            ]
          })
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ text: "Page ", size: 16, color: COLOR_MUTED, font: FONT_FAMILY }),
                  new TextRun({ children: [PageNumber.CURRENT], size: 16, color: COLOR_MUTED, font: FONT_FAMILY }),
                  new TextRun({ text: " of ", size: 16, color: COLOR_MUTED, font: FONT_FAMILY }),
                  new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: COLOR_MUTED, font: FONT_FAMILY })
                ]
              })
            ]
          })
        },
        children: [
          // COVER / TITLE
          p("TV 유럽영업 전략 기획 시리즈", { bold: true, size: 24, color: COLOR_ACCENT, spaceAfter: 100 }),
          p("2026년 LGE TV 유럽 전략회의 및 PD회의 종합 분석 보고서", {
            bold: true,
            size: 44, // 22pt
            color: COLOR_PRIMARY,
            spaceAfter: 140
          }),
          p("시계열(0202 전략회의 → 0414 PD회의 → 0520 전략회의 → 0818 PD회의 → 0922 전략회의) 논의 사안 및 유럽 공통·법인별 실행 로드맵", {
            italic: true,
            size: 22,
            color: COLOR_MUTED,
            spaceAfter: 240
          }),

          // METADATA BOX
          createCallout("보고서 기본 정보 및 문서 개요", [
            "주관 부서: TV 유럽/CIS 영업담당, MS본부 디스플레이 해외영업그룹, TV Europe Master AI Agent",
            "분석 대상 회의체: 2026년 진행된 전사 5개 공식 회의체 원천 자료 및 16~17개 전 판매법인/지점 발표 데이터",
            "적용 프레임워크: 4대 핵심 전략 축 (① OLED 프리미엄 사수, ② QNED/볼륨존 방어 및 경쟁 대응, ③ 유통 Flooring 및 WOS 재고 건전화, ④ 판가/손익 및 D2C 마컴)",
            "작성 목적: 2026년 상반기 NPI 출시부터 하반기 성수기(Black Friday/Boxing Day) 및 2027년 1분기 선행 사업에 이르는 본부·지역 의사결정과 액션 아이템의 완전한 추적 및 실행 지원"
          ]),

          p("", { spaceAfter: 200 }),

          // EXECUTIVE SUMMARY
          h1("EXECUTIVE SUMMARY (경영진 핵심 요약)"),
          p("2026년 LGE 유럽 TV 사업은 글로벌 거시경제 불확실성, 패널 및 메모리 부품 원가 상승 압박, 그리고 중국계 브랜드(TCL, Hisense)와 경쟁사(삼성 QD-OLED)의 공격적 판가 공세 속에서 '흑자 달성'과 '한계돌파'를 최우선 과제로 추진하였습니다. 1년 동안 진행된 5개 회의체(3회 전략회의, 2회 PD회의)의 논의 흐름은 다음과 같은 명확한 전략적 진화를 보여줍니다.", { spaceAfter: 120 }),

          bullet("2월 전략회의 (턴어라운드 원점 정립):", "2025년 부진(경쟁사 게임플랜 센싱 미흡, EOL 구모델 롱테일 운영 실패, 손익 적자)을 통렬히 반성하고, 2026년 최고 KPI를 '흑자 달성'으로 선포하였습니다. OLED의 기술 격차 축소에 대응해 W(무선) 및 G 시리즈 중심 프리미엄 판매 집중을 지시하고, LCD 부문에서도 MiniLED 적용 변형 모델(QNED7M) 투입 및 QNED 카테고리의 MiniLED 재분류를 추진하였습니다."),
          bullet("4월 PD회의 (신모델 NPI 램프업 & 실행력 총결집):", "상반기 신모델 본격 출시 시점에 맞춰 본부 GTM실 및 D2C팀과 연계하여 전 유럽 런칭 전략을 수립하였습니다. 신모델 출시 Net 가격을 전년비 동등/개선하고, EOL 구모델을 빠르게 소진하여 매장 진열(Flooring) 점유율을 선점하는 데 총력을 기울였습니다."),
          bullet("5월 전략회의 (상반기 중간 평가 및 하반기 수정보완):", "1분기 실적과 2분기 초 판가 동향을 점검하고, OLED B시리즈에 대한 과도한 물량 쏠림을 방지하며 C/G 시리즈 상향 판매 믹스를 점검하였습니다. 또한 중국계의 초대형(85\"↑) MiniLED 저가 공세에 대응한 QNED85/90 방어선을 구축하였습니다."),
          bullet("8월 PD회의 (유럽 신모델 ATA 열세 반전 & 성수기 총력전):", "신모델의 경쟁사 대비 실거래가(ATA) 열세를 심각한 위기로 진단하고, 무분별한 SOA/인하 대신 캐시백(Cashback) 프로세스 내재화와 USED 차감율 25% 이하 통제를 결의하였습니다. 아울러 4분기 블랙프라이데이/박싱데이 대비 SCM 단기 증량과 2027년 PRM(True RGB 대응)을 사전 조율하였습니다."),
          bullet("9월 전략회의 (2026 연간 마무리 & 2027 선제 대응):", "본부장 주재 하에 'ATA 개선은 TV 사업 영속을 위한 절대 절명의 과제'로 재차 강조되었습니다. 9~12월 판가 인상 $11.1M 완료 및 추가 개선 $37M을 반영하였으며, 연말 유통재고 630천대(WOS 5.7주)를 엄격히 통제하기로 하였습니다. 또한 차세대 MRGB 전시를 2026년 9.4천대에서 2027년 34.7천대(판매 673천대)로 6배 이상 대폭 확대하는 미래 성장 드라이브를 확정하였습니다."),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 1
          h1("CHAPTER 1. 2026년 2월 유럽 전략회의 (2026.02.02)"),
          h2("1.1 회의 개요 및 핵심 배경"),
          p("2026년 2월 2일 진행된 본부-유럽지역 전략회의는 MS본부장, 디스플레이사업부장, 해외영업그룹장, TV유럽/CIS영업담당 및 팀장들이 대거 참석한 가운데 열렸습니다. 2025년 유럽 TV 실적 부진에 대한 철저한 원인 규명과 함께, 2026년을 흑자 턴어라운드의 원년으로 만들기 위한 사업 체질 개선안이 집중 논의되었습니다.", { spaceAfter: 100 }),

          createCallout("2월 전략회의 핵심 의사결정 프레임", [
            "2025년 부진 반성: 경쟁사의 EOL 롱테일 운영 및 조기 NPI 램프업에 대한 시장 센싱 실패로 3분기 M/S 급락 발생",
            "2026년 최우선 KPI: '흑자 달성' - 매출과 손익의 최적 밸런스 확립 및 한계돌파(SG M/S 초과) 목표 전개",
            "가격 건전성 확립: 신모델 출시 Net 가격은 전년비 동등 이상 사수, 월별 SOA 예산 사전 수립·리뷰 체계 도입"
          ]),

          p("", { spaceAfter: 100 }),
          h2("1.2 유럽 공통 4대 전략 추진과제"),
          bullet("① OLED / 프리미엄 지배력 사수:", "OLED 기술 격차 축소 우려에 대해 3월까지 중장기 프리미엄 전략 Stance를 CEO에게 보고하기로 결정. 인치/시리즈별 한계이익률 Matrix 분석을 기반으로 고수익 시리즈로 물량을 전환하고, 83인치 등 대형은 재료비 인상폭이 적은 W(무선)로 판매 집중. 무선 OLED(W) 확판을 위한 전담 GTM Task 신설."),
          bullet("② QNED / 볼륨존 방어 및 경쟁 대응:", "OLED 외에 LCD에서도 이길 수 있는 체계 구축 지시. QNED 및 UHD 라인업의 실판매 부진 원인을 정밀 분석하고, 하반기 QNED70의 MiniLED 변형 모델인 QNED7M을 신규 투입하되, 원가 개선형인 QNED70도 병행 유지. 유통 Assortment 및 마컴 연계를 위해 QNED 이상 카테고리의 MiniLED 분류를 본사와 협의."),
          bullet("③ 유통 커버리지 및 매장 진열(Flooring) 극대화:", "NPI 신모델의 초기 매장 침투율(Flooring)을 극대화하기 위한 유통 마진 Deal 준비 선결. Distributor 채널에 대한 제품 라인업, 판가, PSI 오퍼레이션 프로세스를 전면 쇄신하여 공급망 혼선 방지."),
          bullet("④ 판가 운영 · 손익 사수 및 360도 마컴 강화:", "Winning PRM은 경쟁력뿐 아니라 손익 개선을 필수 담보하도록 모델/유통별 세부 계획 수립. 360도 길목잡기(Conquest) 마케팅을 전개하여 NPI 핵심 소구 포인트를 법인에 지원하고, 법인은 경쟁사 채널 활동을 실시간 센싱."),

          p("", { spaceAfter: 100 }),
          h2("1.3 지점 및 법인별 현안 및 지시사항"),
          p("전략회의에서는 특히 오퍼레이션 이슈와 손익 적자가 큰 주요 법인들에 대해 맞춤형 개선안 수립이 지시되었습니다."),
          createStyledTable(
            ["법인/지점", "구분", "주요 현안 및 지시사항", "후속 조치 (Follow-up)"],
            [
              ["영국(UK)", "지시", "OLED API 하락 대비 판매지수 하락이 더 큰 원인 규명 (경쟁사 매장전시 및 커버리지 확대 가능성 정밀 분석 및 GTM 개선)", "유럽영업담당 / UK 법인"],
              ["포르투갈(PT)", "지시", "영국과 동일하게 OLED 지표 급락 법인으로 분류되어, 유통 Flooring 점검 및 현지 경쟁 대응안 수립", "유럽영업담당 / PT 법인"],
              ["독일/프랑스/이태리", "지시", "판매법인의 고정비 절감 진척 현황 재점검 및 흑자 턴어라운드를 위한 오퍼레이션 개선안 수립", "MS 원가팀 / 해당 법인"],
              ["유럽 전 법인", "공통", "내부 정기 회의체(S&OP, SOM/GTM 등)에서 경쟁 동향(판가, 전시, 프로모션) 정기 논의 및 본부 지원 데이터 연계", "전 법인장 / PD"]
            ],
            [20, 15, 45, 20]
          ),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 2
          h1("CHAPTER 2. 2026년 4월 유럽 PD 회의 (2026.04.14)"),
          h2("2.1 회의 개요 및 NPI 런칭 로드맵"),
          p("2026년 4월 14일 개최된 유럽 TV PD회의는 2026년형 신모델(OLED B6/C6/G6/M6, QNED80/85/90/MRGB)의 본격 매장 출시(ATS)를 앞두고, 유럽 본부 전략팀, GTM실, D2C팀, 그리고 유럽 16개 판매법인/지점 PD들이 집결하여 런칭 플랜을 확정하였습니다.", { spaceAfter: 100 }),

          h2("2.2 유럽 공통 4대 전략 추진과제 (HQ / GTM / D2C)"),
          bullet("① 신모델 판가 로드맵 확정:", "'0414_유럽 신모델 가격 계획'에 따라 모델별 권장소비자가격(RRP)과 초기 프로모션 판가를 셋업. 출시 초기 과도한 가격 인하를 금지하고 Net 가격을 전년 동급 모델 대비 동등 수준 이상으로 방어."),
          bullet("② GTM 매장 실행력 극대화:", "경쟁사 대비 NPI Ramp-up 속도를 2주 이상 앞당기기 위해 주요 유통사 골든존 진열 점유율을 4월 내 60% 이상 선점. EOL 구모델은 패키지 딜 및 로컬 프로모션을 통해 5월 중순까지 90% 이상 클리어런스 완료."),
          bullet("③ D2C(OBS) 자사몰 직판 체계 강화:", "자사몰을 통한 고수익 프리미엄 라인업(G시리즈, 대형 QNED) 판매 비중을 확대. 오프라인 유통과의 마찰을 회피하기 위해 온라인 단독 사양(BOD) 모델 및 멤버십 전용 케어 패키지 운영."),
          bullet("④ 유통 재고 및 WOS 사전 통제:", "신모델 입고와 구모델 소진이 맞물리는 4~5월 전환기 동안 채널 전체 재고 주수(WOS)가 7주를 초과하지 않도록 주간 단위 SCM 모니터링 강화."),

          p("", { spaceAfter: 100 }),
          h2("2.3 5대 메이저 법인 & 스위스/베네룩스 심층 실행과제"),
          bullet("독일(DG):", "MediaMarktSaturn(MMS) 매장 내 신모델 진열 선점. 특히 베를린/뮌헨 플래그십 매장에 OLED 단독 존 구축. Amazon의 알고리즘 가격 매칭으로 인한 오프라인 매장 가격 붕괴를 막기 위해 온라인 유통가 방어선 구축."),
          bullet("영국(UK):", "Currys와 2026년 신규 T&C 협상 타결 후 NPI 라인업 확정. John Lewis 백화점 채널 내 프리미엄 OLED(G6/C6) Floor Share 사수. Argos 향 중소형 QNED 라인업 확대."),
          bullet("프랑스(FS):", "Fnac/Darty 연합과의 공동 마케팅 계약 갱신. Boulanger 매장 내 라이프스타일 TV(스탠바이미) 연계 복합 진열 추진. 유통 지원금(SOA)의 무분별한 집행을 차단하고 실판가 중심 관리."),
          bullet("스페인(ES):", "MediaMarkt Spain 및 El Corte Ingles 대상 프로모션 전개. 경쟁사(삼성 S90/S95)의 공격적 가격 인하에 대응하여 맞춤형 캐시백 파일럿 프로그램을 가동하고 Price Gap을 100유로 이내로 방어."),
          bullet("이태리(IS):", "Unieuro 및 MediaWorld 중심의 전시 지수 확대. 남부 로컬 유통의 난매로 인한 가격 교란 차단. 2025년 부진했던 OLED 천만대 캠페인을 계승하여 올레드 대세화 마케팅 재시동."),
          bullet("베네룩스(BN):", "Coolblue 등 이커머스 강세 채널과 전통 오프라인 채널(BCC, Expert) 간 공급 밸런스 유지. 물류비 및 창고 보관료 절감을 위한 직배송 체계 확대."),
          bullet("스위스(Swiss):", "초고소득 시장 특성을 살려 65/77인치 이상 OLED G/M 시리즈 및 스탠바이미 프리미엄 번들링 집중. MediaMarkt, Interdiscount, Fust 3대 채널의 가격 왜곡 모니터링."),

          p("", { spaceAfter: 100 }),
          h2("2.4 기타 9개 지역 법인 핵심 현안 및 과제 종합 매트릭스"),
          createStyledTable(
            ["법인/지점", "핵심 현안 (Market Issue)", "중점 추진 과제", "목표 지표"],
            [
              ["체코/슬로바키아(CK)", "Alza, Datart 등 로컬 이커머스 판가 경쟁 심화", "중소형 QNED 및 Entry UHD 볼륨 유지하면서 한계이익 방어", "손익 흑자 유지"],
              ["폴란드(PL)", "Mława 생산기지 인접에도 불구하고 저가 TV 비중 과다", "Euro RTV AGD, Media Expert 대상 55\"↑ OLED 믹스 개선", "OLED 비중 25%↑"],
              ["헝가리(HS)", "극심한 인플레이션 및 포린트(HUF) 환율 약세", "환율 변동을 감안한 판가 슬라이딩제 및 보수적 재고 운영", "WOS 6주 이하"],
              ["루마니아(RO)", "eMAG 온라인 채널 독점에 따른 마진 압박", "Altex 오프라인 채널과의 경쟁 구도 형성 및 신모델 패키지 공급", "ASP 전년비 +5%"],
              ["포르투갈(PT)", "Worten 채널 내 삼성의 독점적 프로모션 공세", "OLED C시리즈 집중 육성 및 카카오/통신사 번들 딜 발굴", "M/S 25% 사수"],
              ["오스트리아(AG)", "독일 법인과의 가격 Gap에 따른 Cross-Border 유입", "독일 MMS와 가격 동기화 및 Mediamarkt AT 단독 프로모션", "가격 차이 3% 이내"],
              ["그리스(MK)", "Kotsovolos(Currys 자회사) 중심 유통 과점", "관광 시즌(여름) 호텔/상업용 B2B 연계 TV 수요 선점", "B2B 매출 20%↑"],
              ["동유럽/발틱(LA)", "소규모 다국가 분산으로 인한 물류 비효율", "중앙 허브 창고 기반 풀필먼트 및 표준 라인업 집약", "물류비 -10%"],
              ["노르딕(SW)", "Elkjøp, Power 2대 유통 체인의 강력한 구매력 행사", "초대형 QNED 및 MiniLED 라인업 확대로 프리미엄 입지 강화", "75\"↑ M/S 1위"]
            ],
            [18, 32, 35, 15]
          ),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 3
          h1("CHAPTER 3. 2026년 5월 유럽 전략회의 (2026.05.20)"),
          h2("3.1 회의 개요 및 상반기 실적 중간 점검"),
          p("2026년 5월 20일 열린 지역전략회의에서는 1분기 결산 결과와 함께 2분기 주요 글로벌 스포츠 이벤트(월드컵 등) 및 여름 비수기를 앞둔 사업 운영 방향성이 논의되었습니다. 1분기 흑자 기조를 확인하였으나, 하반기 부품 원가 상승과 수요 둔화 조짐이 감지됨에 따라 선제적인 리스크 관리가 주문되었습니다.", { spaceAfter: 100 }),

          h2("3.2 유럽 공통 4대 전략 추진과제 (하반기 게임플랜)"),
          bullet("① OLED 믹스 건전화 (B시리즈 쏠림 억제):", "NPI 출시 후 보급형인 B시리즈의 판매 비중이 급격히 증가하여 전체 OLED ASP를 하락시키는 문제점 지적. C시리즈 및 G시리즈로의 업셀링(Up-selling) 마케팅을 강화하고, B시리즈 공급량에 상한선(Cap)을 설정하는 방안 검토 착수."),
          bullet("② QNED / MRGB 초대형 라인업 방어벽 구축:", "TCL과 하이센스가 85인치, 98인치 MiniLED를 파괴적인 가격에 쏟아내는 상황에 대응하여, 자사 QNED85/90의 화질 엔진(알파 AI 프로세서) 및 프리미엄 디자인 소구를 강화. 하반기 예정된 QNED7M 출시 준비 점검."),
          bullet("③ 유통 재고 클린컷(Clean-Cut) 완료:", "2분기 말까지 2025년 EOL 구모델 재고를 전 유럽 매장에서 완전 소진(Zero Remainder)할 것을 결의. 남아있는 구모델에 대해서는 제한적 차감 지원을 통해 조기 청산."),
          bullet("④ 패널 및 원가 상승에 대응한 판가 방어:", "하반기 LCD 패널 가격 및 메모리 반도체 가격 상승 공문이 접수됨에 따라, 하반기 프로모션 예산을 사전 재계산하고 무분별한 블랙프라이데이 가격 덤핑을 금지하는 가이드라인 수립."),

          p("", { spaceAfter: 100 }),
          h2("3.3 지점 및 법인별 중점 관리 지시사항"),
          bullet("서유럽 5대 법인(DG, UK, FS, ES, IS):", "2분기 대형 프로모션 종료 직후 매장 내 잔여 구모델 재고 실사 진행. 신모델 Flooring 달성률 80% 미만 유통사에 대한 영업 지원금 패널티 연계 검토."),
          bullet("동유럽/신흥 법인(PL, HS, RO, CK):", "현지 통화 환율 급변동에 따른 Net 매출 누수를 막기 위해 유통사와의 납품 계약 시 유로화 연동 단가 기준을 엄격히 적용."),
          bullet("스위스/노르딕 지점:", "고환율(CHF) 수혜를 극대화하여 2분기 중 최고 수준의 한계이익률을 달성할 것과 스탠바이미 2세대 런칭을 통한 신규 시장 창출 지시."),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 4
          h1("CHAPTER 4. 2026년 8월 유럽 PD 회의 (2026.08.18)"),
          h2("4.1 회의 개요 및 성수기 총력 체제 가동"),
          p("2026년 8월 18일, 프랑스 파리 법인 회의실과 화상(WebEx)을 연결하여 진행된 8월 PD회의는 본부 디스플레이 해외영업그룹장, TV유럽/CIS영업담당, TV SCM팀, 상품기획팀, 그리고 17개 판매법인/지점 PD 및 리더십이 총집결한 가장 치열한 회의였습니다. 연간 승패를 결정지을 4분기 블랙프라이데이(BF) 및 박싱데이(Boxing Day) 총력전이 선포되었습니다.", { spaceAfter: 100 }),

          createCallout("8월 PD회의 주요 점검 및 지시 아젠다", [
            "위기 진단: 유럽 신모델 실판매 가격(ATA)이 경쟁사 대비 심각하게 열세인 상황 확인 → 하반기 반드시 반전 지시",
            "판가 정책 전환: 4분기 무분별한 판가 인하 지양, 경쟁사 가격/캐시백에 맞춘 정밀 캐시백(Cashback) 프로세스 전사 가동",
            "카테고리 선점: GfK 내 MRGB 8시리즈를 'RGB Mini' 카테고리에 포함되도록 본사 지원실-GfK 공식 협상 추진",
            "4분기 SCM: 연말 물동 증량에 대비한 사전 선적 및 2027년 상반기 DM(수요 예측) 선행 입력"
          ], true),

          p("", { spaceAfter: 100 }),
          h2("4.2 유럽 공통 4대 전략 추진과제"),
          bullet("① ATA(실거래가) 열세 극복 및 캐시백 내재화:", "신모델 ATA 지수가 경쟁사 대비 하락하여 브랜드 가치 및 마진이 훼손되고 있음을 엄중 경고. 송장가(Invoice Price)를 깎는 대신 소비자 대상 다이렉트 캐시백을 운영하여 매장 노출 가격을 지키고, 리뷰 확보와 실판매 촉진을 동시 달성 지시."),
          bullet("② QNED / MRGB 차별화 및 SKU 효율화:", "QNED를 단순히 MRGB로 대체하지 말고, QNED 순수 증량 기회를 발굴할 것 지시. 스웨덴 PD의 QNED7 Variation 확대 요청에 대해, 경쟁사도 라인업을 축소하고 있으므로 불필요한 SKU 증설보다는 핵심 모델에 마케팅을 집중할 것 결정. 2027년 소니의 True RGB 강화에 대비해 Mini/Micro RGB 구조 차별화 포인트 사전 정립."),
          bullet("③ 성수기 4분기 PSI 및 SCM 비상 대응:", "SCM팀은 4분기 단기 증량 발생 시 선박/항공 스페이스 부족이 없도록 비상 대응책 마련. 각 법인은 2027년 상반기까지 DM을 미리 입력하여 EOL 모델과 NPI 모델 간 생산 라인 전환에 차질이 없도록 조치."),
          bullet("④ 손익(PnL) 및 USED 차감율 25% 이하 관리:", "수년간 누적 상승한 매출 차감율(SD Rate)을 25% 이하로 낮추기 위한 고강도 비용 통제. 각 법인은 유통사에 제공하는 가판비, 리베이트, 인스토어 프로모션 비용의 투자 대비 효과(ROI)를 전수 재검토."),

          p("", { spaceAfter: 100 }),
          h2("4.3 5대 메이저 법인 & 주요 지점 심층 실행과제"),
          bullet("독일(DG):", "높은 TT(Target Total) 구조 탈피를 위해 USED 집행 금액을 전년비 연간 $18.9M 대폭 축소 계획 확정. 10월 적자폭 축소를 위한 단기 판가 조정 검토. MRGB85 적극 확대 및 Expert 유통 향 선제 공급."),
          bullet("영국(UK):", "Currys 향 4분기 물량 중 약 $5M을 2027년 1월 판매분으로 사전 반영하여 박싱데이와 1월 정기 세일 탄력 운영. BOD 조정에 따른 SA Gap 전량 만회. 경쟁사의 B2B 대형 딜이 GfK 온라인 실적으로 왜곡 반영되는 현상 규명 요청."),
          bullet("스페인(ES):", "헐리우드 영화감독 연계 OLED 캠페인 진행을 위한 광고비 증액 요청에 대해, MS마컴은 'Perfect Black' 글로벌 통일 메시지 검토 지시. 1억 불이 넘는 가판비/영업비용의 효율성을 철저히 검증 후 집행."),
          bullet("이태리(IS):", "B시리즈 가격 인하 최소화 방안 수립. GfK 내 MRGB8 카테고리 반영 본사 지원 요청. 엔트리 UHD 물량 감소 예측 재점검 및 QNED8M/75QNED70B 증량 요청."),
          bullet("스웨덴/노르딕(SW):", "MRGB90 시리즈의 1폴 스탠드 고급화 개발 요청. 경쟁사 M70 대응을 위한 라인업 경쟁력 강화."),
          bullet("스위스(Swiss):", "Aus unserer Werbung 등 주요 유통 프로모션 시 덤핑 방지 및 65C67 등 전략 모델의 가격 정합성 상시 감사 체계 확립."),

          p("", { spaceAfter: 100 }),
          h2("4.4 17개 전 법인/지점 4분기 성수기 액션 아이템 요약 매트릭스"),
          createStyledTable(
            ["법인/지점", "4분기 핵심 타깃", "가격 및 프로모션 전략", "SCM / 재고 통제"],
            [
              ["독일(LGEDG)", "USED $18.9M 절감", "9~10월 선별 인하, 10월 적자 축소", "Expert 선제 공급, 연말 재고 정상화"],
              ["영국(LGEUK)", "Currys $5M 1월 롤오버", "BF 전년비 동가 이상, Boxing Day 탄력", "SA Gap 전량 만회, BOD 엄격 준수"],
              ["스페인(LGEES)", "1억불 가판비 효율화", "ATA 동등 운영, 캐시백 적극 가동", "MediaMarkt/ECI 믹스 고도화"],
              ["이태리(LGEIS)", "B시리즈 인하 최소화", "QNED 순수 증량, 캐시백 파일럿", "75QNED70B 증량 배정"],
              ["프랑스(LGEFS)", "Fnac/Darty 마진 개선", "OLED/QNED 복합 딜, 인하 축소", "WOS 5.5주 수준 통제"],
              ["베네룩스(LGEBN)", "온-오프 마진 방어", "Coolblue 프라이스 매칭 방어", "연말 재고 클린컷"],
              ["노르딕(LGESW)", "MRGB90 고급화 선점", "Elkjøp 전용 SKU 및 1폴 스탠드 소구", "27년 ATS 4월 조기 공급 요청"],
              ["스위스(Swiss)", "초고수익 PnL 사수", "MediaMarkt 1,599 CHF 가격 정합 유지", "G/W 프리미엄 완제품 중심"],
              ["체코(LGECK)", "Alza 채널 마진 개선", "로컬 가격 덤핑 금지, 캐시백 적용", "중앙 풀필먼트 연계"],
              ["폴란드(LGEPL)", "OLED 대형 믹스 확대", "Euro RTV 프로모션 차감율 통제", "Mława 직송 리드타임 단축"],
              ["헝가리(LGEHS)", "환율 리스크 헷지", "HUF 판가 방어, 저수익 모델 축소", "안전재고 최소화"],
              ["루마니아(LGERO)", "Altex 오프라인 진열", "eMAG 독점 견제 프로모션", "WOS 5주 이내 엄수"],
              ["포르투갈(LGEPT)", "OLED C시리즈 집중", "Worten 공동 펀딩 프로모션", "재고 회전율 15% 개선"],
              ["오스트리아(LGEAG)", "독일 역유입 차단", "독일 MMS 판가 연동 동기화", "AT 전용 물동 배분"],
              ["그리스(LGEMK)", "B2B 잔여 수요 소진", "Kotsovolos 연말 프로모션 사수", "상업용/소비자용 밸런스"],
              ["발틱/동유럽(LGELA)", "물류비 절감 극대화", "핵심 SKU 집중, 마진 저조 모델 단종", "광역 허브 통합 운영"]
            ],
            [15, 25, 35, 25]
          ),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 5
          h1("CHAPTER 5. 2026년 9월 유럽 전략회의 (2026.09.22)"),
          h2("5.1 회의 개요 및 4분기 마무리 & 2027년 선제 사업 논의"),
          p("2026년 9월 22일, MS본부장 주재로 본부 경영진과 유럽 전 판매법인장 및 지점장이 전원 참석한 가운데 마라톤 화상 전략회의가 진행되었습니다. 2026년 연간 실적 전망을 최종 확정하고, 2027년 부품 원가(메모리/패널) 상승에 맞선 2027년 1분기 선제적 사업 준비가 본 회의의 핵심 아젠다였습니다.", { spaceAfter: 100 }),

          createCallout("9월 전략회의 본부장 핵심 지시사항", [
            "【ATA 절대 사수】: ATA 개선을 TV 사업의 영속을 위한 절대 절명의 과제로 여기고 반드시 반전시킬 것",
            "【원가 상승 방어】: 2027년 메모리 가격 인상에 대비하여 9~12월 판가 인상 $11.1M 완료 및 추가 개선 $37M을 10월차 이동 계획에 100% 반영할 것",
            "【MRGB 대폭 확대】: 2026년 MRGB 전시 9.4천대(판매 103천대) → 2027년 전시 34.7천대, 판매 673천대로 6배 이상 대확대할 것",
            "【연말 재고 통제】: 연말 유통재고 630천대, WOS(+8W) 5.7주를 절대 엄수하여 건전성을 확보할 것"
          ], true),

          p("", { spaceAfter: 100 }),
          h2("5.2 유럽 공통 4대 전략 추진과제"),
          bullet("① 2026 연간 목표 확정 및 OLED 수익성 방어:", "2026년 유럽 TV 연간 수량 5,121천대(전년비 -7%), 순매출 $2,672M, 영업이익 $92.5M 달성 전망. OLED는 연간 1,485천대를 사수하되 저수익 모델 공급을 중단하고 고마진 시리즈 판매로 전환."),
          bullet("② 차세대 MRGB 전시 및 검색광고 드라이브:", "지역대표의 요청을 수용하여 4분기 유럽 7개국 대상 MRGB 검색광고 예산 확정. 전 법인은 9월 내 매장 진열(Flooring)을 100% 완료하고 4분기 마컴 및 GTM 활동 집중. 2027년 전시 목표 34.7천대 달성을 위한 선행 투자 확정."),
          bullet("③ ATA 개선을 위한 캐시백 프로세스 전사 내재화:", "본부장 지시로 ATA 개선이 최우선 전략 과제로 격상. 캐시백의 3대 효과(① 판촉 비용 효율화, ② 양질의 온라인 리뷰 확대, ③ 실거래가 ATA 개선)를 전 법인에 전파하고 GfK 주간/월간 데이터를 통해 즉각적인 시정 조치(Corrective Action) 실행."),
          bullet("④ EOL-NPI 전환 최적화 및 2027년 일정 조기화:", "구모델 판가 인하폭을 대폭 축소하여 구모델 손익을 지키고, 신모델은 신/구 가격 차이를 좁혀 Ramp-up 기간 단축. 2027년 신모델 재료비 개선이 예상되므로 2027년 NPI 출시 일정을 현 계획 대비 앞당길 것(Pull-in) 지시."),

          p("", { spaceAfter: 100 }),
          h2("5.3 지점 및 법인별 중점 실행과제 & 본부 합의안"),
          bullet("독일(DG):", "독일 소비자 평가기관 Stiftung Warentest(Stiwa/CMR) 화질 평가 개선을 위해, 독일향 QNED7 공급물량에 대해 VA패널 적용 검토 지시 [본부장]."),
          bullet("영국(UK):", "Currys와 체결한 신규 T&C 기반 하에 사업을 성공적으로 안착시키되, 비용율이 증가된 구조이므로 고수익 제품 Mix 개선을 통해 손익을 반드시 확보할 것 [본부장]. 2027년 T&C 재협의 시 유통 요구가 추가 상승하지 않도록 수시 협의."),
          bullet("스페인(ES):", "스페인 법인장의 독자적 기술 메시지 소구 요청에 대해, 스페인을 'Test Market'으로 삼아 마컴과 협의하여 신규 브랜드 네이밍을 시도해 볼 것 승인 [본부장]. 법인 주도의 선제적 광고비 집행 검토."),
          bullet("이태리(IS):", "UNIEURO 향 OLED 판매 지속 성장을 위한 본부 차원의 PMS(Product Management Session) 현지 지원 확정. GfK 리포트 내 MRGB8 제품의 RGB 카테고리 등재 신속 추진."),
          bullet("노르딕(SW):", "2027년 MRGB 판매 모멘텀을 유지하기 위해 2027년형 MRGB90C 시리즈의 매장 출시(ATS)를 당초 8월에서 4월로 전격 Pull-in 추진 합의."),
          bullet("스위스(Swiss):", "2027년 사업계획 수립 시 프리미엄 OLED(G/W)와 스탠바이미 비중을 유럽 최고 수준으로 편성하고, 환율 안정성에 기반한 마진율 극대화 지속."),

          new Paragraph({ children: [new PageBreak()] }),

          // CHAPTER 6
          h1("CHAPTER 6. 2026 시계열 통합 실행 타임라인 & 종합 관리 매트릭스"),
          h2("6.1 유럽 공통 4대 축 시계열 진화 및 변천사 총괄 비교표"),
          createStyledTable(
            ["전략 축", "0202 전략회의 (출발)", "0414 PD회의 (런칭)", "0520 전략회의 (중간점검)", "0818 PD회의 (성수기준비)", "0922 전략회의 (완성/차기)"],
            [
              [
                "① OLED / 프리미엄",
                "W/G 판매 집중\n중장기 Stance 보고\n무선 GTM Task",
                "신모델 판가 확정\n초기 RRP 사수\nNet Price 방어",
                "B시리즈 과다 방지\nC/G 상향 믹스\n경쟁사 가격 추적",
                "ATA 열세 반전 지시\n캐시백 전사 도입\nB시리즈 인하 최소화",
                "연간 1,485K 사수\n저수익 모델 단종\nATA TV영속 절대과제"
              ],
              [
                "② QNED / MRGB",
                "LCD에서 이기기\nQNED7M 신규 투입\nMiniLED 분류 추진",
                "매장 진열 선점\n경쟁사比 2주 선행\n초대형 85\"+ 런칭",
                "중국계 저가 공세 방어\nQNED85/90 사수\n7M 출시 점검",
                "GfK 카테고리 등재\nQNED 순수 증량\nTrue RGB 차별화",
                "MRGB '27년 6배 확대\n(9.4K→34.7K 전시)\n7개국 검색광고"
              ],
              [
                "③ 유통 / Flooring / WOS",
                "Flooring 마진 딜\nDistributor 프로세스\nNPI Ramp-up 가속",
                "골든존 진열 60%↑\n구모델 5월 청산\nWOS 7주 통제",
                "상반기 구모델 완판\n매장 실사 진행\nWOS 5~6주 유지",
                "유통 차별화 SKU\nSCM 4Q 비상 증량\n'27년 DM 선입력",
                "Flooring 9월 완결\n연말재고 630K 통제\nWOS(+8W) 5.7주"
              ],
              [
                "④ 판가 / 손익 / D2C",
                "연간 '흑자 달성'\nSOA 사전 예산제\n360도 길목잡기",
                "Net 판가 전년비 동등\nD2C 자사몰 확대\n온라인 BOD 운영",
                "원가 인상 선제 반영\n블프 덤핑 방지\n분기 손익 재계산",
                "USED 25% 이하 통제\n독일 USED $18.9M 절감\n할리우드 영상 검토",
                "판가 인상 $11.1M 완료\n추가 $37M 전사 반영\n스페인 Test Market"
              ]
            ],
            [15, 17, 17, 17, 17, 17]
          ),

          p("", { spaceAfter: 140 }),
          h2("6.2 16~17개 전 법인/지점 통합 액션 아이템 트래커"),
          p("본 트래커는 2026년 진행된 5개 회의체에서 도출된 전 법인/지점의 실행 과제와 본부 지시사항을 통합 관리하기 위한 전사 관리 대장입니다."),
          createStyledTable(
            ["법인", "회의체", "핵심 현안 및 논의 사안", "확정된 추진과제 및 완료 기준", "주관 부서"],
            [
              ["독일(DG)", "0818/0922", "높은 TT 구조 및 CMR(Stiwa) 화질 평가", "USED $18.9M 절감, 독일향 QNED7 VA패널 공급 검토", "법인장 / 상품기획"],
              ["영국(UK)", "0202/0818/0922", "Currys 신규 T&C 및 API 하락", "1월 물량 $5M 롤오버, Mix 개선으로 마진 확보", "UK 법인 / SCM"],
              ["프랑스(FS)", "0414/0818", "Fnac/Darty 마진 및 스탠바이미 결합", "공동 마컴 강화, WOS 5.5주 준수, 실판가 방어", "FS 법인 / GTM실"],
              ["스페인(ES)", "0818/0922", "가판비 1억불 효율화 및 브랜드 네이밍", "스페인 Test Market 신규 네이밍, 캐시백 프로세스", "ES 법인 / MS마컴"],
              ["이태리(IS)", "0818/0922", "Unieuro OLED 성장세 및 MRGB 등재", "본부 PMS 지원, B시리즈 인하 최소화, 75QNED 증량", "IS 법인 / 지원실"],
              ["베네룩스(BN)", "0414/0818", "Coolblue 가격 매칭 및 고정비 절감", "온-오프 옴니채널 마진 사수, 연말 재고 클린컷", "BN 법인 / 유럽영업"],
              ["스웨덴(SW)", "0818/0922", "MRGB90 스탠드 고급화 및 ATS 조기화", "1폴 스탠드 개발 반영, '27년 90C ATS 4월 댕김", "SW 법인 / 상품기획"],
              ["스위스(Swiss)", "0202/0818/0922", "미디어마트 프로모션 가격 정합성", "G/W 프리미엄 초고가 라인업 집중, PnL 흑자 극대화", "Swiss 지점 / 가격팀"],
              ["체코(CK)", "0414/0818", "로컬 이커머스(Alza) 가격 덤핑", "캐시백 기반 마진 방어, 저수익 SKU 정리", "CK 법인"],
              ["폴란드(PL)", "0414/0818", "생산지 인접 불구 저가 쏠림", "Euro RTV 대상 55\"↑ OLED 믹스 확대, SA Gap 축소", "PL 법인"],
              ["헝가리(HS)", "0414/0818", "포린트화(HUF) 급락에 따른 마진 누수", "환율 연동 슬라이딩 판가제, 안전재고 최소화", "HS 법인 / 해외관리"],
              ["루마니아(RO)", "0414/0818", "eMAG 온라인 과점 마진 압박", "Altex 오프라인 진열 확대, 신모델 번들 공급", "RO 법인"],
              ["포르투갈(PT)", "0202/0818", "OLED API 급락 및 Worten 공세", "OLED 지표 반전, Worten 공동 펀딩 프로모션", "PT 법인 / GTM실"],
              ["오스트리아(AG)", "0414/0818", "독일 MMS와의 국경 간 가격 불일치", "독일 법인과 가격 동기화, AT 전용 물동 분리", "AG 법인"],
              ["그리스(MK)", "0414/0818", "Kotsovolos 의존도 및 관광 경기", "여름 B2B 호텔 프로젝트 연계, 연말 수량 사수", "MK 법인"],
              ["동유럽(LA)", "0414/0818", "발틱/동유럽 다국가 물류 비효율", "중앙 풀필먼트 허브 일원화, 한계이익 하위 모델 단종", "LA 법인 / SCM"]
            ],
            [12, 12, 30, 34, 12]
          ),

          p("", { spaceAfter: 200 }),
          p("— 보고서 끝 (End of Document) —", { align: AlignmentType.CENTER, italic: true, size: 18, color: COLOR_MUTED })
        ]
      }
    ]
  });

  const buffer = await Packer.toBuffer(doc);
  const targetDir = path.resolve('Task/20261007_2026전략회의_PD회의_추진과제정리');
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const outputPath = path.join(targetDir, '2026년_유럽TV_전략회의_및_PD회의_종합분석_보고서.docx');
  fs.writeFileSync(outputPath, buffer);
  console.log(`Successfully generated document at: ${outputPath}`);
}

buildDocx().catch(err => {
  console.error("Failed to build docx:", err);
  process.exit(1);
});
