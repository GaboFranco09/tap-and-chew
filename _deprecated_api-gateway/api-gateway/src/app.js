const express     = require('express');
const cors        = require('cors');
const helmet      = require('helmet');
const morgan      = require('morgan');
const authenticate              = require('./middlewares/auth');
const { defaultLimiter, authLimiter } = require('./middlewares/rateLimit');
const registerProxies           = require('./routes/proxy.routes');

const app = express();

// Seguridad y utilidades
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));


// Health del gateway
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'api-gateway', port: 8000 });
});

// Rate limiting
app.use('/api/auth', authLimiter);
app.use(defaultLimiter);

// Autenticación centralizada
app.use(authenticate);

// Proxies hacia microservicios
registerProxies(app);

// Ruta no encontrada
app.use((req, res) => {
    res.status(404).json({ message: 'Ruta no encontrada.' });
});

module.exports = app;