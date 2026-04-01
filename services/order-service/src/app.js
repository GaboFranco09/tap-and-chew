const express      = require('express')
const cors         = require('cors')
const morgan       = require('morgan')
const errorHandler = require('./middlewares/errorHandler')
const orderRoutes  = require('./routes/orderRoutes')
require('dotenv').config()

const app = express()

app.use(cors())
app.use(morgan('dev'))
app.use(express.json())

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'order-service', port: process.env.PORT })
})

// Rutas
app.use('/api/orders', orderRoutes)

// Manejo de rutas no encontradas
app.use((req, res) => {
  res.status(404).json({ message: 'Ruta no encontrada.' })
})

// Error handler
app.use(errorHandler)

module.exports = app