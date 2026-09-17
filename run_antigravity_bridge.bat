@echo off
chcp 65001 > nul
title TV Europe Master AI Agent - Antigravity Autonomous Bridge Launcher
echo =====================================================================
echo  🤖 LGE TV Europe Sales Master AI Agent: Antigravity Session Bridge
echo =====================================================================
echo.
echo [1/2] 백그라운드 Express API 서버 (포트 5050) 가동...
start "Master Agent API Server (:5050)" cmd /c "node server.js"

echo [2/2] 브라우저 대시보드 자동 실행 (http://localhost:5050)...
timeout /t 2 /nobreak > nul
start http://localhost:5050

echo.
echo =====================================================================
echo  🚀 안티그래비티 세션 브릿지 감시기 (watch_bridge.js) 상시 가동 중
echo  - 대시보드 질의 감지 시 안티그래비티 AI 세션으로 즉시 전달
echo  - 분석 엔진 하드코딩 없이 안티그래비티 AI가 자율 분석하여 대시보드로 반환
echo  - 종료하시려면 본 창을 닫으십시오.
echo =====================================================================
echo.

node watch_bridge.js
