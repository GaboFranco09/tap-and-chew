import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from menu.models import Category, Product, Combo


INTERNAL_SECRET = 'tapandchew-internal-secret-2026'
WRONG_SECRET    = 'wrong-secret'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_headers():
    return {'HTTP_X_INTERNAL_SECRET': INTERNAL_SECRET}


@pytest.fixture
def wrong_headers():
    return {'HTTP_X_INTERNAL_SECRET': WRONG_SECRET}


@pytest.fixture
def category(db):
    return Category.objects.create(name='Hamburguesas', is_active=True)


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name='Classic Burger',
        price=12500,
        category=category,
        is_active=True,
        is_available=True,
    )


@pytest.fixture
def combo(db, product):
    c = Combo.objects.create(name='Combo Clásico', price=18000, is_active=True)
    c.products.add(product)
    return c


# ─── TEST 1: listar categorías con secret ────────────────────────
@pytest.mark.django_db
def test_get_categories_with_secret(client, auth_headers, category):
    response = client.get('/api/menu/categories/', **auth_headers)
    assert response.status_code == 200
    assert len(response.data) >= 1


# ─── TEST 2: bloqueo sin secret ──────────────────────────────────
@pytest.mark.django_db
def test_get_categories_without_secret(client):
    response = client.get('/api/menu/categories/')
    assert response.status_code == 403


# ─── TEST 3: bloqueo con secret incorrecto ───────────────────────
@pytest.mark.django_db
def test_get_categories_wrong_secret(client, wrong_headers):
    response = client.get('/api/menu/categories/', **wrong_headers)
    assert response.status_code == 403


# ─── TEST 4: crear categoría ─────────────────────────────────────
@pytest.mark.django_db
def test_create_category(client, auth_headers):
    response = client.post(
        '/api/menu/categories/',
        {'name': 'Bebidas', 'is_active': True},
        format='json',
        **auth_headers
    )
    assert response.status_code == 201
    assert response.data['name'] == 'Bebidas'


# ─── TEST 5: categorías activas ──────────────────────────────────
@pytest.mark.django_db
def test_get_active_categories(client, auth_headers, db):
    Category.objects.create(name='Activa', is_active=True)
    Category.objects.create(name='Inactiva', is_active=False)
    response = client.get('/api/menu/categories/active/', **auth_headers)
    assert response.status_code == 200
    names = [c['name'] for c in response.data]
    assert 'Activa' in names
    assert 'Inactiva' not in names


# ─── TEST 6: listar productos ────────────────────────────────────
@pytest.mark.django_db
def test_get_products_with_secret(client, auth_headers, product):
    response = client.get('/api/menu/products/', **auth_headers)
    assert response.status_code == 200
    assert len(response.data) >= 1


# ─── TEST 7: productos disponibles ───────────────────────────────
@pytest.mark.django_db
def test_get_available_products(client, auth_headers, db, category):
    Product.objects.create(
        name='Disponible', price=5000, category=category,
        is_active=True, is_available=True
    )
    Product.objects.create(
        name='No disponible', price=5000, category=category,
        is_active=True, is_available=False
    )
    response = client.get('/api/menu/products/available/', **auth_headers)
    assert response.status_code == 200
    names = [p['name'] for p in response.data]
    assert 'Disponible' in names
    assert 'No disponible' not in names


# ─── TEST 8: listar combos activos ───────────────────────────────
@pytest.mark.django_db
def test_get_active_combos(client, auth_headers, combo, db, product):
    Combo.objects.create(name='Inactivo', price=9000, is_active=False)
    response = client.get('/api/menu/combos/active/', **auth_headers)
    assert response.status_code == 200
    names = [c['name'] for c in response.data]
    assert 'Combo Clásico' in names
    assert 'Inactivo' not in names