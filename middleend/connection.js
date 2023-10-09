const mongoose = require('mongoose');

const PORT = process.env.PORT || 3000;
const BACKEND_HOST = process.env.BACKEND_HOST || 'http://backend-api';
const BACKEND_PORT = process.env.BACKEND_PORT || 8000;
const BACKEND_URL = `${BACKEND_HOST}:${BACKEND_PORT}`;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/';
const MONGO_DB = process.env.MONGO_DB || 'users';
const MONGO_URL = `${MONGO_URI}${MONGO_DB}`;

async function connectMongo(url) {
    return mongoose.connect(url);
  }
  
module.exports = {
    PORT,
    BACKEND_HOST,
    BACKEND_PORT,
    BACKEND_URL,
    MONGO_URI,
    MONGO_DB,
    MONGO_URL,
    connectMongo,
};