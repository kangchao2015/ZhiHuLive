@echo off

set ZIPFILE="C:\Program Files\2345Soft\HaoZip\HaoZipC.exe"

set SRCPATH1=D:\ZhiHuLive\֪��live\download
set SRCPATH2=D:\ZhiHuLive\֪��live\download2
set DESPATH1=G:\1_֪��\֪��live
set DESPATH2=G:\1_֪��\֪��˽�ҿ�

set count = 0

:start

	set /a count += 1

	for /f "delims=" %%i   in ('dir  /b  %SRCPATH1%')  do (


		if EXIST %SRCPATH1%\%%i (
			if EXIST %SRCPATH1%\%%i\done_tag (
				if not EXIST "%DESPATH1%\%%i.zip" (
					%ZIPFILE% a -tzip "%DESPATH1%\%%i.zip" "%SRCPATH1%\%%i"
				)
				rd /s /Q "%SRCPATH1%\%%i"
			)
		)
	)
	
	
	for /f "delims=" %%i   in ('dir  /b  %SRCPATH2%')  do (


		if EXIST %SRCPATH2%\%%i (
				if not EXIST "%DESPATH2%\%%i.zip" (
					%ZIPFILE% a -tzip "%DESPATH2%\%%i.zip" "%SRCPATH2%\%%i"
				)
				rd /s /Q "%SRCPATH2%\%%i"
		)
	)


	
	
	echo ���%count%��ɨ�� 60���ʼ��һ��ɨ��
	ping -n 6 127.0.0.1>nul

goto start
