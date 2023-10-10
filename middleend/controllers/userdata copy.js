const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL } = require("../connection");

const router = express.Router();
router.use(express.urlencoded({ extended: true }));
router.use(cors());
router.use(express.json());
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
      res
        .cookie("user", user.email, { maxAge: 900000, httpOnly: true })
        .status(200)
        .redirect("/");
    } else {
      res.status(404).send(`User not found!`);
    }
  }
});

router
  .route("/pass")
  .get(async (req, res) => {
    const { username } = req.body;
    const user = await User.findOne({ username: username });
    if (user) {
      const passwords = await axios
        .get(`${BACKEND_URL}/api/pass/user/${user.userID}`)
        .catch(function (error) {
          console.log(error);
          res.status(404).send(`Passwords not found!`);
        });
      if (passwords.status === 200) {
        res.send(passwords.data);
      } else {
        res.status(404).send(`Passwords not found!`);
      }
    } else {
      res.status(404).send(`User not found!`);
    }
  })
  .post(async (req, res) => {
    const { loggedInUser, name, password, username, website } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "POST",
      url: `${BACKEND_URL}/api/pass/add/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        name: name,
        password: password,
        username: username,
        website: website,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Passwords not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .put(async (req, res) => {
    const { loggedInUser, name, password, username, website, id } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "PUT",
      url: `${BACKEND_URL}/api/pass/update/${id}/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        name: name,
        password: password,
        username: username,
        website: website,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Passwords not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .delete(async (req, res) => {
    const { id } = req.body;
    var options = {
      method: "DELETE",
      url: `${BACKEND_URL}/api/pass/delete/${id}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Passwords not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  });

router
  .route("/cards")
  .get(async (req, res) => {
    const { username } = req.body;
    const user = await User.findOne({ username: username });
    if (user) {
      const cards = await axios
        .get(`${BACKEND_URL}/api/cards/user/${user.userID}`)
        .catch(function (error) {
          console.log(error);
          res.status(404).send(`Cards not found!`);
        });
      if (cards.status === 200) {
        res.send(cards.data);
      } else {
        res.status(404).send(`Cards not found!`);
      }
    } else {
      res.status(404).send(`User not found!`);
    }
  })
  .post(async (req, res) => {
    const { loggedInUser, name, card_number, card_type, card_cvv, card_exp } =
      req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "POST",
      url: `${BACKEND_URL}/api/cards/add/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        name: name,
        card_number: card_number,
        card_type: card_type,
        card_cvv: card_cvv,
        card_exp: card_exp,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Cards not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .put(async (req, res) => {
    const {
      loggedInUser,
      name,
      card_number,
      card_type,
      card_cvv,
      card_exp,
      id,
    } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "PUT",
      url: `${BACKEND_URL}/api/cards/update/${id}/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        name: name,
        card_number: card_number,
        card_type: card_type,
        card_cvv: card_cvv,
        card_exp: card_exp,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Cards not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .delete(async (req, res) => {
    const { id } = req.body;
    var options = {
      method: "DELETE",
      url: `${BACKEND_URL}/api/cards/delete/${id}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Cards not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  });

router
  .route("/notes")
  .get(async (req, res) => {
    const { username } = req.body;
    const user = await User.findOne({ username: username });
    if (user) {
      const cards = await axios
        .get(`${BACKEND_URL}/api/notes/user/${user.userID}`)
        .catch(function (error) {
          console.log(error);
          res.status(404).send(`Notes not found!`);
        });
      if (cards.status === 200) {
        res.send(cards.data);
      } else {
        res.status(404).send(`Notes not found!`);
      }
    } else {
      res.status(404).send(`User not found!`);
    }
  })
  .post(async (req, res) => {
    const { loggedInUser, notename, content } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "POST",
      url: `${BACKEND_URL}/api/notes/add/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        notename: notename,
        content: content,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Notes not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .put(async (req, res) => {
    const { loggedInUser, notename, content, id } = req.body;
    const user = await User.findOne({ username: loggedInUser });
    console.log(user);
    if (!user) {
      res.status(404).send(`User not found!`);
    }
    const owner_id = user.userID;
    var options = {
      method: "PUT",
      url: `${BACKEND_URL}/api/notes/update/${id}/`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: {
        notename: notename,
        content: content,
        owner_id: owner_id,
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Notes not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  })
  .delete(async (req, res) => {
    const { id } = req.body;
    var options = {
      method: "DELETE",
      url: `${BACKEND_URL}/api/notes/delete/${id}`,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };
    const response = await axios.request(options).catch(function (error) {
      console.log(error);
      res.status(404).send(`Notes not found!`);
    });
    if (response) {
      res.send(response.data);
    }
  });

module.exports = router;
