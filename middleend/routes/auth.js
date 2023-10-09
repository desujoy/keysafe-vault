const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL } = require("../connection");

const router = express.Router();
router.use(express.json());
router.use(express.urlencoded({ extended: true }));
router.use(cors()); 

router.route("/register").post(async (req, res) => {
  const { username, password } = req.body;
  console.log(username);
  console.log(password);
  const response = await axios.post(`${BACKEND_URL}/api/users/add/`, {
    username: username,
  });
  const user = new User({userID: response.data.id, username: username, password: password});
  user.save();
  var options = {
    method: 'POST',
    url: `${BACKEND_URL}/api/genkeypass/`,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: {username: username, password: password}
  };
  const tokenResponse = await axios.request(options).catch(function (error) {
    console.error(error);
  });
  const token = tokenResponse.data.keypass;
  res.send(`User registered with token: ${token}`);
});

router.route("/login").post(async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username: username, password: password });
  if (user) {
    res.send(`User logged in!`);
  } else {
    res.status(404).send(`User not found!`);
  }
});

module.exports = router;