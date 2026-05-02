require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const request  = require('supertest');
const mongoose = require('mongoose');
const app      = require('../app');

const SECRET       = 'tapandchew-internal-secret-2026';
const WRONG_SECRET = 'wrong-secret';

beforeAll(async () => {
    await mongoose.connect('mongodb://127.0.0.1:27017/tapandchew_notifications_test');
});

afterAll(async () => {
    await mongoose.connection.dropDatabase();
    await mongoose.connection.close();
});

afterEach(async () => {
    const collections = mongoose.connection.collections;
    for (const key in collections) {
        await collections[key].deleteMany({});
    }
});


// ─── TEST 1: health check ────────────────────────────────────────
describe('Health', () => {
    it('GET /health retorna 200', async () => {
        const res = await request(app).get('/health');
        expect(res.status).toBe(200);
        expect(res.body.service).toBe('notifications-service');
    });
});


// ─── TEST 2: bloqueo sin secret ──────────────────────────────────
describe('Seguridad — X-Internal-Secret', () => {
    it('POST /api/notifications sin secret retorna 403', async () => {
        const res = await request(app)
            .post('/api/notifications')
            .send({ order_id: 'abc', type: 'order_confirmed', message: 'Test' });
        expect(res.status).toBe(403);
    });

    // ─── TEST 3: secret incorrecto ───────────────────────────────
    it('POST /api/notifications con secret incorrecto retorna 403', async () => {
        const res = await request(app)
            .post('/api/notifications')
            .set('X-Internal-Secret', WRONG_SECRET)
            .send({ order_id: 'abc', type: 'order_confirmed', message: 'Test' });
        expect(res.status).toBe(403);
    });
});


// ─── TEST 4: crear notificación ──────────────────────────────────
describe('POST /api/notifications', () => {
    it('crea notificación con datos válidos', async () => {
        const res = await request(app)
            .post('/api/notifications')
            .set('X-Internal-Secret', SECRET)
            .send({
                order_id: 'order-123',
                type:     'order_confirmed',
                message:  'Tu pedido fue confirmado.',
            });
        expect(res.status).toBe(201);
        expect(res.body.notification.order_id).toBe('order-123');
        expect(res.body.notification.is_read).toBe(false);
    });

    // ─── TEST 5: campos faltantes ────────────────────────────────
    it('retorna 400 si faltan campos requeridos', async () => {
        const res = await request(app)
            .post('/api/notifications')
            .set('X-Internal-Secret', SECRET)
            .send({ order_id: 'order-123' });
        expect(res.status).toBe(400);
    });
});


// ─── TEST 6: obtener por order_id ────────────────────────────────
describe('GET /api/notifications/order/:order_id', () => {
    it('retorna notificaciones de un pedido', async () => {
        await request(app)
            .post('/api/notifications')
            .set('X-Internal-Secret', SECRET)
            .send({ order_id: 'order-456', type: 'order_ready', message: 'Listo.' });

        const res = await request(app)
            .get('/api/notifications/order/order-456')
            .set('X-Internal-Secret', SECRET);

        expect(res.status).toBe(200);
        expect(res.body.length).toBe(1);
        expect(res.body[0].order_id).toBe('order-456');
    });
});


// ─── TEST 7: marcar como leída ───────────────────────────────────
describe('PATCH /api/notifications/:id/read', () => {
    it('marca notificación como leída', async () => {
        const created = await request(app)
            .post('/api/notifications')
            .set('X-Internal-Secret', SECRET)
            .send({ order_id: 'order-789', type: 'payment_processed', message: 'Pago OK.' });

        const id  = created.body.notification._id;
        const res = await request(app)
            .patch(`/api/notifications/${id}/read`)
            .set('X-Internal-Secret', SECRET);

        expect(res.status).toBe(200);
        expect(res.body.notification.is_read).toBe(true);
    });
});