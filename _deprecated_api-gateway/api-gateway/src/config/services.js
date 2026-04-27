require('dotenv').config();

const services = {
    auth:    process.env.AUTH_SERVICE_URL,
    menu:    process.env.MENU_SERVICE_URL,
    orders:  process.env.ORDER_SERVICE_URL,
    kitchen: process.env.KITCHEN_SERVICE_URL,
    payment: process.env.PAYMENT_SERVICE_URL,
};

module.exports = services;