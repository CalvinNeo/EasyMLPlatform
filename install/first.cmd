@echo "press any key to init www"
@pause
python ../manage.py makemigrations
python ../manage.py migrate
python ../manage.py flush
python ../manage.py createsuperuser 