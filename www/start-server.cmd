:start
@python manage.py runserver 8090
@echo restart serever(Y/N)?
@set /p op=
@if op == "Y" goto start
