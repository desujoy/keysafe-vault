require('dotenv').config();
const express = require('express');
const auth = require('./routes/auth');
const userdata = require('./routes/userdata');
const cors = require('cors');
const { MONGO_URL, PORT, connectMongo } = require('./connection');

const app = express();
app.use(express.json());
app.use(cors());
connectMongo(MONGO_URL).then(() => {
    console.log('Connected to MongoDB');
  }).catch((err) => {
    console.log('Error connecting to MongoDB', err);
  });

app.use('/auth', auth);
app.use('/data', userdata);

app.listen(PORT, () => {
  console.log(`Server listening on port: ${PORT}`);
});