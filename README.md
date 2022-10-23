# App Web MongoDB

En este repositorio se encuentra el código de mi aplicación Flask para MongoDB, y en este `README.md` se encuentra toda la documentación necesaria.

## Requerimientos

```shell
sudo apt update
sudo apt install python3-venv git nginx
```

## Crear venv

```shell
mkdir venv
cd venv
python3 -m venv .
source bin/activate
```

## Descargar la app del repo

```shell
git clone git@github.com:adriasir123/flask-mongo.git
pip install -r requirements.txt
```

## Probar con el servidor de desarrollo

```shell
flask run --host=0.0.0.0
```

![testdevserver](https://i.imgur.com/xbcOTBK.png)

## Despliegue con Nginx

### Fichero wsgi

`/home/vagrant/flask-mongo/wsgi.py`

```shell
from app import app as application
```

### Instalar Gunicorn

```shell
pip install gunicorn
```

### Probar funcionamiento

```shell
gunicorn -w 2 -b :8080 wsgi
```

![gunicorntest](https://i.imgur.com/6xQkVOo.png)

### Crear unidad systemd

`/etc/systemd/system/gunicorn-flask-mongo.service`:

```shell
Description=gunicorn-flask-mongo
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
User=www-data
Group=www-data
Restart=always

ExecStart=/home/vagrant/venv/bin/gunicorn -w 2 -b :8080 wsgi
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

WorkingDirectory=/home/vagrant/flask-mongo
Environment=PYTHONPATH='/home/vagrant/flask-mongo:/home/vagrant/venv/lib/python3.9/site-packages'

PrivateTmp=true
```

La activo e inicio:

```shell
sudo systemctl enable gunicorn-flask-mongo.service
sudo systemctl start gunicorn-flask-mongo.service
```

Compruebo que está funcionando:

```shell
(venv) vagrant@servidormongodb:~/flask-mongo$ sudo systemctl status gunicorn-flask-mongo.service
● gunicorn-flask-mongo.service
     Loaded: loaded (/etc/systemd/system/gunicorn-flask-mongo.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2022-10-23 22:29:47 UTC; 1min 17s ago
   Main PID: 2500 (gunicorn)
      Tasks: 9 (limit: 1131)
     Memory: 61.6M
        CPU: 1.229s
     CGroup: /system.slice/gunicorn-flask-mongo.service
             ├─2500 /home/vagrant/venv/bin/python3 /home/vagrant/venv/bin/gunicorn -w 2 -b :8080 wsgi
             ├─2501 /home/vagrant/venv/bin/python3 /home/vagrant/venv/bin/gunicorn -w 2 -b :8080 wsgi
             └─2502 /home/vagrant/venv/bin/python3 /home/vagrant/venv/bin/gunicorn -w 2 -b :8080 wsgi

Oct 23 22:29:47 servidormongodb systemd[1]: Started gunicorn-flask-mongo.service.
Oct 23 22:29:47 servidormongodb gunicorn[2500]: [2022-10-23 22:29:47 +0000] [2500] [INFO] Starting gunicorn 20.1.0
Oct 23 22:29:47 servidormongodb gunicorn[2500]: [2022-10-23 22:29:47 +0000] [2500] [INFO] Listening at: http://0.0.0.0:8080 (2500)
Oct 23 22:29:47 servidormongodb gunicorn[2500]: [2022-10-23 22:29:47 +0000] [2500] [INFO] Using worker: sync
Oct 23 22:29:47 servidormongodb gunicorn[2501]: [2022-10-23 22:29:47 +0000] [2501] [INFO] Booting worker with pid: 2501
Oct 23 22:29:47 servidormongodb gunicorn[2502]: [2022-10-23 22:29:47 +0000] [2502] [INFO] Booting worker with pid: 2502
Oct 23 22:31:05 servidormongodb systemd[1]: /etc/systemd/system/gunicorn-flask-mongo.service:1: Assignment outside of section. Ignoring.
Oct 23 22:31:05 servidormongodb systemd[1]: /etc/systemd/system/gunicorn-flask-mongo.service:2: Assignment outside of section. Ignoring.
```

### Nginx + Gunicorn

Creo `/etc/nginx/sites-available/flask-mongo.conf`:

```shell
server {

    listen 80;
    server_name www.flask-mongo-gunicorn.com;
    root /home/vagrant/flask-mongo;

    location / {
        proxy_pass http://localhost:8080;
        include proxy_params;
    }

}
```

Lo habilito:

```shell
sudo ln -s /etc/nginx/sites-available/flask-mongo.conf /etc/nginx/sites-enabled
```

Reinicio Nginx:

```shell
sudo systemctl restart nginx
```

Pruebo que funciona desde `clientemongodb`:

![clientemongoaccesoweb](https://i.imgur.com/PcLt5ZI.png)

## Pruebas de funcionalidades

Habiendo ya probado que la aplicación funciona desde `clientemongodb` accediendo a la URL final de Nginx, haré estas pruebas accediendo desde mi máquina simplemente para que las screenshots salgan con mejor calidad.

### Creación de usuario y acceso

![creousuario](https://i.imgur.com/Q1kJd9X.png)

![primeracceso](https://i.imgur.com/bfx5slT.png)

### Evita emails repetidos

No dejará avanzar en la creación de usuario si el email es repetido:

![emailrepetido](https://i.postimg.cc/fbNFRbjP/email-repetido.gif)

### Evita logins con contraeña incorrecta

![badpassword](https://i.postimg.cc/rFSynDmn/bad-password.gif)

### Redirects si se intenta saltar el login

![redirect](https://i.postimg.cc/gJH7fbCZ/redirect.gif)

### Info de usuario actual y listado completo

![usuarios](https://i.postimg.cc/05mG5CjV/usuarios.gif)

### Función de Sign Out

Cierra la sesión actual:

![signout](https://i.postimg.cc/VvcC03vD/signout.gif)

## Bibliografía

https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application
https://www.youtube.com/watch?v=w1STSSumoVk
