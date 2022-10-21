const express = require('express');
const withdrawCtrl = require('../controllers/withdraw');
const router = express.Router();
module.exports = router;

router.get('/',  withdrawCtrl.withdraw);
