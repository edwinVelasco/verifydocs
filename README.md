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

  - Lectura de código qr mediante webcam usando el desarrollo de [bc-qr-reader](https://github.com/blockchain/bc-qr-reader)
  - Inicio de sesión las cuentas de correo institucionales  con Google
  - Encriptación de documentos con sha_512, sha_256
  - Encriptación de token de verificación con md5
  - Servicios REST de consumo para la vinculación entre aplicaciones
  - Envío de notificación por correo electrónico 

***
 
 #### Contenido del proyecto
  - [repositorio Github](https://github.com/edwinVelasco/verifydocs): Raiz del proyecto
  - [Security/app.py](https://github.com/edwinVelasco/verifydocs/tree/master/security): Paquete de seguridad de encriptación de documentos
  - [tools](https://github.com/edwinVelasco/verifydocs/tree/master/tools): Paquete de herramientas requeridas en el proyecto, manejo de archivos PDF y envío de correo 
  - [templates](https://github.com/edwinVelasco/verifydocs/tree/master/templates): Carpeta en donde se encuantran ubicados los archivos .html ubicados por modulos 
  - [verifydocs/parameters-dist.py](https://github.com/edwinVelasco/verifydocs/blob/master/verifydocs/parameters-dist.py): Archivo de parametrización del proyecto 
  - [verifydocs/urls.py](https://github.com/edwinVelasco/verifydocs/blob/master/verifydocs/urls.py): Archivo de rutas del proyecto 
  - [app/migrations](https://github.com/edwinVelasco/verifydocs/tree/master/app/migrations): Modulo en donde se ubican las migraciones del proyecto
  - [app/forms.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/forms.py): Archivo en donde se ubican las clases de los formularios
  - [app/mixins.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/mixins.py): Archivo en donde se ubican las clases de los mixins
  - [app/models.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/models.py): Archivo en donde se ubican las clases de los modelos
  - [app/serializers.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/serializers.py): Archivo en donde se ubican las clases que serializan las clases de los modelos
  - [app/urls.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/urls.py): Archivo en donde se ubican las rutas de la aplicación app
  - [app/validators.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/validators.py): Archivo en donde se ubican las validaciones del dominio del correo
  - [app/views.py](https://github.com/edwinVelasco/verifydocs/blob/master/app/views.py): Archivo en donde se ubican las clases de las vistas
  - [app/static/app](https://github.com/edwinVelasco/verifydocs/tree/master/app/static/app): Carpeta donde se ubican los archivos estaticos de la aplicación app
  - [app/test](https://github.com/edwinVelasco/verifydocs/tree/master/app/test): Modulo de las pruebas unitarias de formularios, modelos, url's y vistas

***
#### Tecnologías

  - HTML5
  - JavaScript
  - Angular JS
  - Python
  - Django
  - Patron de diseño MTV (Models, Templates, Views)
  - Bootstrap
  - Sha 512
  - Sha 256
  - MD5
  
  ***
#### IDE
  - El proyecto se desarrolla con [PyCharm](https://www.jetbrains.com/es-es/pycharm/) con [licencia de estudiante](https://www.jetbrains.com/es-es/community/education/#students)
  - Entornos virtuales del interprete python3.8 [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

  ***
### Instalación

 - Instalar y configurar [postgresql](https://www.postgresql.org/), preferiblemente la versión mas reciente
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

Instalar las librerías necesarias para la ejecución 
```shell script
 $ pip install -Ur requirements.txt
```

Ajustar la variable de entorno necesaria
```shell script
sudo nano /home/<usuario>/.virtualenvs/verifydocs/bin/postactivate
```
Registrar la siguiente línea al final del archivo
```shell script
export DJANGO_SETTINGS_MODULE=verifydocs.settings
```

Copiar y configurar el archivo de parámetros requeridos para la ejecución.
```shell script
$ mv verifydocs/parameters-dist.py verifydocs/parameters.py
$ nano verifydocs/parameters.py
```
Se presentan las siguientes variables.
```python
# Sistema de base de datos
PG_ENGINE = ''

# Nombre de la base de datos
PG_DBNAME = ''

# Usuario con acceso a la base de datos
PG_DBUSER = ''

# Contraseña del usuario con acceso a la base de datos
PG_DBPASSWORD = ''

# host donde se ubica el servidor de base de datos, IP o dominio
PG_DBHOST = ''
# puerto donde se aloja la base de datos en caso de tenerlo
PG_DBPORT = ''

DJ_SECRET_KEY = ''

# True en caso de estar en ambiente de pruebas
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
DJ_SITE_ID = 2

# Ruta absoluta de la raiz del proyecto ejemplo: '/home/<user>/verifydocs'
DJ_URL_PROJECT = ''

# URL del proyecto instalado, se usa para utilizarlo en la creación del texto que acompaña el código QR
WEB_CLIENT_URL = 'https://verifydocs.ufps.edu.co/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
# Correo elecronico para el envío de notificación por smtp
EMAIL_HOST_USER = ''
# Contraseña de la cuenta de correo
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
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

#### Configuración personal de las variables de ejecución
Llave única por instancia instala
```python
DJ_SECRET_KEY = ''
```
Ejecutar el siguiente comando para crear la llave única, retorna una cadena
```shell script
$ openssl rand -base64 32
HuUk7oOLlxgdA0rw2J5qF+Et9kYW1+MwBTtMeFUHN8M=
$ # copiar el texto generado a la variable DJ_SECRET_KEY
```

Creación y ejecución de las migraciones, y la agrupación del los archivos estáticos de la aplicación
```shell script
$ python manage.py makemigrations
$ python manage.py migrate
$ mkdir static & mkdir temp & mkdir media & mkdir media/tmp/
$ python manage.py collectstatic
```

Ejecutar bower para descargar las librerías de javascript necesarias
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
command=/home/<usuario>/.virtualenvs/verifydocs/bin/gunicorn --workers 2 --bind unix:/home/<usuario>/verifydocs/verifydocs.sock  --certfile /home/<usuario>/ssl/file.crt --keyfile /home/<usuario>/ssl/file.key verifydocs.wsgi:application
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
Activar la configuración de supervisorctl y revisar el estado de ejecución de la tarea
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
Si todo parece estar correcto reiniciar nginx
```shell script
$ sudo systemctl restart nginx
```
Crear usuario superadministrador, ingresando a la ruta raíz del proyecto, 
ejecutar e ingresar usuario, contraseña y correo electrónico de superadministrador
 ```shell script
$ python manage.py createsuperuser
```
***
### Configurar servicios Google API
#### OAuth 2.0
Para obtener credenciales de Google API Console use la siguiente 
[guía](https://developers.google.com/identity/protocols/oauth2?authuser=1) tendrá un resultado como se muestra en la siguiente imagen:

![img](https://dl.dropboxusercontent.com/s/n4bgqgc1krtzwhc/WhatsApp%20Image%202020-11-22%20at%209.53.57%20AM.jpeg?dl=0)

Ingrese a través del explorador web al proyecto, con la ruta admin e iniciar sesión.
 
 ```text
Ejemplo: https://verifydocs.ufps.edu.co/admin/
```

Debe agregar un nuevo site, para esto presione el botón *add* que se encuentra delante del modelo *sites*

![img](https://dl.dropboxusercontent.com/s/zm19utfs6ewum29/Captura%20de%20pantalla%20de%202020-11-20%2013-54-37.png?dl=0)

En los campos de *Domain name* y *Display name* el valor de *https://verifydocs.ufps.edu.co* 
y presionar el botón guardar.

Regresar a la lista de modelos y presionar el botón *add* del modelo 
*Social application* e ingresar los siguientes valores:
* Provider: Google
* Name: GOOGLE API
* Client id: *Client ID* de las credenciales proporcionadas por google.
* Secret key: *Client secret* de  las credenciales proporcionadas por google.
* Sites: Seleccione el site creado en el paso anterior.

#### Servicio de aplicación para el almacenamiento de documentos
Para obtener el servicio de aplicación use la siguiente 
[guía](https://developers.google.com/identity/protocols/oauth2/service-account) 
y descargue el archivo json del servicio.

Cargue el archivo en la siguiente ruta del servidor en donde se 
encuentra alojado el aplicativo y con el mismo nombre

 ```shell script
$ verifydocs/tools/storage_key_file.json
```



***
### Demo

Para ver el demo de la aplicación puede dirigirse a: [VerifyDocs](https://albertove.pythonanywhere.com/)

***
### Autores
Proyecto desarrollado por:
 - Edwin Velasco [GitHub](https://github.com/edwinVelasco) [LinkedIn](https://www.linkedin.com/in/edwin-alberto-velasco-2396891a7)
 - Denis González [GitHub](https://github.com/dexer13)

***
### Institución Académica   
Proyecto desarrollado para el curso de profundización en desarrollo de software del [Programa de Ingeniería de Sistemas] de la [Universidad Francisco de Paula Santander]


   [Programa de Ingeniería de Sistemas]:<https://ingsistemas.cloud.ufps.edu.co/>
   [Universidad Francisco de Paula Santander]:<https://ww2.ufps.edu.co/>

