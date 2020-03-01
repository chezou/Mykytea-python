set PLATFORM_PREFIX=
if "%PLATFORM%"=="x64" set PLATFORM_PREFIX=-x64

call :BuildPython C:\Python35%PLATFORM_PREFIX%
call :BuildPython C:\Python36%PLATFORM_PREFIX%
call :BuildPython C:\Python37%PLATFORM_PREFIX%
call :BuildPython C:\Python38%PLATFORM_PREFIX%
exit

:BuildPython
%1\python -m pip install -U wheel setuptools || goto :error
%1\python setup.py bdist_wheel || goto :error
rmdir /Q /S build
exit /b

:error
exit /b %errorlevel%