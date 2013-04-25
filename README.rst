mkvirtualenv project
pip install django
django-admin.py startproject --template=https://github.com/twoscoops/django-twoscoops-project/zipball/master --extension=py,rst,html project
cd project && add2virtualenv `pwd`
pip install -r requirements/local.txt

