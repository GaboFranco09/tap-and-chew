# Gateway Auth Service — tap&Chew

Punto de entrada único del sistema tap&Chew.
Construido con **Laravel 11** + **JWT** + **MySQL**.

## Responsabilidad

Actúa simultáneamente como API Gateway y servicio de autenticación.
Todas las peticiones externas pasan obligatoriamente por este servicio,
que valida la identidad del usuario, aplica rate limiting y enruta
cada petición al microservicio correspondiente mediante controladores
específicos por dominio.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Laravel 11              |
| Autenticación  | tymon/jwt-auth (JWT)    |
| Base de datos  | MySQL 8                 |
| Puerto         | 8000                    |

## Endpoints — Auth

| Método | Ruta                        | Auth | Descripción                    |
|--------|-----------------------------|------|--------------------------------|
| GET    | /api/health                 | No   | Estado del servicio            |
| POST   | /api/auth/register          | No   | Registrar nuevo usuario        |
| POST   | /api/auth/login             | No   | Login — retorna JWT            |
| POST   | /api/auth/forgot-password   | No   | Enviar enlace de recuperación  |
| POST   | /api/auth/reset-password    | No   | Resetear contraseña con token  |
| POST   | /api/auth/logout            | Sí   | Invalidar token JWT            |
| GET    | /api/auth/me                | Sí   | Datos del usuario autenticado  |

## Endpoints — Proxy a microservicios

| Prefijo              | Microservicio destino  | Puerto |
|----------------------|------------------------|--------|
| /api/menu/...        | Menu Service           | 8002   |
| /api/orders/...      | Order Service          | 8003   |
| /api/kitchen/...     | Kitchen Service        | 8004   |
| /api/payments/...    | Payment Service        | 8005   |
| /api/notifications/..| Notifications Service  | 8006   |

## Roles disponibles

| Rol       | Descripción                            |
|-----------|----------------------------------------|
| admin     | Acceso total al sistema                |
| cashier   | Gestión de pagos                       |
| kitchen   | Visualización y gestión de cola cocina |
| customer  | Realiza pedidos desde el kiosko        |

## Instalación local

```bash
cd services/gateway-auth-service
composer install
cp .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8000
```

## Base de datos
Nombre:    tapandchew_gateway
Motor:     MySQL 8
Tablas:    users, password_reset_tokens

## Variables de entorno requeridas

```env
APP_NAME=TapAndChew-Gateway
APP_URL=http://localhost:8000

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tapandchew_gateway
DB_USERNAME=root
DB_PASSWORD=

JWT_SECRET=
JWT_TTL=60

INTERNAL_SECRET=

MS_MENU_URL=http://127.0.0.1:8002
MS_ORDER_URL=http://127.0.0.1:8003
MS_KITCHEN_URL=http://127.0.0.1:8004
MS_PAYMENT_URL=http://127.0.0.1:8005
MS_NOTIFICATIONS_URL=http://127.0.0.1:8006
```

## Ejemplos de uso

**Login:**
```json
POST /api/auth/login
{
  "email": "admin@tapandchew.com",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "message": "Login exitoso.",
  "user": { "id": 1, "name": "Gabriel Admin", "email": "admin@tapandchew.com", "role": "admin" },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Petición a microservicio (con token):**
GET /api/menu/products
Authorization: Bearer {token}

**Sin token → 401:**
```json
{ "message": "Token requerido." }
```

## Notas de diseño

- JWT reemplaza a Sanctum — los tokens son autocontenidos y no requieren
  consulta a BD para validarse, eliminando acoplamiento con los microservicios.
- Cada microservicio tiene su controlador dedicado en el gateway:
  MenuController, OrderController, KitchenController, PaymentController,
  NotificationsController. No existe proxy genérico.
- El header `X-Internal-Secret` se inyecta en cada petición saliente
  hacia los microservicios, garantizando que ninguno sea accesible
  directamente sin pasar por el gateway.
- Rate limiting: 10 req/15min sobre rutas de autenticación para
  prevenir ataques de fuerza bruta.
- `JWT_TTL` configura la duración del token en minutos (por defecto 60).