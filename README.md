# README #

Pasos para levantamiento PezTech

### Configuración del entorno ###

* Instalar Python v3.6
* Intalar Pip (gestor de dependencias)
* Instalar WebDriver Chrome (https://sites.google.com/a/chromium.org/chromedriver/downloads)
* Instalar OBS

### Librerías pip necesarias ###

* pip install django
* pip install freeze
* pip install selenium

### Ejecución de la app ###

* 1) python manage.py migrate
* 2) python manage.py makemigrations
* 3) python manage.py migrate
* 4) python manage.py runserver