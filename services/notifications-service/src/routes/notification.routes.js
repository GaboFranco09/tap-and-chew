const router       = require('express').Router();
const internalAuth = require('../middlewares/internalAuth');
const ctrl         = require('../controllers/notification.controller');

router.use(internalAuth);

router.get ('/order/:order_id', ctrl.getByOrder);
router.post('/',                ctrl.create);
router.patch('/:id/read',       ctrl.markAsRead);

module.exports = router;