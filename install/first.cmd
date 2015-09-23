@echo "press any key to init www"
@pause
python ../www/manage.py makemigrations
python ../www/manage.py migrate
python ../www/manage.py flush
python ../www/manage.py createsuperuser 