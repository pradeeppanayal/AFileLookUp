start /B python FileWatcher.py
start /B waitress-serve --host 127.0.0.1 Server:app
start /B http://localhost:8080/web/index
pause