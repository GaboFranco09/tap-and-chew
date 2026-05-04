# tap&Chew — Guía de despliegue con Docker

## Requisitos

- Docker 24+
- Docker Compose v2+
- Git

## Clonar el repositorio

```bash
git clone https://github.com/GaboFranco09/tap-and-chew.git
cd tap-and-chew
```

## Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y completa los valores requeridos:

```env
INTERNAL_SECRET=tapandchew-internal-secret-2026
JWT_SECRET=tu-jwt-secret-seguro
JWT_TTL=60

MYSQL_ROOT_PASSWORD=tu-password-mysql
MYSQL_GATEWAY_DB=tapandchew_gateway
MYSQL_KITCHEN_DB=tapandchew_kitchen

POSTGRES_DB=tapandchew_menu
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-password-postgres

MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=tu-password-mongo

MS_MENU_URL=http://menu:8002
MS_ORDER_URL=http://order:8003
MS_KITCHEN_URL=http://kitchen:8004
MS_PAYMENT_URL=http://payment:8005
MS_NOTIFICATIONS_URL=http://notifications:8006

APP_KEY=base64:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa=
APP_ENV=production
APP_DEBUG=false
```

## Construir imágenes

```bash
docker compose build
```

## Levantar bases de datos

```bash
docker compose up -d mysql postgres mongo
```

Espera ~15 segundos y verifica que estén healthy:

```bash
docker compose ps
# mysql, postgres y mongo deben mostrar (healthy)
```

## Generar APP_KEY de Laravel

```bash
docker compose up -d gateway
docker compose exec gateway php artisan key:generate --show
```

Copia el valor generado, actualiza `APP_KEY` en `.env` y reinicia:

```bash
docker compose restart gateway
```

## Levantar todos los servicios

```bash
docker compose up -d menu order kitchen payment notifications
docker compose ps
# Los 9 contenedores deben estar Up
```

## Ejecutar migraciones

```bash
# Laravel
docker compose exec gateway php artisan migrate --force

# Django
docker compose exec menu python manage.py migrate

# Flask
docker compose exec kitchen flask db init
docker compose exec kitchen flask db migrate -m "create kitchen tables"
docker compose exec kitchen flask db upgrade
```

## Verificar sistema

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Admin","email":"admin@tapandchew.com","password":"password123","password_confirmation":"password123","role":"admin"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@tapandchew.com","password":"password123"}'
```

Con el token del login prueba cualquier endpoint protegido:

```bash
curl http://localhost:8000/api/menu/categories \
  -H "Authorization: Bearer {token}"
```

## Servicios y puertos

| Servicio        | Puerto | Descripción              |
|-----------------|--------|--------------------------|
| Gateway + Auth  | 8000   | Único punto de entrada   |
| Menu Service    | 8002   | Catálogo del restaurante |
| Order Service   | 8003   | Gestión de pedidos       |
| Kitchen Service | 8004   | Cola de cocina           |
| Payment Service | 8005   | Registro de pagos        |
| Notifications   | 8006   | Notificaciones           |

## Comandos útiles

```bash
# Ver logs de un servicio
docker compose logs -f gateway

# Reiniciar un servicio
docker compose restart kitchen

# Reconstruir un servicio
docker compose build gateway
docker compose up -d gateway

# Bajar sin borrar datos
docker compose down

# Bajar y borrar todos los datos
docker compose down -v
```

## Flujo end-to-end de prueba

```
1. Register/Login          → POST /api/auth/login
2. Crear pedido            → POST /api/orders
3. Confirmar pedido        → PATCH /api/orders/{id}/status { "status": "confirmed" }
4. Sincronizar cocina      → POST /api/kitchen/sync
5. Ver cola                → GET /api/kitchen/queue
6. Iniciar preparación     → PATCH /api/kitchen/orders/{id}/start
7. Completar pedido        → PATCH /api/kitchen/orders/{id}/complete
8. Registrar pago          → POST /api/payments
9. Crear notificación      → POST /api/notifications
10. Logout                 → POST /api/auth/logout
```