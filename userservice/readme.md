# START THE ENV
env\Scripts\activate
# LINUX 
source venv/bin/activate

# START SERVER
python manage.py runserver

# CREATE ANY FOLDER UNDER A SPECFIC SERVICE
python manage.py startapp api 

# CREATE MODEL FOR MIGRAION
python manage.py makemigrations
python manage.py makemigrations "App name = api"

# MIGRATE MODEL TO DB
python manage.py migrate


