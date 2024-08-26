Create project with PyCharm 2024.1 (Professional Edition) and Python 3.12.0.
![[Pasted image 20240703084852.png]]
So install it online, after install **PostegreSQL** package and application by the follow command.
```
pip install psycopg2
python manage.py startapp agribusiness
```
After that, install **Pillow** package for using *ImageField*.
```
pip install Pillow
```
After make migrations and migrate to automatic create table in database.
```
python manage.py makemigrations
python manage.py migrate
```
Create super user to do admin in this application and give it the access in this application. Do this access in admin.py.
```
python manage.py createsuperuser 
```
