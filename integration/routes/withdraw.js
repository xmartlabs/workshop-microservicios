const express = require('express');
const withdrawCtrl = require('../controllers/withdraw');
const router = express.Router();
module.exports = router;

router.post('/',  withdrawCtrl.withdraw);
