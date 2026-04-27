# Kitchen Service — tap&Chew

Microservicio de gestión de la cola de cocina del sistema tap&Chew.
Construido con **Flask 3** + **Flask-SQLAlchemy** + **MySQL**.

## Responsabilidad

Gestiona la cola de trabajo de la cocina: sincroniza pedidos confirmados
desde el Order Service vía HTTP, permite a los cocineros marcar el progreso
de cada pedido y actualiza el estado en el Order Service al completar.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Flask 3                 |
| ORM            | Flask-SQLAlchemy        |
| Migraciones    | Flask-Migrate           |
| Base de datos  | MySQL 8                 |
| Puerto         | 8004                    |

## Endpoints

| Método | Ruta                                              | Descripción                        |
|--------|---------------------------------------------------|------------------------------------|
| GET    | /health                                           | Estado del servicio                |
| GET    | /api/kitchen/queue                                | Cola activa (received + preparing) |
| GET    | /api/kitchen/history                              | Últimos 50 pedidos completados     |
| POST   | /api/kitchen/sync                                 | Sincronizar cola desde Order Service|
| POST   | /api/kitchen/orders                               | Recibir pedido manualmente         |
| PATCH  | /api/kitchen/orders/{order_id}/start              | Iniciar preparación                |
| PATCH  | /api/kitchen/orders/{order_id}/complete           | Marcar pedido como listo           |
| PATCH  | /api/kitchen/orders/{order_id}/items/{id}/toggle  | Marcar ítem individual             |

## Estados en cocina
received → preparing → ready

## Modelos

**KitchenOrder**
id              INT PK
order_id        VARCHAR(36)
kiosk_id        VARCHAR(50)
status          ENUM received | preparing | ready
notes           TEXT
total           DECIMAL(10,2)
received_at     DATETIME
started_at      DATETIME
completed_at    DATETIME

**KitchenItem**
id                INT PK
kitchen_order_id  INT FK
product_id        VARCHAR(50)
name              VARCHAR(150)
quantity          INT
unit_price        DECIMAL(10,2)
is_ready          BOOLEAN

## Instalación local

```bash
cd services/kitchen-service
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
python run.py
```

## Base de datos
Nombre:    tapandchew_kitchen
Motor:     MySQL 8
Tablas:    kitchen_orders, kitchen_items

## Variables de entorno requeridas

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=

DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=tapandchew_kitchen
DB_USER=root
DB_PASSWORD=

ORDER_SERVICE_URL=http://127.0.0.1:8003
INTERNAL_SECRET=

PORT=8004
```

## Ejemplos de uso
Sincronizar cola desde Order Service
POST /api/kitchen/sync
X-Internal-Secret: {INTERNAL_SECRET}
→ { "message": "3 pedidos sincronizados desde Order Service.", "synced": 3 }
Iniciar preparación
PATCH /api/kitchen/orders/{order_id}/start
X-Internal-Secret: {INTERNAL_SECRET}
Sin secret → 403
GET /api/kitchen/queue
→ { "message": "Acceso denegado. Debe pasar por el API Gateway." }

## Notas de diseño

- Firebase eliminado en Entrega #2 — la sincronización en tiempo real
  se reemplaza por consulta HTTP directa al Order Service.
- `/api/kitchen/sync` obtiene pedidos en estado `pending` y `confirmed`
  desde Order Service y los registra localmente en MySQL.
- Al completar un pedido, Kitchen Service notifica al Order Service
  vía HTTP para actualizar el estado global.
- La comunicación service-to-service usa `X-Internal-Secret` como
  mecanismo de autenticación interno.