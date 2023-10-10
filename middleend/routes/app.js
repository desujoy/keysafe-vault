const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL } = require("../connection");
var cookieParser = require("cookie-parser");

const router = express.Router();
router.use(express.static("public"));
router.use(express.urlencoded({ extended: true }));
router.use(cors());
router.use(express.json());
router.use(cookieParser());

router.route("/").get(async (req, res) => {
  const { username } = req.cookies;
  const validated = await User.findOne({ username: username });
  // console.log(validated);
  if (!validated) {
    res.redirect("/login");
  } else {
    res.render("index.ejs", { user: username });
  }
});

router.route("/logout").get(async (req, res) => {
  res.clearCookie("user");
  res.redirect("/login");
});

router
  .route("/register")
  .get(async (req, res) => {
    res.render("register.ejs", { error: null });
  })
  .post(async (req, res) => {
    const { username, email, password } = req.body;
    if (!username || !email || !password) {
      res.render("register.ejs", {
        error: "Username or password or email not provided!",
      });
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
      const tokenResponse = await axios
        .request(options)
        .catch(function (error) {
          console.error(error);
        });
      const token = tokenResponse.data.keypass;
      res.render("keypass.ejs", { token: token });
    }
  });

router
  .route("/login")
  .get(async (req, res) => {
    res.render("login.ejs", { error: null });
  })
  .post(async (req, res) => {
    const { email, password } = req.body;
    console.log(email);
    console.log(password);
    if (!email || !password) {
      res.render("login.ejs", { error: "Username or password not provided!" });
    } else {
      const user = await User.findOne({ email: email, password: password });
      if (user) {
        res
          .cookie("username", user.username, { httpOnly: true })
          .status(200)
          .redirect("/");
      } else {
        res.render("login.ejs", { error: "User not found!" });
      }
    }
  });

router
  .route("/pass")
  .get(async (req, res) => {
    const { username } = req.cookies;
    if (!username) {
      res.redirect("/login");
    } else {
      const user = await User.findOne({ username: username });
      if (user) {
        const passwords = await axios
          .get(`${BACKEND_URL}/api/pass/user/${user.userID}`)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });
        if (passwords.status === 200) {
          // console.log(passwords.data);
          res.render("pass.ejs", {
            type: "Password",
            data: passwords.data,
            error: null,
          });
        } else {
          res.redirect("/login");
        }
      } else {
        res.redirect("/login");
      }
    }
  })
  .post(async (req, res) => {
    console.log(req.body.method);
    if (req.body.method === "PUT") {
      console.log("put hit");
      const loggedInUser = req.cookies.username;
      const { name, password, username, website, id } = req.body;
      const user = await User.findOne({ username: loggedInUser });
      console.log(user);
      if (!user) {
        res.redirect("/login");
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
        res.render("pass.ejs", {
          type: "Password",
          data: null,
          error: "Passwords not found!",
        });
      });
      if (response) {
        res.redirect("/pass");
      }
    } else if (req.body.method === "DELETE") {
      console.log("delete hit");
      const { id } = req.body;
      console.log(id);
      var options = {
        method: "DELETE",
        url: `${BACKEND_URL}/api/pass/delete/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/pass");
      });
      if (response) {
        res.redirect("/pass");
      }
    } else {
      const loggedInUser = req.cookies.username;
      const { name, password, username, website } = req.body;
      const user = await User.findOne({ username: loggedInUser });
      console.log(user);
      if (!user) {
        res.redirect("/login");
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
        res.render("pass.ejs", {
          type: "Password",
          data: null,
          error: "Passwords not found!",
        });
      });
      if (response) {
        res.redirect("/pass");
      }
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
