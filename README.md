![Verifydocs](https://dl.dropboxusercontent.com/s/9ssp4wx8o079bsh/readme_banner.png?dl=0)
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
### Instalación

 - Intalar y configurar [postgresql](https://www.postgresql.org/), preferiblemente la versión mas reciente
 - Instalar [supervisor](http://supervisord.org/installing.html)
 - Instalar [node](https://nodejs.org/es/) y [bower](https://bower.io/)
 - Instalar [gunicorn](https://docs.gunicorn.org/en/stable/install.html#ubuntu)
 - Instalar [nginx](https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview)

Creación del entorno virtual en el sistema operativo con [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) usando python 3.6 o superior

```shell script
 $ mkvirtualenv verifydocs -p /usr/bin/python3.x
 $ workon verifydocs
```
Clonar el repositorio privado desde GitHub
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

Creación y ejecución de las migraciones, y la agrupación del los archivos estaticos de la aplicación
```shell script
$ python manage.py makemigrations
$ python manage.py migrate
$ mkdir static & mkdir temp & mkdir media & mkdir media/tmp/
$ python manage.py collectstatic
```

Ejecutar bower para descargar las librerias de javascript necesarias
```shell script
$ cd static/app/
$ bower install --save blockchain/bc-qr-reader
$ cd ../../
```
Crear el archivo verifydocs.conf en supervisorctl
```shell script
$ sudo mkdir /var/log/verifydocs
$ sudo nano /etc/supervisor/conf.d/verifydocs.conf
```
Copiar el siguiente texto en el archivo de configuración
```text
[program:verifydocs_gunicorn]
directory=/home/<usuario>/verifydocs
command=/home/<usuario>/.virtualenvs/verifydocs/bin/gunicorn --workers 2 --bind unix:/home/<usuario>/verifydocs/verifydocs.sock verifydocs.wsgi:appl$
autostart=true
autorestart=true
stderr_logfile=/var/log/verifydocs/gunicorn.out.log
stdout_logfile=/var/log/verifydocs/gunicorn.err.log
user=<usuario>
group=www-data
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8

[group:guni]
programs:verifydocs_gunicorn
```
Activar la configuracion de supervisorctl y revisar el estado de ejecución de la tarea
```shell script
$ sudo supervisorctl reread
$ sudo supervisorctl update
$ sudo supervisorctl status
```
Se debe tener en la carpeta /home/usuario/ssl/ los archivos del cerificado de seguridad SSL

Crear archivo de configuración del virtualhost en Nginx
```shell script
$ sudo nano /etc/nginx/sites-available/verifydocs
```
Copiar el siguiente texto en el archivo de configuración
```text
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
              '$status $body_bytes_sent "$http_referer" '
              '"$http_user_agent" "$http_x_forwarded_for"';
access_log  /var/log/nginx/access.log  main;

server {
    listen      443 ssl;
    listen [::]:443 default_server ipv6only=on;

    server_name verifydocs.ufps.edu.co;
    include /etc/nginx/default.d/*.conf;

    ssl on;
    ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;
    ssl_certificate /home/<usuario>/ssl/ufps.edu.co.crt;
    ssl_certificate_key /home/<usuario>/ssl/ufps.edu.co.key;
    ssl_session_cache shared:SSL:10m; 
    ssl_session_timeout 10m;

    location / {
        include proxy_params;
        proxy_pass https://unix:/home/<usuario>/verifydocs/verifydocs.sock;
    }

    location /static/ {
        root /home/<usuario>/verifydocs;
    }
    location /media/ {
        root /home/<usuario>/verifydocs;
    }

    error_page 404 /404.html;
        location = /40x.html {
    }

    error_page 500 502 503 504 /50x.html;
        location = /50x.html {
    }
}
```
Crear el enlace en la carpeta sites-enabled/
```shell script
$ sudo ln -s /etc/nginx/sites-available/verifydocs /etc/nginx/sites-enabled
```
Ejecutar pruebas de configuración en nginx
```shell script
$ nginx -t
```
Si todo parece estar correcto reicniar nginx
```shell script
$ sudo systemctl restart nginx
```

***
### Demo

Para ver el demo de la aplicación puede dirigirse a: [VerifyDocs](https://albertove.pythonanywhere.com/)

***
### Autores
Proyecto desarrollado por:
 - Edwin Velasco [GitHub](https://github.com/edwinVelasco) [LinkedIn](https://www.linkedin.com/in/edwin-alberto-velasco-2396891a7)
 - Denis González [GitHub](https://github.com/dexer13) [LinkedIn](https://www.linkedin.com/in/edwin-alberto-velasco-2396891a7)

***
### Institución Académica   
Proyecto desarrollado para el curso de profundización en desarrollo de software del [Programa de Ingeniería de Sistemas] de la [Universidad Francisco de Paula Santander]


   [Programa de Ingeniería de Sistemas]:<https://ingsistemas.cloud.ufps.edu.co/>
   [Universidad Francisco de Paula Santander]:<https://ww2.ufps.edu.co/>

