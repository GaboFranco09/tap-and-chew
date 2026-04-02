const PUBLIC_ROUTES = [
    { method: 'POST', path: '/api/auth/login'           },
    { method: 'POST', path: '/api/auth/register'        },
    { method: 'POST', path: '/api/auth/forgot-password' },
    { method: 'POST', path: '/api/auth/reset-password'  },
    { method: 'GET',  path: '/health'                   },
];

const isPublic = (req) =>
    PUBLIC_ROUTES.some(
        (r) => r.method === req.method && req.path.startsWith(r.path)
    );

const authenticate = (req, res, next) => {
    if (isPublic(req)) return next();

    const header = req.headers['authorization'];
    if (!header || !header.startsWith('Bearer ')) {
        return res.status(401).json({ message: 'Token requerido.' });
    }

    // El token se reenvía al servicio destino — cada servicio valida el suyo
    next();
};

module.exports = authenticate;