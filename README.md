# typeFiction
An online platform for amateur writers to publish their stories.

## To start the ap
1. pip3 install django-crispy-forms
1. pip3 install markdown2
1. Setting.py + CRISPY_TEMPLATE_PACK = 'bootstrap4'
1. Run `python3 manage.py makemigrations typeFiction` to make migrations for the typeFiction app.
1. Run `python3 manage.py migrate` to apply migrations to your database.
1. Run `python3 manage.py runserver` to start server

## 🔊 Plan and processes
This project started out as an extension of my [Network project](https://github.com/abeatrix/network). The goal of this project is to utilize the skills I’ve acquired from the last four projects to build something new, which includes making API calls, creating API routes, pagination, etc. However, instead of using SQLite, I have decided to use PostgreSQL as the database. 

I wanted to use React.js for the frontend initially but realized React.js would be better used when building a single-page application, that makes me believe staying with Django templates and focus on creating reusable components with jQuery would be a better choice here. I have also done my research on designing mobile-friendly web apps and other django libraries.


## 🖨 Dependents
markdown 2
Crispy Form
Popper
BootStrap
Python
Django
JavaScript
HTML5&CSS