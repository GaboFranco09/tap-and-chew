require('dotenv').config();
const app       = require('./app');
const connectDB = require('./config/database');

const PORT = process.env.PORT || 8005;

connectDB().then(() => {
    app.listen(PORT, () => {
        console.log(`Payment Service corriendo en http://localhost:${PORT}`);
        console.log("SERVER CORRECTO LEVANTADO");
    });
});