require('dotenv').config();
const app       = require('./app');
const connectDB = require('./config/database');

const PORT = process.env.PORT || 8003;

connectDB().then(() => {
    app.listen(PORT, () => {
        console.log(`Order Service corriendo en http://localhost:${PORT}`);
    });
});