@echo off
call C:\ProgramData\Anaconda3\condabin\activate.bat C:\Users\micha\THU\H5PTranslator\env
python.exe ..\h5p_translate_process\translate_process.py %1 %2 %3
