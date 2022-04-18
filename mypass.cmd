@ECHO OFF
Rem %~dp0main.py %*
if N%PYTHON_PATH%==N (py %~dp0main.py %*) else (%PYTHON_PATH% %~dp0main.py %*)