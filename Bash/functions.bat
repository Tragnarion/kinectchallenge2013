@echo off

rem ------------------------------------------------------------------
rem Function Definitions
rem ------------------------------------------------------------------

REM Skip function definitions
goto EndFunctions

rem ------------------------------------------------------------------
REM This function will process all words from a given text file using
REM a provided callback
REM %1 Relative path to the source file
REM %2 Call back used to process every word
rem ------------------------------------------------------------------
:processWord
REM Word list from file
set WordList=
FOR /F "eol= tokens=* delims= usebackq" %%i IN (%1) DO (
	set WordList=%%i
)
FOR %%i IN (%WordList%) DO (
	%2 %%i
)
GOTO:EOF

rem ------------------------------------------------------------------
REM Funtion that looks if a string contains another
REM USE: call:containsString Test e
REM RETURN: %$answer% is Y then e in in Test, N otherwise
REM %1 string
REM %2 sub-set
rem ------------------------------------------------------------------
:containsString
setlocal
set $answer=N
if {%1} EQU {} goto endContainsString
if {%1} EQU {""} goto endContainsString
if {%2} EQU {} goto endContainsString
if {%2} EQU {""} goto endContainsString
set $string=####%1####
set $string=%$string:####"=%
set $string=%$string:"####=%
if "%$string%" EQU "" goto endContainsString
set $string=%$string:####=%
set $substring=####%2####
set $substring=%$substring:####"=%
set $substring=%$substring:"####=%
if "%$substring%" EQU "" goto endContainsString
set $substring=%$substring:####=%
for /f "Tokens=*" %%k in ('@echo %%$string:%$substring%^=%%') do @set $work$=%%k
if NOT "%$string%" EQU "%$work$%" set $answer=Y
:endContainsString
endlocal&set $answer=%$answer%
GOTO:EOF

:EndFunctions