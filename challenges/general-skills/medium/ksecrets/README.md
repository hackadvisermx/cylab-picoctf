# General Skills — KSECRETS

## Descripción
> **Prompt oficial del reto:** "We have a kubernetes cluster setup and flag is in the secrets. You think you can get it?" — se entrega la dirección del API server de Kubernetes (`green-hill.picoctf.net:59581`) y un enlace de descarga de un `kubeconfig`.

- **Categoría:** General Skills
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2026
- **Autor:** Darkraicg492

## Solución
El `kubeconfig.yaml` descargado trae credenciales de cliente (certificado + llave privada, autenticación TLS mutua) pero apunta a `server: https://127.0.0.1:6443` — una dirección interna del propio clúster, no accesible desde fuera. No hace falta instalar `kubectl`: basta con hablarle directamente a la API REST de Kubernetes (HTTP+TLS estándar) usando el certificado de cliente incluido, contra la dirección externa real que da el enunciado.

```bash
# extraer CA / cert / key del kubeconfig (base64 -> PEM)
python3 -c "
import yaml, base64
cfg = yaml.safe_load(open('kubeconfig.yaml'))
open('client.pem','wb').write(base64.b64decode(cfg['users'][0]['user']['client-certificate-data']))
open('client-key.pem','wb').write(base64.b64decode(cfg['users'][0]['user']['client-key-data']))
"

# listar namespaces (el CA del kubeconfig es para 127.0.0.1, no para el hostname externo -> -k para saltar verificación TLS)
curl -sk --cert client.pem --key client-key.pem \
  "https://green-hill.picoctf.net:59581/api/v1/namespaces"
# -> default, kube-node-lease, kube-public, kube-system, picoctf

# el namespace "picoctf" es el interesante -> listar sus secrets
curl -sk --cert client.pem --key client-key.pem \
  "https://green-hill.picoctf.net:59581/api/v1/namespaces/picoctf/secrets"
```

La respuesta trae el Secret `ctf-secret` con el campo `data.flag` en Base64 (los Secrets de Kubernetes **no están cifrados**, solo codificados en Base64):

```bash
echo "cGljb0NURntrczNjcjM3NV80MW43X3M0ZjNfZTBlZWVmYTZ9Cg==" | base64 -d
# picoCTF{ks3cr375_41n7_s4f3_e0eeefa6}
```

De hecho, la propia anotación `kubectl.kubernetes.io/last-applied-configuration` que Kubernetes guarda automáticamente al crear el recurso con `kubectl apply` ya expone el mismo Base64 en texto plano dentro del JSON del objeto — ni siquiera hace falta mirar el campo `data` mapeado.

## Notas adicionales
- El certificado de cliente entregado en el `kubeconfig` resultó tener privilegios suficientes para listar namespaces y leer Secrets en todos ellos (efectivamente admin) — no hubo que enumerar ni escalar RBAC.
- Lección del propio nombre del reto (y su flag: *"k8s secrets ain't safe"*): los Secrets de Kubernetes son **Base64, no cifrado** — cualquiera con permiso de lectura sobre el objeto (o acceso al `etcd` subyacente sin cifrado en reposo) puede decodificarlos trivialmente. En un clúster real, esto se mitiga con *encryption at rest*, RBAC estricto, y herramientas externas de gestión de secretos (Vault, SealedSecrets, etc.), nunca confiando en que "Base64 no es texto plano".
- No fue necesario instalar `kubectl`: la API de Kubernetes es simplemente HTTPS con autenticación por certificado de cliente (mTLS) sobre un esquema REST documentado — `curl --cert/--key` contra `/api/v1/namespaces/<ns>/<recurso>` funciona igual de bien para explorar un clúster cuando la CLI no está disponible.

## Referencias
- Reto: https://learn.cylabacademy.org/library/732
