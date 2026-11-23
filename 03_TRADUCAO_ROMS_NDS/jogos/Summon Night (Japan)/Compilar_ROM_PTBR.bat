@echo off
chcp 65001 >nul
title Compilador de ROM PT-BR - Summon Night (NDS)
cd /d "%~dp0"
echo Compilando a ROM traduzida de Summon Night (NDS)...
python -X utf8 tools\build_ptbr_rom.py
pause
