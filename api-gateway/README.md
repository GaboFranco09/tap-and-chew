# API Gateway — tap&Chew

Punto de entrada único del sistema tap&Chew.
Construido con **Express.js** + **http-proxy-middleware**.

## Responsabilidad

Recibe todas las peticiones externas del kiosko y las enruta
al microservicio correspondiente. Centraliza la validación de
presencia de token, rate limiting y cabeceras de seguridad,
manteniendo cada microservicio desacoplado del mundo exterior.

## Stack

| Componente     | Tecnología                    |
|----------------|-------------------------------|
| Framework      | Express.js                    |
| Proxy          | http-proxy-middleware v2      |
| Seguridad      | helmet, cors                  |
| Rate limiting  | express-rate-limit            |
| Logging        | morgan                        |
| Puerto         | 8000                          |

## Rutas

| Prefijo         | Servicio destino   | Puerto |
|-----------------|--------------------|--------|
| /api/auth       | Auth Service       | 8001   |
| /api/menu       | Menu Service       | 8002   |
| /api/orders     | Order Service      | 8003   |
| /api/kitchen    | Kitchen Service    | 8004   |
| /api/payment    | Payment Service    | 8005   |

## Rutas públicas (sin token)

| Método | Ruta                          |
|--------|-------------------------------|
| POST   | /api/auth/login               |
| POST   | /api/auth/register            |
| POST   | /api/auth/forgot-password     |
| POST   | /api/auth/reset-password      |
| GET    | /health                       |

## Rate Limiting

| Scope         | Límite             |
|---------------|--------------------|
| General       | 100 req / 15 min   |
| /api/auth     | 10 req  / 15 min   |

## Instalación local
```bash
cd api-gateway
npm install
cp .env.example .env
npm run dev
```

## Variables de entorno requeridas
```env
PORT=8000
NODE_ENV=development

JWT_SECRET=

AUTH_SERVICE_URL=http://localhost:8001
MENU_SERVICE_URL=http://localhost:8002
ORDER_SERVICE_URL=http://localhost:8003
KITCHEN_SERVICE_URL=http://localhost:8004
PAYMENT_SERVICE_URL=http://localhost:8005
```

## Ejemplo de uso
```
# Health check
GET http://localhost:8000/health

# Login (público)
POST http://localhost:8000/api/auth/login
Content-Type: application/json
{ "email": "admin@tapandchew.com", "password": "password123" }

# Ruta protegida
GET http://localhost:8000/api/menu/products/
Authorization: Bearer {token}

# Sin token → 401
GET http://localhost:8000/api/menu/products/

# Servicio caído → 502
```

## Notas de diseño

- El gateway **no parsea el body** (`express.json()` eliminado) —
  hacerlo consumía el stream antes de que el proxy pudiera reenviarlo,
  dejando a los servicios destino sin datos.
- La validación de token es de **presencia**, no de firma. Cada
  microservicio valida su propio token (Sanctum en Laravel, Firebase
  en Order, etc.). El gateway solo garantiza que nadie llega sin token.
- `http-proxy-middleware v2` se usa sobre v3 por estabilidad —
  v3 cambió la API del error handler y genera comportamiento inesperado
  con Express en desarrollo.
- `JWT_SECRET` está en el `.env` preparado para cuando se migre
  a tokens JWT unificados en entregas posteriores.
- Las URLs de servicios en variables de entorno permiten apuntar
  a contenedores Docker en la Entrega #2 sin tocar el código.
```

---

## 3. Flujo y cambios explicados

**Flujo completo de una petición:**
```
Thunder Client
    │
    ▼
API Gateway :8000
    │  ¿Tiene Bearer token?
    │  ¿Es ruta pública?
    │
    ├─ Sin token → 401 (nunca llega al servicio)
    │
    ├─ Con token → reenvía la petición completa
    │   (headers, body, método) al servicio destino
    │
    ▼
Microservicio (:8001-8005)
    │  Valida token con su propio mecanismo
    │  Procesa la lógica de negocio
    │
    ▼
Respuesta viaja de vuelta por el proxy al cliente