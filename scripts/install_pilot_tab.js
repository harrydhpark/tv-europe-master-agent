const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const PORTAL_DIR = path.resolve(ROOT_DIR, '..', '00. TV Europe Sales Management Portal');

function removePilotFromGuide(guidePath) {
  if (!fs.existsSync(guidePath)) return false;
  let html = fs.readFileSync(guidePath, 'utf8');

  // Remove any injected 7. AXIS 작업 지시 프롬프트(Pilot) nav, section, and script blocks
  html = html.replace(/\s*<!-- AXIS_PILOT_NAV_START -->[\s\S]*?<!-- AXIS_PILOT_NAV_END -->/g, '');
  html = html.replace(/\s*<!-- AXIS_PILOT_SECTION_START -->[\s\S]*?<!-- AXIS_PILOT_SECTION_END -->/g, '');
  html = html.replace(/\s*<!-- AXIS_PILOT_SCRIPT_START -->[\s\S]*?<!-- AXIS_PILOT_SCRIPT_END -->/g, '');

  fs.writeFileSync(guidePath, html, 'utf8');
  return true;
}

const guideTargets = [
  path.join(PORTAL_DIR, 'docs', 'AXIS_System_Architecture_Guide.html'),
  path.join(PORTAL_DIR, 'public', 'docs', 'AXIS_System_Architecture_Guide.html'),
  path.join(ROOT_DIR, 'public', 'docs', 'AXIS_System_Architecture_Guide.html')
];

for (const gp of guideTargets) {
  if (removePilotFromGuide(gp)) {
    console.log('[RemovePilot] Removed 7. AXIS 작업 지시 프롬프트 menu from:', gp);
  }
}
