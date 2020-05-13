# FinalProject

1. Install python
Install python 3.8 and python-pip

2. Setup virtual environment

Make a directory 'envs'
mkdir envs

Create virtual environment 
virtualenv ./envs/

Activate the virtual environment
source envs/bin/activate

3. Clone git repository
git clone "https://github.com/vcviet253/FinalProject.git"

4. Install requirements
cd FinalProject/
pip install -r requirements.txt

5. Run migrate
python manage.py migrate
python manage.py makemigrations

6. Create superuser
python manage.py createsuperuser

7. Run the project
python manage.py runserver
//By default, the server is located at http://127.0.0.1:8000/

