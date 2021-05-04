# typeFiction
An online platform for amateur writers to publish their stories.

## Project requirements
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.
- Your web application must be mobile-responsive.
- In a README file (whose extension can be .txt, .md, .adoc, or .pdf) in your project’s main directory, include a full write-up describing your project, what’s contained in each file you created, why you made certain design decisions, and any other additional information the staff should know about your project. This document should be sufficiently thorough for your teaching fellow to run your project without any need to contact you further with questions. Take your time, and do not save this step for last.
- If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to a requirements.txt file!


## To start the app
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