const express = require('express');
const app     = express();

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'notifications-service', port: 8006 });
});

app.use('/api/notifications', require('./routes/notification.routes'));

module.exports = app;