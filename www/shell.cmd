@echo "press any key to enter shell"
@pause
@python manage.py shell
from www.models import Dataset
Dataset.objects.create(name="test",filetype="STR",path="/e/",head="1,2,3")