@echo off
SET COMMAND=cli.WorkMan.Daemon.hello
SET MIO_CONFIG=production
python\python mio\shell.pyc cli exe -cls=%COMMAND%
pause