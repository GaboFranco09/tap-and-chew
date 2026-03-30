# Menu Service — tap&Chew

Microservicio de gestión del menú del sistema tap&Chew.
Construido con **Django 5** + **Django REST Framework** + **PostgreSQL**.

## Responsabilidad

Gestiona el catálogo completo del restaurante: categorías, productos y combos.
Es el servicio consultado por el kiosko para mostrar el menú al cliente
y por el Order Service al momento de crear un pedido.

## Stack

| Componente     | Tecnología                  |
|----------------|-----------------------------|
| Framework      | Django 5 + DRF              |
| Base de datos  | PostgreSQL 18               |
| Puerto         | 8002                        |
| Admin panel    | Django Admin (incluido)     |

## Endpoints

| Método | Ruta                              | Descripción                        |
|--------|-----------------------------------|------------------------------------|
| GET    | /api/menu/categories/             | Listar todas las categorías        |
| POST   | /api/menu/categories/             | Crear categoría                    |
| GET    | /api/menu/categories/{id}/        | Detalle de categoría               |
| PUT    | /api/menu/categories/{id}/        | Actualizar categoría               |
| DELETE | /api/menu/categories/{id}/        | Eliminar categoría                 |
| GET    | /api/menu/categories/active/      | Solo categorías activas            |
| GET    | /api/menu/products/               | Listar todos los productos         |
| POST   | /api/menu/products/               | Crear producto                     |
| GET    | /api/menu/products/{id}/          | Detalle de producto                |
| PUT    | /api/menu/products/{id}/          | Actualizar producto                |
| DELETE | /api/menu/products/{id}/          | Eliminar producto                  |
| GET    | /api/menu/products/available/     | Solo productos activos y disponibles|
| GET    | /api/menu/products/?category={id} | Filtrar productos por categoría    |
| GET    | /api/menu/combos/                 | Listar todos los combos            |
| POST   | /api/menu/combos/                 | Crear combo                        |
| GET    | /api/menu/combos/{id}/            | Detalle de combo                   |
| PUT    | /api/menu/combos/{id}/            | Actualizar combo                   |
| DELETE | /api/menu/combos/{id}/            | Eliminar combo                     |
| GET    | /api/menu/combos/active/          | Solo combos activos                |

## Modelos

**Category** — agrupa los productos del menú.

**Product** — ítem individual con precio, disponibilidad y categoría.

**Combo** — agrupación de productos con precio especial.

## Instalación local
```bash
cd services/menu-service
python -m venv venv
source venv/Scripts/activate      # Windows
pip install -r requirements.txt
cp .env.example .env              # completar con credenciales locales
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata menu/fixtures/initial_data.json
python manage.py runserver 8002
```

## Base de datos
```
Nombre:    tapandchew_menu
Motor:     PostgreSQL 18
Tablas:    menu_category, menu_product,
           menu_combo, menu_combo_products
```

## Variables de entorno requeridas
```env
DEBUG=True
SECRET_KEY=
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=tapandchew_menu
DB_USER=postgres
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=5432
```

## Datos de prueba

El fixture incluido carga 2 categorías y 3 productos de ejemplo:
```bash
python manage.py loaddata menu/fixtures/initial_data.json
# Installed 5 object(s) from 1 fixture(s)
```

## Admin de Django

Disponible en `http://localhost:8002/admin/` — permite gestionar
categorías, productos y combos directamente desde el navegador
sin necesidad de un cliente HTTP externo.

## Notas de diseño

- Los endpoints no requieren autenticación directa — la validación
  de tokens ocurre en el API Gateway antes de llegar a este servicio.
- `is_active` controla visibilidad general. `is_available` en Product
  controla disponibilidad en tiempo real (se puede agotar un producto
  sin desactivarlo completamente).
- Los combos usan relación ManyToMany con productos, permitiendo
  armar paquetes flexibles sin duplicar datos.