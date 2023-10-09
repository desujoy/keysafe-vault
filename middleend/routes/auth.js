const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const { BACKEND_URL } = require("../connection");
const cors = require("cors");

const app = express();

app.use(cors());

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post("/register", async (req, res) => {
  const { username, email, password } = req.body;
  console.log(username);
  console.log(password);
  console.log(email);
  const response = await axios.post(`${BACKEND_URL}/api/users/add/`, {
    username: username,
  });
  const user = new User({
    userID: response.data.id,
    username: username,
    email: email,
    password: password,
  });
  user.save();
  var options = {
    method: "POST",
    url: `${BACKEND_URL}/api/genkeypass/`,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    data: { username: username, password: password },
  };
  const tokenResponse = await axios
    .request(options)
    .catch(function (error) {
      console.error(error);
    });
  const token = tokenResponse.data.keypass;
  res.send(`User registered with token: ${token}`);
});

app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  console.log(email);
  console.log(password);
  const user = await User.findOne({ email: email, password: password });
  if (user) {
    res.send(`User logged in!`);
    console.log(200);
  } else {
    res.status(404).send(`User not found!`);
    console.log(404);
  }
});

module.exports = app;
