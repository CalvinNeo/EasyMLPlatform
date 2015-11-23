@echo "press any key to migrate www"
@pause
python ../www/manage.py makemigrations www
python ../www/manage.py migrate www

@pause