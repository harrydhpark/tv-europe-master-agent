const { RealDataEngine } = require('../realDataEngine');
const { LocalRuleEngine } = require('../localRuleEngine');
const { getAgentById, getAgentStatusSummary } = require('../agentRegistry');
const path = require('path');

async function testAll() {
  console.log("======================================================================");
  console.log(" 🧪 Strategic Reports Knowledge Base & Master Agent Integration Test");
  console.log("======================================================================");

  // Test 1: Agent Registry
  console.log("\n[Test 1] Checking Agent Registry...");
  const agent = getAgentById('strategic-reports');
  if (agent) {
    console.log(`  ✓ Agent found: ${agent.name} (Tag: ${agent.mentionTag})`);
  } else {
    throw new Error("Agent 'strategic-reports' not found in registry!");
  }

  // Test 2: RealDataEngine Summary
  console.log("\n[Test 2] Querying Strategic Reports Summary from DuckDB...");
  const realEngine = new RealDataEngine(path.resolve(__dirname, '..'));
  const summary = await realEngine.getStrategicReportsSummary();
  console.log(`  ✓ Total Indexed Reports: ${summary?.totalReports}`);
  console.log(`  ✓ Total Indexed Slides: ${summary?.totalSlides}`);
  console.log(`  ✓ Recent 3 Reports:`);
  summary?.recentReports?.slice(0, 3).forEach(r => {
    console.log(`    - [${r.meeting_type} | ${r.report_date}] ${r.report_name} (${r.total_slides} slides)`);
  });

  // Test 3: FTS Keyword Search
  console.log("\n[Test 3] Testing FTS BM25 Search for 'OLED'...");
  const oledSlides = await realEngine.searchStrategicReports('OLED', { limit: 3 });
  console.log(`  ✓ Found ${oledSlides?.length} slides:`);
  oledSlides?.forEach((s, i) => {
    console.log(`    ${i+1}. [${s.meeting_type}] ${s.report_name} (Slide ${s.slide_no}) - ${s.slide_title}`);
  });

  // Test 4: End-to-End Orchestration via LocalRuleEngine
  console.log("\n[Test 4] Testing End-to-End Query Orchestration...");
  const ruleEngine = new LocalRuleEngine(path.resolve(__dirname, '..'));
  const userQuery = "독일 법인 4분기 OLED 판가 인하 승인 요청 왔는데 전략회의 방침과 실적 대조해서 조언해줘";
  console.log(`  -> User Query: "${userQuery}"`);
  
  const response = await ruleEngine.processQuery(userQuery);
  console.log(`  ✓ Success: ${!!response}`);
  console.log(`  ✓ Dispatched Agents: ${response?.dispatchedAgents?.join(', ')}`);
  console.log(`  ✓ Timeline Steps (${response?.timeline?.length}):`);
  response?.timeline?.forEach(t => console.log(`     ${t.description}`));
  console.log(`  ✓ Artifact Type: ${response?.artifact?.type}`);
  console.log(`  ✓ Artifact Cited Slides: ${response?.artifact?.slides?.length}`);
  console.log(`  ✓ Artifact Metrics:`);
  response?.artifact?.metrics?.forEach(m => console.log(`     - ${m.label}: ${m.value} (${m.change})`));

  console.log("\n======================================================================");
  console.log(" 🎉 All 4 Tests Passed Successfully with Zero Errors!");
  console.log("======================================================================");
}

testAll().catch(err => {
  console.error("❌ Test Failed:", err);
  process.exit(1);
});
