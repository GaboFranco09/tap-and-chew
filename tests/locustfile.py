from locust import HttpUser, task, between
import json

VALID_TOKEN   = ""   # se llena en FASE 5
INTERNAL_SECRET = "tapandchew-internal-secret-2026"


class TapAndChewUser(HttpUser):
    host        = "http://localhost:8000"
    wait_time   = between(0.5, 1.5)
    token       = None

    def on_start(self):
        """Se ejecuta al inicio de cada usuario simulado — hace login."""
        res = self.client.post(
            "/api/auth/login",
            json={"email": "admin@tapandchew.com", "password": "password123"},
        )
        if res.status_code == 200:
            self.token = res.json().get("token")

    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    # TEST 1: health del gateway
    @task(1)
    def test_health(self):
        self.client.get("/api/health", name="T01 - Health Gateway")

    # TEST 2: login válido
    @task(2)
    def test_login(self):
        self.client.post(
            "/api/auth/login",
            json={"email": "admin@tapandchew.com", "password": "password123"},
            name="T02 - Login válido",
        )

    #TEST 3: login con credenciales inválidas
    @task(1)
    def test_login_invalid(self):
        self.client.post(
            "/api/auth/login",
            json={"email": "noexiste@test.com", "password": "wrong"},
            name="T03 - Login inválido",
        )

    #TEST 4: acceso sin token (debe retornar 401)
    @task(1)
    def test_no_token(self):
        with self.client.get(
            "/api/menu/products",
            name="T04 - Sin token → 401",
            catch_response=True,
        ) as res:
            if res.status_code == 401:
                res.success()
            else:
                res.failure(f"Esperado 401, recibido {res.status_code}")

    #TEST 5: listar productos (autenticado)
    @task(3)
    def test_get_products(self):
        self.client.get(
            "/api/menu/products",
            headers=self.auth_headers(),
            name="T05 - GET productos",
        )

    #TEST 6: listar categorías (autenticado) 
    @task(2)
    def test_get_categories(self):
        self.client.get(
            "/api/menu/categories",
            headers=self.auth_headers(),
            name="T06 - GET categorías",
        )

    #TEST 7: listar pedidos 
    @task(2)
    def test_get_orders(self):
        self.client.get(
            "/api/orders",
            headers=self.auth_headers(),
            name="T07 - GET pedidos",
        )

    # TEST 8: crear pedido
    @task(2)
    def test_create_order(self):
        self.client.post(
            "/api/orders",
            headers=self.auth_headers(),
            json={
                "kiosk_id": "kiosk-01",
                "items": [
                    {"product_id": "1", "name": "Classic Burger",
                     "quantity": 1, "unit_price": 12500}
                ],
                "notes": "Test Locust",
                "total": 12500,
            },
            name="T08 - POST crear pedido",
        )

    # TEST 9: cola de cocina
    @task(2)
    def test_kitchen_queue(self):
        self.client.get(
            "/api/kitchen/queue",
            headers=self.auth_headers(),
            name="T09 - GET cola cocina",
        )

    # TEST 10: flood login (rate limiting)
    @task(1)
    def test_flood_login(self):
        with self.client.post(
            "/api/auth/login",
            json={"email": "flood@test.com", "password": "wrong"},
            name="T10 - Flood login → 429",
            catch_response=True,
        ) as res:
            if res.status_code in [401, 429]:
                res.success()
            else:
                res.failure(f"Inesperado: {res.status_code}")