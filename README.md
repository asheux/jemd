# jengachamaapp
A savings application that users can manage their saving, build with Django

# Installation and Setup
Clone the repository.

```
$ git clone https://github.com/asheuh/jengachamaapp
```

## Navigate to the project folder

```
$ cd jengachamaapp
```

## Create a virtual environment and activate

On linux

```
$ python -m venv venv
$ source venv/bin/activate

```

On Windows

```
$ py -3 -m venv venv
$ venv\Scripts\activate

```

## Install requirements( with pip)

```
$ pip install -r requirements.txt

```

## Running the application

After the configuration, you will run the app

```
$ mysql -u root -p
mysql> create database chamatu;
```

Run the application

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

```

## Url for endpoints

```
http://127.0.0.1:8000

```
