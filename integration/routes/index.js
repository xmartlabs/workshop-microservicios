const express = require('express');
const withdrawRoutes = require('./withdraw');
const router = express.Router();

router.use('/withdraw', withdrawRoutes);

module.exports = router;
