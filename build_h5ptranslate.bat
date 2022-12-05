call C:\ProgramData\Anaconda3\condabin\activate.bat C:\Users\micha\THU\H5PTranslator\env
cd C:\Users\micha\THU\H5PTranslator
git tag -l --contains HEAD >version.txt
git rev-parse --short HEAD >> version.txt
REM pyinstaller main_gui.py
pause