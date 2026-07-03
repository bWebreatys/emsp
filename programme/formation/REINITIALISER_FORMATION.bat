@echo off
REM === Remet le jeu de FORMATION a neuf : restaure les exemples et efface ===
REM === les donnees ET les utilisateurs crees pendant la formation.        ===
REM Donnees dans le dossier frere  donnees\  (V1.53).
cd /d "%~dp0\.."
set "DON=..\donnees"
if not exist "%DON%\instance\formation.flag" (
  echo.
  echo Ce poste n'est PAS une installation de formation ^(drapeau absent^).
  echo Reinitialisation ANNULEE pour proteger d'eventuelles donnees de production.
  echo.
  pause
  exit /b 1
)
echo Fermez d'abord l'application si elle est ouverte, puis appuyez sur une touche...
pause >nul
echo  - restauration du jeu d'exemples
copy /Y "formation\seed\EMSP_V1.xlsx" "%DON%\data\EMSP_V1.xlsx" >nul
copy /Y "formation\seed\EMSP_Notes.xlsx" "%DON%\data\EMSP_Notes.xlsx" >nul
echo  - effacement des utilisateurs et du journal crees en formation
if exist "%DON%\instance\comptes.json" del /Q "%DON%\instance\comptes.json"
if exist "%DON%\instance\journal.csv" del /Q "%DON%\instance\journal.csv"
echo.
echo Termine. Le jeu de formation est remis a neuf (le mode formation reste actif).
pause
