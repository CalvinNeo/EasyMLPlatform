@echo "press any key to migrate www"
@pause
python ../manage.py makemigrations
python ../manage.py migrate