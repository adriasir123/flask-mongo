# App Web MongoDB

En este repositorio se encuentra el código de mi aplicación Flask para MongoDB, y en este `README.md` se encuentra toda la documentación necesaria.

## Requerimientos

```shell
sudo apt update
sudo apt install python3-venv git
```

## Crear venv

```shell
mkdir venv
cd venv
python3 -m venv .
source bin/activate
```

### Descargar la app del repo

```shell
git clone git@github.com:adriasir123/flask-mongo.git
pip install -r requirements.txt
```




```shell
sudo apt install python3-pip
flask run --host=0.0.0.0
```


FALTA LA PRUEBA conecte con el servidor MongoDB desde un cliente remoto (clientemongo instalar interfaz gráfica)

FALTAN PRUEBAS DE FUNCIONAMIENTO


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

captura de pantalla aquí

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

captura de funcionamiento aquí

### Nginx + Gunicorn

```shell
sudo apt install nginx
```

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

Pruebo que funciona:

captura de pantalla funcionando

## Bibliografía

https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application
https://www.youtube.com/watch?v=w1STSSumoVk
