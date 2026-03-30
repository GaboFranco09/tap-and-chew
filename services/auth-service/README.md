# Auth Service — tap&Chew

Microservicio de autenticación y gestión de identidad del sistema tap&Chew.
Construido con **Laravel 11** + **MySQL**.

## Responsabilidad

Gestiona el ciclo de vida completo de la identidad:
registro, autenticación, sesiones y recuperación de contraseña.
Todos los demás microservicios dependen de los tokens que este servicio emite.

## Stack

| Componente     | Tecnología              |
|----------------|-------------------------|
| Framework      | Laravel 11              |
| Autenticación  | Laravel Sanctum (tokens)|
| Base de datos  | MySQL 8                 |
| Puerto         | 8001                    |

## Endpoints

| Método | Ruta                        | Auth | Descripción                        |
|--------|-----------------------------|------|------------------------------------|
| POST   | /api/auth/register          | No   | Registrar nuevo usuario            |
| POST   | /api/auth/login             | No   | Iniciar sesión, retorna token      |
| POST   | /api/auth/logout            | Sí   | Revocar token actual               |
| GET    | /api/auth/me                | Sí   | Datos del usuario autenticado      |
| POST   | /api/auth/forgot-password   | No   | Enviar enlace de recuperación      |
| POST   | /api/auth/reset-password    | No   | Resetear contraseña con token      |

## Roles disponibles

| Rol       | Descripción                              |
|-----------|------------------------------------------|
| admin     | Acceso total al sistema                  |
| cashier   | Gestión de pagos y cierre de pedidos     |
| kitchen   | Visualización y gestión de cola cocina   |
| customer  | Realiza pedidos desde el kiosko          |

## Instalación local
```bash
cd services/auth-service
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve --port=8001
```

## Base de datos
```
Nombre:    tapandchew_auth
Motor:     MySQL 8
Tablas:    users, password_reset_tokens,
           sessions, personal_access_tokens
```

## Ejemplos de uso

**Registro:**
```json
POST /api/auth/register
{
  "name": "Gabriel Admin",
  "email": "admin@tapandchew.com",
  "password": "password123",
  "password_confirmation": "password123",
  "role": "admin"
}
```

**Login:**
```json
POST /api/auth/login
{
  "email": "admin@tapandchew.com",
  "password": "password123"
}
```

**Respuesta login:**
```json
{
  "message": "Login exitoso.",
  "user": {
    "id": 1,
    "name": "Gabriel Admin",
    "email": "admin@tapandchew.com",
    "role": "admin"
  },
  "token": "1|abc123..."
}
```

**Endpoints protegidos** requieren header:
```
Authorization: Bearer {token}
```

## Variables de entorno requeridas
```env
APP_NAME=TapAndChew-Auth
APP_URL=http://localhost:8001
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=tapandchew_auth
DB_USERNAME=root
DB_PASSWORD=
```

## Notas de diseño

- Cada login revoca todos los tokens anteriores del usuario — una sesión activa por usuario.
- El campo `is_active` permite deshabilitar usuarios sin eliminarlos.
- Las contraseñas se hashean automáticamente con bcrypt via Laravel.
- En producción configurar SMTP en `.env` para recuperación de contraseña.