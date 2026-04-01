const app = require('./app')
require('dotenv').config()

const PORT = process.env.PORT || 8003

app.listen(PORT, () => {
  console.log(`Order Service corriendo en http://localhost:${PORT}`)
})