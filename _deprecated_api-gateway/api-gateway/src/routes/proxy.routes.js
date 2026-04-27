const { createProxyMiddleware } = require('http-proxy-middleware');
const services = require('../config/services');

const proxy = (target) =>
    createProxyMiddleware({
        target,
        changeOrigin: true,
        onError: (err, req, res) => {
            res.status(502).json({
                message: 'Servicio no disponible.',
                service: target,
            });
        },
    });

module.exports = (app) => {
    app.use('/api/auth',    proxy(services.auth));
    app.use('/api/menu',    proxy(services.menu));
    app.use('/api/orders',  proxy(services.orders));
    app.use('/api/kitchen', proxy(services.kitchen));
    app.use('/api/payment', proxy(services.payment));
};