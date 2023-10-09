const express = require('express');
const axios = require('axios');
const User = require('./models/user');

const app = express();
app.use(express.json());

app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const response = await axios.post(`${BACKEND_URL}/register`, { username, password });
    const user = new User({ username, password });
    await user.save();

    res.send('User created');
});

