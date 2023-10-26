const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL } = require("../connection");
var cookieParser = require("cookie-parser");

const router = express.Router();
router.use(express.json());
router.use(express.urlencoded({ extended: true }));
router.use(cors());
router.use(cookieParser());

router.route("/register").post(async (req, res) => {
  const { username, email, password } = req.body;
  if (!username || !email || !password) {
    res.status(400).send("Username or password or email not provided!");
  } else {
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
      data: { username: email, password: password },
    };
    const tokenResponse = await axios.request(options).catch(function (error) {
      console.error(error);
    });
    const token = tokenResponse.data.keypass;
    res.send(`User registered with token: ${token}`).redirect("/login");
  }
});

router.route("/login").post(async (req, res) => {
  const { email, password } = req.body;
  console.log(email);
  console.log(password);
  if (!email || !password) {
    res.status(400).send("Username or password not provided!");
  } else {
    const user = await User.findOne({ email: email, password: password });
    if (user) {
      // Setting cookie with the user's email.
      res.cookie("user", user.email, { maxAge: 900000, httpOnly: true });

      // Sending response with the username.
      res.status(200).json({ username: user.username });
    } else {
      res.status(404).send(`User not found!`);
    }
  }
});

module.exports = router;
