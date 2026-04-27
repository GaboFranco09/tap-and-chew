# ⚠️ DEPRECADO — API Gateway (Express)

Esta carpeta ya no está en uso activo desde la Entrega #2.

## ¿Qué pasó?

El API Gateway original fue implementado en Express. Durante la revisión
arquitectónica de la Entrega #2, Se identificó que los microservicios
seguían siendo accesibles directamente, rompiendo el principio de punto único
de entrada.

## Solución aplicada

Gateway y Auth Service fueron **unificados en un solo microservicio Laravel**
ubicado en `services/gateway-auth-service/`, que actúa como:

- Único punto de entrada del sistema
- Emisor y validador de JWT
- Router centralizado hacia los microservicios
- Rate limiting y middleware de seguridad global

## Se corrige la regla arquitectónica
Cliente → services/gateway-auth-service/ (puerto 8000) → Microservicios

Ningún microservicio acepta peticiones sin el header `X-Internal-Secret`.

## No eliminar esta carpeta

Se conserva como registro histórico del proceso de refactorización.