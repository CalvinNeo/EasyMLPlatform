:start
@python manage.py runserver 8090
@echo server start at port 8090
@echo restart serever(Y/N)?
@set /p op=
@if %op% == "y" goto start
