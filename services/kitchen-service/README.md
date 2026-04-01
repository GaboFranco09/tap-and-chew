# Kitchen Service — tap&Chew

Microservicio de gestión de la cola de cocina del sistema tap&Chew.
Construido con **Flask 3** + **Flask-SQLAlchemy** + **MySQL**.

## Responsabilidad

Gestiona la cola de trabajo de la cocina: recibe los pedidos confirmados
desde el Order Service, permite a los cocineros marcar el progreso de
cada pedido ítem por ítem y sincroniza los cambios de estado en tiempo
real con Firebase para que el kiosko y el cliente vean el avance
instantáneamente.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Flask 3                 |
| ORM            | Flask-SQLAlchemy        |
| Migraciones    | Flask-Migrate           |
| Base de datos  | MySQL 8                 |
| Tiempo real    | Firebase Realtime DB    |
| Puerto         | 8004                    |

## Endpoints

| Método | Ruta                                              | Descripción                              |
|--------|---------------------------------------------------|------------------------------------------|
| GET    | /health                                           | Estado del servicio                      |
| GET    | /api/kitchen/queue                                | Cola activa (received + preparing)       |
| GET    | /api/kitchen/history                              | Últimos 50 pedidos completados           |
| POST   | /api/kitchen/orders                               | Recibir pedido desde Order Service       |
| PATCH  | /api/kitchen/orders/{order_id}/start              | Iniciar preparación del pedido           |
| PATCH  | /api/kitchen/orders/{order_id}/complete           | Marcar pedido como listo                 |
| PATCH  | /api/kitchen/orders/{order_id}/items/{id}/toggle  | Marcar/desmarcar ítem individual         |

## Estados de un pedido en cocina
```
received → preparing → ready
```

| Estado     | Descripción                                         |
|------------|-----------------------------------------------------|
| received   | Pedido recibido, esperando que cocina lo tome       |
| preparing  | Cocinero inició la preparación                      |
| ready      | Todos los ítems listos, pedido listo para entregar  |

## Modelos

**KitchenOrder** — registro de cada pedido en la cola de cocina.
```
id              INT PK
order_id        VARCHAR(36)     UUID del pedido en Order Service
kiosk_id        VARCHAR(50)     Kiosko de origen
status          ENUM            received | preparing | ready
notes           TEXT
total           DECIMAL(10,2)
received_at     DATETIME
started_at      DATETIME        Cuando cocina tomó el pedido
completed_at    DATETIME        Cuando se marcó como listo
```

**KitchenItem** — ítem individual dentro del pedido.
```
id                INT PK
kitchen_order_id  INT FK → kitchen_orders.id
product_id        VARCHAR(50)
name              VARCHAR(150)
quantity          INT
unit_price        DECIMAL(10,2)
is_ready          BOOLEAN         Marcado ítem a ítem por el cocinero
```

## Instalación local
```bash
cd services/kitchen-service
python -m venv venv
source venv/Scripts/activate      # Windows
pip install -r requirements.txt
cp .env.example .env              # completar con credenciales locales
cp ../order-service/src/config/firebase-credentials.json app/config/firebase-credentials.json
flask db upgrade
python run.py
```

## Base de datos
```
Nombre:    tapandchew_kitchen
Motor:     MySQL 8
Tablas:    kitchen_orders, kitchen_items
```

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

FIREBASE_DATABASE_URL=
FIREBASE_CREDENTIALS_PATH=app/config/firebase-credentials.json

PORT=8004
```

## Ejemplos de uso

**Cola activa:**
```json
GET /api/kitchen/queue

[
  {
    "id": 1,
    "order_id": "uuid-del-pedido",
    "kiosk_id": "kiosk-01",
    "status": "received",
    "notes": "Sin cebolla",
    "total": 34500.0,
    "received_at": "2026-04-01T10:32:00",
    "started_at": null,
    "completed_at": null,
    "items": [
      { "id": 1, "name": "Classic Burger", "quantity": 2, "unit_price": 12500.0, "is_ready": false },
      { "id": 2, "name": "Coca-Cola",       "quantity": 2, "unit_price": 4500.0,  "is_ready": false }
    ]
  }
]
```

**Iniciar preparación:**
```json
PATCH /api/kitchen/orders/{order_id}/start

{
  "message": "Preparación iniciada.",
  "order": { "status": "preparing", "started_at": "2026-04-01T10:33:45", ... }
}
```

**Toggle ítem:**
```json
PATCH /api/kitchen/orders/{order_id}/items/1/toggle

{
  "message": "Ítem actualizado.",
  "item_id": 1,
  "is_ready": true
}
```

**Completar pedido:**
```json
PATCH /api/kitchen/orders/{order_id}/complete

{
  "message": "Pedido listo para entregar.",
  "order": { "status": "ready", "completed_at": "2026-04-01T10:39:10", ... }
}
```

## Credenciales Firebase

El archivo `firebase-credentials.json` no se versiona en el repositorio.
Se comparte con el Order Service — es el mismo proyecto Firebase:
```
Firebase Console → Project Settings → Service Accounts
→ Generate new private key
```

Guardarlo en `app/config/firebase-credentials.json`.

## Notas de diseño

- Flask se eligió por su ligereza — la lógica de cocina es simple pero
  crítica: recibir, actualizar y registrar tiempos. No necesita el peso
  de Django ni la concurrencia de Express.
- El servicio **sincroniza Firebase en cada cambio de estado** (start y
  complete), garantizando que el kiosko y el Order Service siempre
  reflejan el estado real del pedido sin polling.
- Los pedidos **no se eliminan** — `history` muestra los últimos 50
  completados para análisis operacional del turno.
- `toggle_item` permite al cocinero marcar ítems individualmente mientras
  prepara, dando visibilidad granular al display de cocina.
- En producción, `started_at` y `completed_at` permiten calcular tiempos
  promedio de preparación por producto o turno.