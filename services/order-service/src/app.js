const express = require('express');
const app     = express();

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'order-service', port: 8003 });
});

app.use('/api/orders', require('./routes/orderRoutes'));

module.exports = app;