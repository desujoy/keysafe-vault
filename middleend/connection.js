const mongoose = require('mongoose');

const PORT = process.env.PORT || 3000;
const BACKEND_HOST = process.env.BACKEND_HOST || 'http://localhost';
const BACKEND_PORT = process.env.BACKEND_PORT || 8000;
const BACKEND_URL = `${BACKEND_HOST}:${BACKEND_PORT}`;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/';
const MONGO_DB = process.env.MONGO_DB || 'users';
const MONGO_URL = `${MONGO_URI}${MONGO_DB}`;
const SECRET_KEY = process.env.SECRET_KEY || "gAAAAABlNXDvO0r2G4xJJ0LHgfAZKF1wUuOsczySlv0Wt2iitfMvF03Hm0lEEZv4QSvlJzCPo7xIsPjU7b_PJrYxGgqUEVDHSv6E7flaBVnx9nv3HFzKvPE="

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
    SECRET_KEY,
    connectMongo,
};