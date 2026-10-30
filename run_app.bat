@echo off
title CropCare AI - On-Device Assistant
cd /d "%~dp0"
echo ========================================================
echo Starting CropCare AI - Edge-Native Diagnostic Assistant
echo Team: pixel blend.r ^| Alliance University
echo ========================================================
python -m streamlit run app.py --server.port 8501 --server.headless false
pause
