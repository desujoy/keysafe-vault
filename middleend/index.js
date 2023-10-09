require('dotenv').config();
const express = require('express');
const axios = require('axios');
const mongoose = require('mongoose');
const auth = require('./routes/auth');
const { MONGO_URL, PORT, connectMongo } = require('./connection');

const app = express();
app.use(express.json());
connectMongo(MONGO_URL).then(() => {
    console.log('Connected to MongoDB');
  }).catch((err) => {
    console.log('Error connecting to MongoDB', err);
  });

app.use('/auth', auth);

app.listen(PORT, () => {
  console.log(`Server listening on port: ${PORT}`);
});