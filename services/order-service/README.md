# Order Service — tap&Chew

Microservicio de gestión de pedidos del sistema tap&Chew.
Construido con **Express** + **Firebase Realtime Database**.

## Responsabilidad

Gestiona el ciclo de vida completo de un pedido: desde que el cliente
lo confirma en el kiosko hasta que es entregado. Al usar Firebase Realtime
Database, cualquier cambio de estado es visible instantáneamente en la
pantalla de cocina sin necesidad de recargar.

## Stack

| Componente     | Tecnología                      |
|----------------|---------------------------------|
| Framework      | Express 4                       |
| Base de datos  | Firebase Realtime Database      |
| Puerto         | 8003                            |

## Endpoints

| Método | Ruta                          | Descripción                              |
|--------|-------------------------------|------------------------------------------|
| GET    | /health                       | Estado del servicio                      |
| POST   | /api/orders                   | Crear nuevo pedido                       |
| GET    | /api/orders                   | Listar todos los pedidos                 |
| GET    | /api/orders?status={status}   | Filtrar pedidos por estado               |
| GET    | /api/orders/status/pending    | Pedidos pendientes (pantalla de cocina)  |
| GET    | /api/orders/:id               | Detalle de un pedido                     |
| PATCH  | /api/orders/:id/status        | Actualizar estado del pedido             |
| DELETE | /api/orders/:id               | Cancelar pedido (cambio de estado)       |

## Estados de un pedido
```
pending → confirmed → preparing → ready → delivered
                                        ↘ cancelled
```

| Estado     | Descripción                                        |
|------------|----------------------------------------------------|
| pending    | Pedido creado, esperando confirmación              |
| confirmed  | Confirmado, enviado a cocina                       |
| preparing  | Cocina está preparando el pedido                   |
| ready      | Listo para entregar al cliente                     |
| delivered  | Entregado                                          |
| cancelled  | Cancelado (no se puede cancelar si está preparing) |

## Estructura del pedido en Firebase
```json
{
  "orders": {
    "{uuid}": {
      "id": "uuid-generado",
      "kiosk_id": "kiosk-01",
      "items": [
        {
          "product_id": "1",
          "name": "Classic Burger",
          "quantity": 2,
          "unit_price": 12500
        }
      ],
      "notes": "Sin cebolla",
      "status": "pending",
      "total": 25000,
      "created_at": 1234567890,
      "updated_at": 1234567890
    }
  }
}
```

## Instalación local
```bash
cd services/order-service
npm install
cp .env.example .env
# Agregar firebase-credentials.json en src/config/
npm run dev
```

## Variables de entorno requeridas
```env
PORT=8003
FIREBASE_DATABASE_URL=https://tap-and-chew-default-rtdb.firebaseio.com
FIREBASE_CREDENTIALS_PATH=./src/config/firebase-credentials.json
```

## Credenciales Firebase

El archivo `firebase-credentials.json` no se versiona en el repositorio.
Para obtenerlo:
```
Firebase Console → Project Settings → Service Accounts
→ Generate new private key
```

Guardarlo en `src/config/firebase-credentials.json`.

## Notas de diseño

- Los pedidos no se eliminan físicamente — un DELETE cambia el estado
  a `cancelled` para mantener historial completo.
- Un pedido en estado `preparing` o `ready` no puede cancelarse.
- El endpoint `/api/orders/status/pending` es el que consume
  el Kitchen Service para mostrar la cola de cocina.
- Los cambios en Firebase son visibles en tiempo real desde la consola
  sin necesidad de recargar.