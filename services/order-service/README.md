# Order Service — tap&Chew

Microservicio de gestión de pedidos del sistema tap&Chew.
Construido con **Express** + **Mongoose** + **MongoDB**.

## Responsabilidad

Gestiona el ciclo de vida completo de un pedido: desde que el cliente
lo confirma en el kiosko hasta que es entregado. Persiste los pedidos
en MongoDB y expone el estado actualizado para que el Kitchen Service
lo consulte vía HTTP.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Express 4               |
| ORM            | Mongoose                |
| Base de datos  | MongoDB                 |
| Puerto         | 8003                    |

## Endpoints

| Método | Ruta                        | Descripción                        |
|--------|-----------------------------|------------------------------------|
| GET    | /health                     | Estado del servicio                |
| GET    | /api/orders                 | Listar pedidos (filtro por status) |
| GET    | /api/orders/status/pending  | Pedidos pending y confirmed        |
| GET    | /api/orders/:id             | Detalle de un pedido               |
| POST   | /api/orders                 | Crear nuevo pedido                 |
| PATCH  | /api/orders/:id/status      | Actualizar estado                  |
| DELETE /api/orders/:id             | Cancelar pedido           |

## Estados de un pedido
pending → confirmed → preparing → ready → delivered
↘ cancelled

| Estado     | Descripción                                          |
|------------|------------------------------------------------------|
| pending    | Pedido creado, esperando confirmación                |
| confirmed  | Confirmado, enviado a cocina                         |
| preparing  | Cocina está preparando                               |
| ready      | Listo para entregar                                  |
| delivered  | Entregado al cliente                                 |
| cancelled  | Cancelado — no aplica si está preparing/ready/delivered |

## Modelos

**Order** — pedido completo.
_id         ObjectId PK
kiosk_id    String
items       Array (product_id, name, quantity, unit_price)
notes       String
status      Enum
total       Number
createdAt   Date
updatedAt   Date

## Instalación local

```bash
cd services/order-service
npm install
cp .env.example .env
npm run dev
```

## Base de datos
Motor:      MongoDB
Puerto:     27017
Colección:  orders

## Variables de entorno requeridas

```env
PORT=8003
NODE_ENV=development
MONGO_URI=mongodb://127.0.0.1:27017/tapandchew_orders
INTERNAL_SECRET=
```

## Ejemplos de uso

```json
POST /api/orders
X-Internal-Secret: {INTERNAL_SECRET}
{
  "kiosk_id": "kiosk-01",
  "items": [
    { "product_id": "1", "name": "Classic Burger", "quantity": 2, "unit_price": 12500 }
  ],
  "notes": "Sin cebolla",
  "total": 25000
}
```

**Sin secret → 403:**
```json
{ "message": "Acceso denegado. Debe pasar por el API Gateway." }
```

## Notas de diseño

- Firebase eliminado en Entrega #2 — persistencia migrada a MongoDB
  para consistencia arquitectónica con Payment y Notifications.
- El endpoint `/api/orders/status/pending` es consumido directamente
  por Kitchen Service (service-to-service con X-Internal-Secret).
- Los pedidos no se eliminan físicamente — DELETE cambia estado a
  `cancelled` para mantener historial completo.
- `internalAuth` middleware bloquea cualquier acceso sin el secret.