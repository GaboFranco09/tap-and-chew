# Notifications Service — tap&Chew

Microservicio de notificaciones del sistema tap&Chew.
Construido con **Express.js** + **Mongoose** + **MongoDB**.

## Responsabilidad

Registra y gestiona las notificaciones de eventos del sistema asociadas
a cada pedido: confirmación, pedido listo y pago procesado. Permite
consultar el historial de notificaciones por pedido y marcarlas como
leídas. Solo acepta peticiones provenientes del API Gateway.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Express.js              |
| ORM            | Mongoose                |
| Base de datos  | MongoDB                 |
| Puerto         | 8006                    |

## Endpoints

| Método | Ruta                              | Descripción                        |
|--------|-----------------------------------|------------------------------------|
| GET    | /health                           | Estado del servicio                |
| GET    | /api/notifications/order/:order_id| Notificaciones de un pedido        |
| POST   | /api/notifications                | Crear notificación                 |
| PATCH  | /api/notifications/:id/read       | Marcar notificación como leída     |

## Tipos de notificación

| Tipo                | Descripción                        |
|---------------------|------------------------------------|
| order_confirmed     | Pedido confirmado y enviado a cocina|
| order_ready         | Pedido listo para retirar          |
| payment_processed   | Pago registrado exitosamente       |

## Modelos

**Notification**
_id       ObjectId PK
order_id  String
type      ENUM order_confirmed | order_ready | payment_processed
message   String
is_read   Boolean (default: false)
createdAt Date
updatedAt Date

## Instalación local

```bash
cd services/notifications-service
npm install
cp .env.example .env
npm run dev
```

## Base de datos
Motor:      MongoDB
Puerto:     27017
Colección:  notifications

## Variables de entorno requeridas

```env
PORT=8006
NODE_ENV=development
MONGO_URI=mongodb://127.0.0.1:27017/tapandchew_notifications
INTERNAL_SECRET=
```

## Ejemplos de uso

```json
POST /api/notifications
X-Internal-Secret: {INTERNAL_SECRET}
{
  "order_id": "abc123",
  "type": "order_confirmed",
  "message": "Tu pedido ha sido confirmado y está en preparación."
}
```

**Consultar por pedido:**
GET /api/notifications/order/abc123
X-Internal-Secret: {INTERNAL_SECRET}

**Sin secret → 403:**
```json
{ "message": "Acceso denegado. Debe pasar por el API Gateway." }
```

## Notas de diseño

- Servicio creado en Entrega #2 para reemplazar el api-gateway Express
  que fue deprecado al unificar Gateway + Auth en Laravel.
- Diseño deliberadamente simple — registra eventos, no los procesa.
- `is_read` permite al kiosko saber qué notificaciones ya fueron vistas.
- `internalAuth` middleware bloquea acceso directo sin el secret.