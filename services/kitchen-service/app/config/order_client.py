import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://127.0.0.1:8003')
INTERNAL_SECRET   = os.getenv('INTERNAL_SECRET', '')

INTERNAL_HEADERS = {
    'X-Internal-Secret': INTERNAL_SECRET,
    'Content-Type':      'application/json',
    'Accept':            'application/json',
}


def get_pending_orders():
    """Obtiene pedidos confirmed y pending desde Order Service."""
    response = requests.get(
        f'{ORDER_SERVICE_URL}/api/orders/status/pending',
        headers=INTERNAL_HEADERS,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def update_order_status(order_id: str, status: str):
    """Actualiza el estado de un pedido en Order Service."""
    response = requests.patch(
        f'{ORDER_SERVICE_URL}/api/orders/{order_id}/status',
        json={'status': status},
        headers=INTERNAL_HEADERS,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()