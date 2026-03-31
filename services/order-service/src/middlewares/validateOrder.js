const validateOrder = (req, res, next) => {
  const { kiosk_id, items } = req.body

  if (!kiosk_id) {
    return res.status(400).json({ message: 'kiosk_id es requerido.' })
  }

  if (!items || !Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ message: 'El pedido debe tener al menos un ítem.' })
  }

  for (const item of items) {
    if (!item.product_id || !item.name || !item.quantity || !item.unit_price) {
      return res.status(400).json({
        message: 'Cada ítem requiere: product_id, name, quantity, unit_price.',
      })
    }
    if (item.quantity <= 0) {
      return res.status(400).json({ message: 'La cantidad debe ser mayor a 0.' })
    }
  }

  next()
}

module.exports = validateOrder