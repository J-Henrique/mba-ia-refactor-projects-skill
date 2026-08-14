const bcrypt = require('bcryptjs');
const config = require('../config/config');

function hashPassword(password) {
    return bcrypt.hashSync(password, config.bcryptSaltRounds);
}

function comparePassword(password, hash) {
    return bcrypt.compareSync(password, hash);
}

module.exports = { hashPassword, comparePassword };