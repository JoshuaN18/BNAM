
```
virtualenv venv --python=python3
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

```
pip install django
django-admin startproject <name>
python manage.py startapp <name>
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py runserver
```

```
pip install djangorestframework
```

https://medium.com/@jtpaasch/the-right-way-to-use-virtual-environments-1bc255a0cba7