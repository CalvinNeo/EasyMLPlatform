:start
@python manage.py runserver 8091
@echo server start at port 8091
@echo restart serever(Y/N)?
@set /p op=
@if op == "Y" goto start
@if op == "y" goto start
