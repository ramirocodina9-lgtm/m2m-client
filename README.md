# M2M Client (Python)

Cliente ligero para consumir tres endpoints HTTP de **M2M_Cluster_Master**, mediante `requests`.

> **Estado:** cliente funcional para un nodo local de demostración. Los datos devueltos por la implementación inicial del servidor (arbitraje, leads y score de riesgo) son **sintéticos** y no deben interpretarse como oportunidades, contactos verificados ni auditorías financieras reales. Este repositorio **no** incluye el servidor ni claves de acceso.

## Requisitos

- Python 3.9 o superior.
- Acceso autorizado a una instancia del nodo M2M.
- La URL base del nodo y una API key emitida por el operador.

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Uso

```python
import os
from m2m_client import M2MClient

client = M2MClient(
    node_url=os.getenv("M2M_NODE_URL", "http://127.0.0.1:8000"),
    api_key=os.environ["M2M_API_KEY"],
)

print(client.get_arbitrage_alpha())
print(client.post_risk_audit(entidad_id="ENTIDAD_DE_PRUEBA", sector="saas"))
print(client.get_qualified_leads())
```

Para la ejecución local, definí `M2M_API_KEY` en el entorno del proceso: **no la publiques ni la incorpores al código fuente**. La dirección `127.0.0.1` solo funciona desde el equipo donde corre el nodo.

## Endpoints

| Método | Ruta | Método de cliente |
| --- | --- | --- |
| GET | `/api/v1/highticket/arbitrage` | `get_arbitrage_alpha()` |
| POST | `/api/v1/highticket/risk-audit` | `post_risk_audit(entidad_id, sector)` |
| GET | `/api/v1/highticket/qualified-leads` | `get_qualified_leads()` |

El cliente manda `X-API-KEY` a través de HTTPS/HTTP según la URL proporcionada. Usá **HTTPS** al conectarte con nodos remotos. Los métodos levantan una excepción ante estados HTTP distintos de 200. Las llamadas no definen un timeout explícito: en redes no confiables, se recomienda configurarlo antes de poner este cliente en producción.

## Seguridad y transparencia

- No se suministran credenciales, tokens de pago, endpoints externos ni claves de demostración.
- El servidor inicial de prueba incluye una clave trial compartida **sin vencimiento efectivo**; nunca lo expongas como servicio público hasta reemplazarla por autenticación segura y expiración por cliente.
- `llms.txt` local no equivale por sí solo a descubrimiento automático en Internet.
- La publicación de esta librería **no** implica publicación ni monetización del nodo.
- Cualquier scoring real de contraparte necesita datos externos autorizados, metodología verificable y tratamiento adecuado de datos personales.

## Alcance

Este repositorio contiene únicamente el cliente Python. No ejecuta arbitraje, evaluación de riesgo, generación de leads ni movimientos de fondos por sí mismo.
