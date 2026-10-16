const {
  syncPortalBridgeFiles,
  listBrainConversations,
  scanTaskDeliverables
} = require('./antigravity_sidecar_engine');

console.log('[Sync] Running syncPortalBridgeFiles...');
const res = syncPortalBridgeFiles();
console.log('[Sync] Result:', JSON.stringify(res));

const convs = listBrainConversations(3);
console.log('[Sync] Recent Brain Conversations found:', convs.length);
if (convs.length > 0) {
  console.log('  Latest session:', convs[0].conversationId, '| steps:', convs[0].stepCount);
}

const tasks = scanTaskDeliverables(3);
console.log('[Sync] Recent Task Deliverables found:', tasks.length);
