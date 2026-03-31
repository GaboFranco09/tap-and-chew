const express      = require('express')
const router       = express.Router()
const controller   = require('../controllers/orderController')
const validateOrder = require('../middlewares/validateOrder')

router.get('/status/pending',  controller.getPendingOrders)
router.get('/',                controller.getAllOrders)
router.get('/:id',             controller.getOrderById)
router.post('/',   validateOrder, controller.createOrder)
router.patch('/:id/status',    controller.updateOrderStatus)
router.delete('/:id',          controller.cancelOrder)

module.exports = router