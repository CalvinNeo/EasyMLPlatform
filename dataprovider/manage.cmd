:start
@echo input one command
@set /p op=
@python manage.py %op%
@goto start