const rateLimit = require('express-rate-limit');

const defaultLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max:      100,
    standardHeaders: true,
    legacyHeaders:   false,
    message: { message: 'Demasiadas solicitudes, intenta de nuevo en 15 minutos.' },
});

const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max:      10,
    standardHeaders: true,
    legacyHeaders:   false,
    message: { message: 'Demasiados intentos de autenticación.' },
});

module.exports = { defaultLimiter, authLimiter };