### projectile ###
We are setting up an application for the students to find projects of their interest and also to post projects to work along with other interested students. This application will provide an opportunity to novice student to work on something interesting.
We will set up a student platform where students from different domains could find projects of their interest and follow accordingly. 
It also gives them the feasibility for requesting a mentor who could guide them through.

### Getting it into your machine ###

* cd to a comfy location
* git clone git@github.com:devists/projectile.git
* cd projectile/
* virtualenv -p $(which python3) venv
* source venv/bin/activate
* pip install -r requirements.txt
* ./manage.py migrate
* ./manage.py runserver
* point your browser to [http://localhost:8000/](http://localhost:8000/)