@echo off

set SRCPATH1=D:\ZhiHuLive\知乎live\download
set SRCPATH2=D:\ZhiHuLive\知乎live\download2
set DESPATH1=D:\ZhiHuLive\知乎live\zip
set DESPATH2=D:\ZhiHuLive\知乎live\zip2

set count = 0

:start

	set /a count += 1

	for /f "delims=" %%i   in ('dir  /b  %SRCPATH1%')  do (


		if EXIST %SRCPATH1%\%%i (
			if EXIST %SRCPATH1%\%%i\done_tag (
				if not EXIST "%DESPATH1%\%%i.zip" (
					haozipc a -tzip "%DESPATH1%\%%i.zip" "%SRCPATH1%\%%i"
				)
				rd /s /Q "%SRCPATH1%\%%i"
			)
		)
	)
	
	
	for /f "delims=" %%i   in ('dir  /b  %SRCPATH2%')  do (


		if EXIST %SRCPATH2%\%%i (
			if EXIST %SRCPATH2%\%%i\done_tag (
				if not EXIST "%DESPATH2%\%%i.zip" (
					haozipc a -tzip "%DESPATH2%\%%i.zip" "%SRCPATH2%\%%i"
				)
				rd /s /Q "%SRCPATH2%\%%i"
			)
		)
	)


	
	
	echo 完成%count%次扫描 60秒后开始下一次扫描
	ping -n 60 127.0.0.1>nul

goto start
