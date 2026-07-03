@echo off
REM === Transforme CE poste en poste de FORMATION ===
REM Les donnees vivent dans le dossier frere  donnees\  (V1.53).
cd /d "%~dp0\.."
set "DON=..\donnees"
if not exist "%DON%\instance" mkdir "%DON%\instance"
if not exist "%DON%\data" mkdir "%DON%\data"
echo formation> "%DON%\instance\formation.flag"
copy /Y "formation\seed\EMSP_V1.xlsx" "%DON%\data\EMSP_V1.xlsx" >nul
copy /Y "formation\seed\EMSP_Notes.xlsx" "%DON%\data\EMSP_Notes.xlsx" >nul
if exist "%DON%\instance\comptes.json" del /Q "%DON%\instance\comptes.json"
if exist "%DON%\instance\journal.csv" del /Q "%DON%\instance\journal.csv"
echo.
echo Installation FORMATION terminee (bandeau rouge, donnees fictives).
echo Lancez l'application normalement. A NE PAS faire sur le poste de production.
pause
