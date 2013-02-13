@echo off

rem We will define different platforms, they can come from an argument too
rem the platform will then be used to jump to the specific section
set Platform=PC
rem set Platform=MAC
rem set Platform=XBOX

rem Ese the platform string to jump to a given section
goto:section_%Platform%

:section_PC
echo This is the PC Section
goto:end

:section_MAC
echo This is the MAC Section
goto:end

:section_XBOX
echo This is the XBOX Section
goto:end

:end
pause