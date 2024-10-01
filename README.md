# Retwitter

Retwitter es una sencilla herramienta que te permite hacer *retweets* de manera automática de otra cuenta. Es una forma sencilla de seguir una cuenta concreta sin tener que hacerlo manualmente.

## Instalación

Esta herramienta utiliza Docker para funcionar, con lo que es realmente sencillo ponerla en funcionamiento utilizando `docker-compose`. Para ello, simplemente utiliza el `docker-compose.yml` que se incluye en el repositorio, y que indico a continuación,

```yaml
services:
  image: atareao/retwitter:v0.1.0
  container_name: retwitter
  restart: unless-stopped
  init: true
  environment:
    - TZ=Europe/Madrid
    - CONFIG_FILE=/app/config.json
  volumes:
    - ./config.json:/app/config.json
```

Indicar que el fichero `config.json` es el que contiene la configuración de la cuenta que se va a seguir. Un ejemplo de este fichero es el siguiente,

```json
{
    "last_id": 1111111111111111111,
    "mail": "tu@correo.es",
    "openobserve_base_url": "",
    "openobserve_index": "",
    "openobserve_token": "",
    "password": "tu-password",
    "sleep_time": 600,
    "user_id": "user_id",
    "username": "username"
}
```

Este archivo tiene los siguientes campos,

* `last_id` es el último *tweet* que se ha retuiteado. Se utiliza para no retuitear los mismos *tweets* una y otra vez.
* `mail` es el correo electrónico de tu cuenta de Twitter.
* `password` es la contraseña de tu cuenta de Twitter.
* `username` es el nombre de usuario de tu cuenta de Twitter.
* `user_id` es el identificador de la cuenta de Twitter **a seguir**.
* `sleep_time` es el tiempo que se espera entre *retweets*.
* `openobserve_base_url` es la URL base de OpenObserve.
* `openobserve_index` es el índice de OpenObserve.
* `openobserve_token` es el token de OpenObserve.

En el caso de que `openobserve_base_url`, `openobserve_index` y `openobserve_token` estén vacíos, se ignorarán y no se utilizarán.

Es **importante** tener en cuenta que el archivo de configuración tiene que tener permisos de lectura y escritura para el usuario que ejecuta el contenedor. Por defecto, el contenedor se ejecuta con el usuario `10001`, con lo que el archivo de configuración tiene que tener permisos de lectura y escritura para este usuario.

Una vez configurado el archivo `config.json`, simplemente tienes que ejecutar el siguiente comando,

```bash
docker-compose up -d
```
