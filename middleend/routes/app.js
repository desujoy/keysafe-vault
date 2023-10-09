const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL } = require("../connection");
var cookieParser = require("cookie-parser");
var jwt = require("jsonwebtoken");

const router = express.Router();
router.use(express.urlencoded({ extended: true }));
router.use(cors());
router.use(express.static("public"));
router.use(cookieParser());

router.get("/", (req, res) => {
  res.render("index.ejs");
});


router.get("/login", (req, res) => {
  res.render("login.ejs");
});

router.get("/register", (req, res) => {
  res.render("register.ejs");
});

module.exports = router;
