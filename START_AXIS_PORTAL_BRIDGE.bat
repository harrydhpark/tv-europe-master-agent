@echo off
chcp 65001 >nul
title AXIS Sales Portal - Antigravity Master Agent Bridge (Port 5050)
cd /d "%~dp0"

echo ============================================================================
echo   [AXIS Master Agent] Sales Portal ^<--^> Antigravity Sidecar Bridge Launcher
echo ============================================================================
echo.

set "NODE_BIN=node"
if exist "C:\Users\harry.park\node-dist\node-v20.11.1-win-x64\node.exe" (
    set "NODE_BIN=C:\Users\harry.park\node-dist\node-v20.11.1-win-x64\node.exe"
)

echo [1/2] Syncing Sales Portal Unified AI Command Bar ^& Slide-over Drawer...
"%NODE_BIN%" -e "require('./scripts/antigravity_sidecar_engine').syncPortalBridgeFiles(); console.log('  - Synced successfully.');"

echo [2/2] Starting AXIS Master Agent API Server (Port 5050) ^& Autonomous Bridge Worker...
echo       - Sales Portal URL : http://localhost:5050/portal/index.html
echo       - Master Agent URL : http://localhost:5050/
echo.
"%NODE_BIN%" start_sidecar_bridge.js
pause
