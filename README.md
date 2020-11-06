![Verifydocs](https://ucdb94fe13d9592d231ce14f1cf6.dl.dropboxusercontent.com/cd/0/get/BCr0wvsDoAwzbvKZpSdS7ZDEzpEiAro-HwX-_AefL95sPNti6xG_de_R2_K8JUXm3nQYdIq6s8soN3hspiG6IlphYvkm5rl_f5JQ--F91LI4ufGEZLQlVkvbnjocjFjnZ-o/file?_download_id=8092854901454845999159113084193445394528382896175854567170748172&_notify_domain=www.dropbox.com&dl=1)
# VerifyDocs 
### Nombre del proyecto:
#### Aplicativo web para verificar los documentos expedidos por las diferentes dependencias de la UFPS
***
### Índice
1. [Características](#caracter-sticas-)
2. [Contenido del proyecto](#contenido-del-proyecto)
3. [Tecnologías](#tecnologías)
4. [IDE](#ide)
5. [Instalación](#instalación)
6. [Demo](#demo)
7. [Autores](#autores)
8. [Institución Académica](#institución-académica)
***

#### Características:

  - Lectura de codigo qr mediante webcam usando el desarrollo de [bc-qr-reader](https://github.com/blockchain/bc-qr-reader)
  - Inicio de sesión social con Google
***
 
 #### Contenido del proyecto
  - [repositorio Github](https://gitlab.com/programacion-web---i-sem-2019/lectura-json-ii-2020-pizzeria/-/blob/master/index.html): Archivo principal de invocación a la lectura de JSON
  - [js/proceso.js](https://gitlab.com/programacion-web---i-sem-2019/lectura-json-ii-2020-pizzeria/-/blob/master/js/proceso.js): Archivo JS con el proceso de lectura del JSON y sus funciones adicionales para la impresión de resultados

***
#### Tecnologías

  - HTML5
  - JavaScript

Usted puede ver el siguiente marco conceptual sobre la API fetch:

  - [Vídeo explicativo lectura con fetch()](https://www.youtube.com/watch?v=DP7Hkr2ss_I)
  - [Gúia de Mozzilla JSON](https://developer.mozilla.org/es/docs/Learn/JavaScript/Objects/JSON)
  
  ***
#### IDE
  - El proyecto se desarrolla con [PyCharm](https://www.jetbrains.com/es-es/pycharm/) con [licencia de estudiante](https://www.jetbrains.com/es-es/community/education/#students)

***
#### Instalación

 - Intalar y configurar [postgresql](https://www.postgresql.org/), preferiblemente la versión mas reciente
 - Instalar [supervisor](http://supervisord.org/installing.html)
 - Instalar [node](https://nodejs.org/es/) y [bower](https://bower.io/)

Creación del entorno virtual en el sistema operativo con [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) usando python 3.6 o superior

```shell script
 $ mkvirtualenv verifydocs -p /usr/bin/python3.x
 $ workon verifydocs
```
Clonación del repositorio privado desde GitHub
```shell script
 $ git clone https://github.com/edwinVelasco/verifydocs.git verifydocs
 $ cd verifydocs
```

Instalar las librerias necesarias para la ejecución 
```shell script
 $ pip install -Ur requirements.txt
```

Ajustar la variable de entorno necesaria
```shell script
sudo nano /home/<usuario>/.virtualenvs/verifydocs/bin/postactivate
```
Registrar la siguiente linea al final del archivo
```shell script
export DJANGO_SETTINGS_MODULE=verifydocs.settings
```

Copiar y configurar el archivo de parametros requeridos para la ejecución.
```shell script
$ mv verifydocs/parameters-dist.py verifydocs/parameters.py
$ nano verifydocs/parameters.py
```
Se presentan las siguientes variables.
```python
PG_ENGINE = ''
# Nombre de la base de datos
PG_DBNAME = ''
# Usuario con acceso a la base de datos
PG_DBUSER = ''
# Contraseña del usuario con acceso a la base de datos
PG_DBPASSWORD = ''
PG_DBHOST = ''
PG_DBPORT = ''

DJ_SECRET_KEY = ''

# True en cado de estar en ambiente de pruebas
DJ_DEBUG = False

# Dominio en donde se esta alojando el aplicativo ejemplo: ['verifydocs.ufps.edu.co'] o ['*'] para ejecuciones de prueba
DJ_ALLOWED_HOSTS = ['*']

# Lenguaje que se maneja en el aplicativo
DJ_LANGUAGE_CODE = 'es-co'

# Zona horaria
DJ_TIME_ZONE = 'America/Bogota'
DJ_USE_I18N = False
DJ_USE_L10N = True
DJ_USE_TZ = False

# Id del sitio configurado con Google
DJ_SITE_ID = 1

# Ruta absoluta de la raiz del proyecto ejemplo: '/home/<user>/verifydocs'
DJ_URL_PROJECT = ''

# URL del proyecto instalado, se usa para utilizarlo en la creación del texto que acompaña el código QR
WEB_CLIENT_URL = 'https://verifydocs.ufps.edu.co/'
```
#### Configuración de acceso a la base de datos
Sistema de base de datos
```text
PG_ENGINE:  <django.db.backends.postgresql_psycopg2> Postgresql o <django.db.backends.mysql> Mysql
```
Host en donde se encuentra ubicada la base de datos
```text
PG_DBHOST: 127.0.0.1, localhost, 192.689.3.119, https://dbpostgresq.edu.co
```
Puerto de acceso a la base de datos
```text
PG_DBPORT: El puerto por defecto para PostgreSQL es 5432 y y para MySQL es 6379
```

#### Configuración personal de las variables de ejecición
Llave unica por instancia instala
```python
DJ_SECRET_KEY = ''
```
Ejecutar el siguiente comando para crear la llave unica, retorna una cadena
```shell script
$ openssl rand -base64 32
HuUk7oOLlxgdA0rw2J5qF+Et9kYW1+MwBTtMeFUHN8M=
$ # copiar el texto generado a la variable DJ_SECRET_KEY
```

Creación y ejecución de las migraciones y la agrupación del los archivos estaticos de la aplicación
```shell script
$ python manage.py makemigrations
$ python manage.py migrate
$ mkdir static
$ python manage.py collectstatic
```

Ejecutar bower para descargar las librerias de javascript necesarias
```shell script
$ cd static/app/
$ bower install --save blockchain/bc-qr-reader
$ cd ../../
```


***
### Demo

Para ver el demo de la aplicación puede dirigirse a: [VerifyDocs](https://albertove.pythonanywhere.com/)

***
### Autores
Proyecto desarrollado por:
 - Edwin Velasco [![git](https://ucc369a35be597189b31d8e4f331.dl.dropboxusercontent.com/cd/0/get/BCpj5Lg4x5ifMjS481b1HB0YEggeLg8EKR-ar7xM9LFKtobCUSB_21qDwSlzlcM3CXXvRaZJoiGW0z90OKkBHjfSzXs01eRHZ2nySvCZQ3Ly5B1E2HhgFavCMU-0Eoo-R54/file?_download_id=9568804072349331042274211886759505759415927615930644992703173029747&_notify_domain=www.dropbox.com&dl=1)](https://github.com/edwinVelasco) [LinkedIn](www.linkedin.com/in/edwin-alberto-velasco-2396891a7)
 - Denis González [![git](https://ucc369a35be597189b31d8e4f331.dl.dropboxusercontent.com/cd/0/get/BCpj5Lg4x5ifMjS481b1HB0YEggeLg8EKR-ar7xM9LFKtobCUSB_21qDwSlzlcM3CXXvRaZJoiGW0z90OKkBHjfSzXs01eRHZ2nySvCZQ3Ly5B1E2HhgFavCMU-0Eoo-R54/file?_download_id=9568804072349331042274211886759505759415927615930644992703173029747&_notify_domain=www.dropbox.com&dl=1)](https://github.com/dexer13) [LinkedIn](www.linkedin.com/in/edwin-alberto-velasco-2396891a7)


***
### Institución Académica   
Proyecto desarrollado para el curso de profundización en desarrollo de software del [Programa de Ingeniería de Sistemas] de la [Universidad Francisco de Paula Santander]


   [Programa de Ingeniería de Sistemas]:<https://ingsistemas.cloud.ufps.edu.co/>
   [Universidad Francisco de Paula Santander]:<https://ww2.ufps.edu.co/>
   


# verifydocs
The application includes the development of a module in charge of registering dependencies and users, uploading and downloading of authenticated documents through the web, public viewing of documents through a QR code and loading and unloading of documents.
