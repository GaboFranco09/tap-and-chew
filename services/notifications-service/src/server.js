require('dotenv').config();
const app       = require('./app');
const connectDB = require('./config/database');

const PORT = process.env.PORT || 8006;

connectDB().then(() => {
    app.listen(PORT, () => {
        console.log(`Notifications Service corriendo en http://localhost:${PORT}`);
    });
});