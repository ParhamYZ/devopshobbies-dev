# DevOpsHobbies
## Project Description
This is a practical project to learn how to build a django project and deploy it in the production environment. A full description of this assignment is provided in 'python-assignment.md' file. Dear Amirbahador has explained this project step by step in Persian and you can see his videos in the link below:
https://www.youtube.com/playlist?list=PLYrn63eEqAzY5uG5ks_OquWcojzHvhp9Z


## Project Setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd DevOpsHobbies
```

2- SetUp venv
```
virtualenv -p python3.10 venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements/local.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

7- run the project
```
python manage.py runserver
```
