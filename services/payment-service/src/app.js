const express  = require('express');
const app      = express();

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'payment-service', port: 8005 });
});

app.use('/api/payments', require('./routes/payment.routes'));

module.exports = app;