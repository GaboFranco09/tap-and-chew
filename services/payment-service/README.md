# Payment Service — tap&Chew

Microservicio de gestión de pagos del sistema tap&Chew.
Construido con **Express.js** + **Mongoose** + **MongoDB**.

## Responsabilidad

Gestiona el registro de pagos asociados a los pedidos del sistema.
Permite crear pagos únicos por pedido, consultarlos, filtrarlos,
generar estadísticas diarias y procesar reembolsos controlados,
asegurando consistencia mediante control de estados.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Express.js              |
| ORM            | Mongoose                |
| Base de datos  | MongoDB                 |
| Validación     | express-validator       |
| Entorno        | dotenv                  |
| Puerto         | 8005                    |

## Endpoints

| Método | Ruta                                   | Descripción                              |
|--------|----------------------------------------|------------------------------------------|
| GET    | /health                                | Estado del servicio                      |
| GET    | /api/payments                          | Listar pagos (filtros opcionales)        |
| GET    | /api/payments/stats                    | Estadísticas del día                     |
| GET    | /api/payments/order/{order_id}          | Obtener pago por order_id               |
| GET    | /api/payments/{id}                     | Obtener pago por _id                     |
| POST   | /api/payments                          | Registrar pago                           |
| PATCH  | /api/payments/{id}/refund              | Procesar reembolso                       |

## Estados de un pago

| Estado     | Descripción                                  |
|------------|----------------------------------------------|
| pending    | Pago creado pero no confirmado               |
| completed  | Pago procesado correctamente                 |
| refunded   | Pago reembolsado                             |
| failed     | Pago fallido                                 |


**Payment** — registro de cada pago en el sistema.
| ready      | Todos los ítems listos, pedido listo para entregar  |

## Modelos

**Payment** — registro de cada pago en el sistema.
```
_id ObjectId PK
order_id        String (unique) UUID del pedido (Order Service)
kiosk_id        String Kiosko de origen
items           Array Lista de productos

subtotal        Number
discount        Number
tip             Number
total N         umber

payment_method  ENUM cash | card | qr
status          ENUM pending | completed | failed | refunded

receipt_number  String (unique)
notes           String

createdAt       Date
updatedAt       Date
```

**PaymentItem** — ítem individual dentro del pago.
```
product_id      String
name            tring
quantity        Number
unit_price      Number

```

## Instalación local
```bash
cd services/payment-service
npm install
cp .env.example .env
npm run dev

```

# Base de datos
```
Motor:     MongoDB
Puerto:    27017
Colección: payments
```

## Variables de entorno requeridas
```env
PORT=8005
MONGO_URI=mongodb://127.0.0.1:27017/payment-service
```

## Ejemplos de uso
```json
POST /api/payments

{
  "order_id": "uuid-del-order-service",
  "kiosk_id": "kiosk-01",
  "items": [
    { "product_id": "1", "name": "Classic Burger", "quantity": 2, "unit_price": 12500 },
    { "product_id": "3", "name": "Coca-Cola",       "quantity": 2, "unit_price": 4500  }
  ],
  "subtotal": 34000,
  "discount": 0,
  "tip": 1000,
  "total": 35000,
  "payment_method": "card",
  "notes": "Sin novedad"
}
```

**Respuesta**
```json
{
  "message": "Pago registrado exitosamente.",
  "payment": { ... }
}
```

**Estadisticas del dia:**
```json
GET /api/payments/stats

{
  "today": {
    "total_revenue": 35000,
    "total_orders": 1,
    "avg_ticket": 35000
  },
  "by_method": [
    { "_id": "card", "count": 1, "total": 35000 }
  ]
}
```

**Reembolso**
```json
PATCH /api/payments/{id}/refund

{
  "message": "Reembolso procesado.",
  "payment": { "status": "refunded" }
}
```

## Credenciales 
No requiere credenciales externas.
MongoDB corre localmente.

## Notas de diseño
-MongoDB permite almacenar los ítems del pago sin necesidad de joins.
-order_id es único, evitando pagos duplicados por pedido.
-El flujo de estados controla la lógica de negocio: solo pagos completed pueden ser reembolsados.
-Se implementa validación para evitar doble reembolso (idempotencia básica).
-El servicio es desacoplado del Order Service, pero preparado para integración futura (validación de pedidos).
-El endpoint /stats utiliza agregaciones de MongoDB para cálculos en tiempo real sin necesidad de procesamiento adicional.


## Nota importante sobre Mongoose (BUG común)

En hooks de Mongoose modernos no usar next() si no es necesario.

Incorrecto:
paymentSchema.pre('save', function (next) {
    next();
});

Correcto:
paymentSchema.pre('save', function () {
    // lógica
});

Usar next() incorrectamente puede generar el error:
next is not a function
Este error puede confundirse con Express, pero proviene del modelo.

