# Payment Service — tap&Chew

Microservicio de gestión de pagos del sistema tap&Chew.
Construido con **Express.js** + **Mongoose** + **MongoDB**.

## Responsabilidad

Gestiona el registro de pagos asociados a los pedidos del sistema.
Permite crear pagos únicos por pedido, consultarlos, filtrarlos,
generar estadísticas diarias y procesar reembolsos controlados.
Solo acepta peticiones provenientes del API Gateway.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Express.js              |
| ORM            | Mongoose                |
| Base de datos  | MongoDB                 |
| Validación     | express-validator       |
| Puerto         | 8005                    |

## Endpoints

| Método | Ruta                       | Descripción                   |
|--------|----------------------------|-------------------------------|
| GET    | /health                    | Estado del servicio           |
| GET    | /api/payments              | Listar pagos                  |
| GET    | /api/payments/stats        | Estadísticas del día          |
| GET    | /api/payments/order/:id    | Pago por order_id             |
| GET    | /api/payments/:id          | Pago por _id                  |
| POST   | /api/payments              | Registrar pago                |
| PATCH  | /api/payments/:id/refund   | Procesar reembolso            |

## Estados de un pago

| Estado    | Descripción                    |
|-----------|--------------------------------|
| pending   | Pago creado sin confirmar      |
| completed | Pago procesado correctamente   |
| refunded  | Pago reembolsado               |
| failed    | Pago fallido                   |

## Modelos

**Payment**
_id             ObjectId PK
order_id        String (unique)
kiosk_id        String
items           Array
subtotal        Number
discount        Number
tip             Number
total           Number
payment_method  ENUM cash | card | qr
status          ENUM pending | completed | failed | refunded
receipt_number  String (unique, auto-generado)
notes           String
createdAt       Date
updatedAt       Date

## Instalación local

```bash
cd services/payment-service
npm install
cp .env.example .env
npm run dev
```

## Base de datos
Motor:      MongoDB
Puerto:     27017
Colección:  payments

## Variables de entorno requeridas

```env
PORT=8005
NODE_ENV=development
MONGO_URI=mongodb://127.0.0.1:27017/tapandchew_payments
INTERNAL_SECRET=
```

## Ejemplos de uso

```json
POST /api/payments
X-Internal-Secret: {INTERNAL_SECRET}
{
  "order_id": "abc123",
  "kiosk_id": "kiosk-01",
  "items": [{ "product_id": "1", "name": "Classic Burger", "quantity": 2, "unit_price": 12500 }],
  "subtotal": 25000,
  "discount": 0,
  "tip": 1000,
  "total": 26000,
  "payment_method": "card"
}
```

**Sin secret → 403:**
```json
{ "message": "Acceso denegado. Debe pasar por el API Gateway." }
```

## Notas de diseño

- `order_id` es único — evita pagos duplicados por pedido.
- Solo pagos `completed` pueden ser reembolsados (idempotencia básica).
- `receipt_number` se genera automáticamente en el hook `pre('save')`.
- `/stats` usa agregaciones MongoDB para cálculos en tiempo real.
- `internalAuth` middleware bloquea acceso directo sin el secret.