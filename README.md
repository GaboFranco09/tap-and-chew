# tap&Chew 🍔

Sistema de autoservicio para restaurantes inspirado en los kioskos de McDonald's.
El cliente interactúa con una pantalla táctil, arma su pedido, paga
y la cocina lo recibe en tiempo real.

## Arquitectura

Sistema basado en microservicios con Gateway+Auth centralizado en Laravel.
Cliente (Kiosko)
│
▼
┌─────────────────────────────┐
│   Gateway + Auth Service    │  Laravel 11 + JWT — Puerto 8000
│   Único punto de entrada    │
└──────────┬──────────────────┘
│  X-Internal-Secret
┌─────┼──────────────────────────┐
▼     ▼        ▼        ▼        ▼
Menu   Orders  Kitchen  Payment  Notifications
:8002   :8003   :8004    :8005    :8006
Django  Express  Flask   Express   Express
PG    MongoDB  MySQL   MongoDB   MongoDB

**Regla arquitectónica:** ningún microservicio acepta peticiones sin
el header `X-Internal-Secret`. Todo tráfico pasa por el Gateway.

## Microservicios

| Servicio               | Framework     | Base de datos | Puerto | Estado  |
|------------------------|---------------|---------------|--------|---------|
| Gateway + Auth Service | Laravel 11    | MySQL         | 8000   | ✅ Listo |
| Menu Service           | Django 5      | PostgreSQL    | 8002   | ✅ Listo |
| Order Service          | Express       | MongoDB       | 8003   | ✅ Listo |
| Kitchen Service        | Flask 3       | MySQL         | 8004   | ✅ Listo |
| Payment Service        | Express       | MongoDB       | 8005   | ✅ Listo |
| Notifications Service  | Express       | MongoDB       | 8006   | ✅ Listo |

## Levantar el sistema (desarrollo local)

### Requisitos previos
- PHP 8.2+, Composer
- Python 3.11+
- Node.js 18+
- MySQL 8 (Laragon)
- PostgreSQL (Laragon)
- MongoDB (`mongod` directo)

### 1. Bases de datos
```bash
# MySQL — Laragon
mysql -u root -e "CREATE DATABASE tapandchew_gateway;"
mysql -u root -e "CREATE DATABASE tapandchew_kitchen;"

# PostgreSQL — Laragon
# Crear base de datos tapandchew_menu desde pgAdmin o psql

# MongoDB — automático al primer insert
mongod
```

### 2. Levantar servicios (una terminal por servicio)

```bash
# Gateway + Auth — Terminal 1
cd services/gateway-auth-service
php artisan serve --port=8000

# Menu Service — Terminal 2
cd services/menu-service
source venv/Scripts/activate
python manage.py runserver 8002

# Order Service — Terminal 3
cd services/order-service
npm run dev

# Kitchen Service — Terminal 4
cd services/kitchen-service
source venv/Scripts/activate
python run.py

# Payment Service — Terminal 5
cd services/payment-service
npm run dev

# Notifications Service — Terminal 6
cd services/notifications-service
npm run dev
```

### 3. Verificar que todo está activo

```bash
curl http://localhost:8000/api/health
curl http://localhost:8002/health  # requiere X-Internal-Secret
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8006/health
```

## Flujo de una venta

Cliente navega menú     → GET /api/menu/products (vía Gateway)
Confirma pedido         → POST /api/orders (vía Gateway)
Cocina sincroniza       → POST /api/kitchen/sync (vía Gateway)
Cocina prepara          → PATCH /api/kitchen/orders/{id}/start
Pedido listo            → PATCH /api/kitchen/orders/{id}/complete
Pago registrado         → POST /api/payments (vía Gateway)
Notificación generada   → POST /api/notifications (vía Gateway)


## Repositorio
main          → producción / entregas
develop       → integración
feature/      → una rama por servicio (activas entre entregas)

## Entregas

| Entrega | Descripción                          | Estado   |
|---------|--------------------------------------|-------------|----------|
| #1      | Implementación inicial               | ✅ v1.0-entrega1 |
| #2      | Dockerización + refactoring arquitectónico | 🔄 En progreso |
| #3      | CI/CD con Jenkins                    | 25 de mayo  | ⏳ Pendiente |

## Cambios arquitectónicos — Entrega #2

- **Gateway unificado:** Express gateway reemplazado por Laravel 11
  combinando Gateway + Auth en un solo servicio.
- **Firebase eliminado:** Order Service migró de Firebase a MongoDB.
  Kitchen Service ahora sincroniza vía HTTP con Order Service.
- **X-Internal-Secret:** todos los microservicios validan este header
  — acceso directo sin pasar por el Gateway retorna 403.
- **Notifications Service:** nuevo microservicio Express + MongoDB
  para eventos del sistema (pedido confirmado, listo, pago procesado).