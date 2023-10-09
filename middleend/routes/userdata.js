const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const { BACKEND_URL } = require("../connection");

const router = express.Router();
router.use(express.urlencoded({ extended: true }));

router.route('/pass')
.get(async (req, res) => {
    const { username } = req.body;
    const user = await User.findOne({ username: username });
    if (user) {
        const passwords=await axios.get(`${BACKEND_URL}/api/pass/user/${user.userID}`).catch(function (error) {
            console.error(error);
        });
        res.send(passwords.data);
    } else {
        res.status(404).send(`User not found!`);
    }
}).post(async (req, res) => {
    const { loggedInUser, name, password, username, website } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    const owner_id = user.userID;
    var options = {
        method: 'POST',
        url: `${BACKEND_URL}/api/pass/add/`,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: {
          name: name,
          password: password,
          username: username,
          website: website,
          owner_id: owner_id
        }
      };
    const response = await axios.request(options).catch(function (error) {
        console.error(error);
    });
    res.send(response.data);

});

module.exports = router;
