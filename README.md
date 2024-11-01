# Welcome to Our Backend!

### Building the Project:

Ensure you have both the frontend and backend in the same folder as your development enviroment folder, and then build the docker container using the commands below

```

```
Once done, ensure you set up your database properly by running all of the commands in your terminal below:
```
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations auth
python manage.py migrate auth
python manage.py makemigrations emdcbackend
python manage.py migrate emdcbackend
```