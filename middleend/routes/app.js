const express = require("express");
const axios = require("axios");
const User = require("../models/user");
const cors = require("cors");
const { BACKEND_URL, SECRET_KEY } = require("../connection");
var cookieParser = require("cookie-parser");
const jwt = require("jsonwebtoken");
var fileupload = require("express-fileupload");
var fs = require("fs");
const bcrypt = require("bcrypt");

const router = express.Router();
router.use(express.static("public"));
router.use(express.urlencoded({ extended: true }));
router.use(cors());
router.use(express.json());
router.use(cookieParser());
router.use(fileupload());

router.route("/").get(async (req, res) => {
  const { token } = req.cookies;
  if (!token) {
    res.redirect("/login");
  } else {
    var username = jwt.verify(token, SECRET_KEY).username;
    const validated = await User.findOne({ username: username });
    if (!validated) {
      res.redirect("/login");
    } else {
      res.render("index.ejs", { user: username });
    }
  }
});

router.route("/logout").get(async (req, res) => {
  res.clearCookie("token");
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
      const hashedPassword = await bcrypt.hash(password, 10);
      const options_ = {
        method: "POST",
        url: `${BACKEND_URL}/api/users/add/`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: { username: username, password: hashedPassword },
      };
      const response = await axios.request(options_).catch(function (error) {
        console.log(error);
        res.redirect("/login");
      });
      if (response) {
        const user = new User({
          userID: response.data.id,
          username: username,
          email: email,
          password: hashedPassword,
        });
        user.save();
        var options = {
          method: "POST",
          url: `${BACKEND_URL}/api/genkeypass/`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          data: { username: username, password: hashedPassword },
        };
        const tokenResponse = await axios
          .request(options)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });

        res.render("keypass.ejs", {
          token: tokenResponse.data.enc_blob,
          username: username,
        });
      }
    }
  });

router
  .route("/forgot")
  .get(async (req, res) => {
    res.render("forgot.ejs", { error: null, verified: false });
  })
  .post(async (req, res) => {
    if (req.body.method === "VERIFY") {
      if (!req.files) {
        res.render("forgot.ejs", {
          error: "Keypass file not found!",
          verified: false,
        });
      } else {
        const keypass = req.files.keypass;

        keypassContent = keypass.data.toString();

        const options = {
          method: "POST",
          url: `${BACKEND_URL}/api/verifykeypass/`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          data: {
            enc_blob: keypassContent.trim(),
          },
        };
        const response = await axios.request(options).catch(function (error) {
          console.log(error);
          res.render("forgot.ejs", {
            error: "Keypass file not found!",
            verified: false,
          });
        });
        if (response) {
          if (response.data.status == "success") {
            res.render("forgot.ejs", {
              error: null,
              verified: true,
              keypass: keypassContent.trim(),
              old_id: response.data.old_id,
            });
          } else {
            res.render("forgot.ejs", {
              error: "Keypass file not found!",
              verified: false,
            });
          }
        } else {
          res.render("forgot.ejs", {
            error: "Keypass file not found!",
            verified: false,
          });
        }
      }
    } else if (req.body.method === "RESTORE") {
      console.log("restore hit");
      console.log(req.body);
      const { old_id, password, keypass } = req.body;
      if (!old_id || !password || !keypass) {
        console.log("is this hot?");
        res.redirect("/forgot");
      } else {
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = await User.findOne({ userID: old_id });
        console.log(user.username);
        old_username = user.username;
        if (user) {
          const options = {
            method: "POST",
            url: `${BACKEND_URL}/api/restore/`,
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            data: {
              username: user.username,
              password: hashedPassword,
              enc_blob: keypass,
            },
          };
          const response = await axios.request(options).catch(function (error) {
            console.log(error);
            res.redirect("/forgot");
          });
          if (response) {
            if (response.data.status == "success") {
              user.password = hashedPassword;
              user.save();
              var options_ = {
                method: "POST",
                url: `${BACKEND_URL}/api/genkeypass/`,
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
                data: { username: old_username, password: hashedPassword },
              };
              const tokenResponse = await axios
                .request(options_)
                .catch(function (error) {
                  console.log(error);
                  res.redirect("/login");
                });

              res.render("keypass.ejs", {
                token: tokenResponse.data.enc_blob,
                username: old_username,
              });
            } else {
              res.redirect("/forgot");
            }
          } else {
            res.redirect("/forgot");
          }
        }
      }
    } else {
    }
  });

router
  .route("/login")
  .get(async (req, res) => {
    res.render("login.ejs", { error: null });
  })
  .post(async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
      res.render("login.ejs", { error: "Username or password not provided!" });
    } else {
      const user = await User.findOne({ email: email });
      if (user) {
        const match = await bcrypt.compare(password, user.password);
        if (match) {
          const token = jwt.sign({ username: user.username }, SECRET_KEY);
          res
            .cookie("token", token, { httpOnly: true })
            .status(200)
            .redirect("/");
        }
      } else {
        res.render("login.ejs", { error: "User not found!" });
      }
    }
  });

router
  .route("/pass")
  .get(async (req, res) => {
    const { token } = req.cookies;
    if (!token) {
      res.redirect("/login");
    } else {
      var username = jwt.verify(token, SECRET_KEY).username;
      const user = await User.findOne({ username: username });
      if (user) {
        const passwords = await axios
          .get(`${BACKEND_URL}/api/pass/user/${user.userID}`)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });
        if (passwords.status === 200) {
          //
          res.render("pass.ejs", {
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
    if (req.body.method === "PUT") {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { name, password, username, website, id } = req.body;
      const user = await User.findOne({ username: loggedInUser });

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
          data: null,
          error: "Passwords not found!",
        });
      });
      if (response) {
        res.redirect("/pass");
      }
    } else if (req.body.method === "DELETE") {
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
        res.redirect("/pass");
      });
      if (response) {
        res.redirect("/pass");
      }
    } else if (req.body.method === "DECRYPT") {
      const { id } = req.body;

      var options = {
        method: "GET",
        url: `${BACKEND_URL}/api/pass/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/pass");
      });
      if (response) {
        res.send(response.data);
      }
    } else {
      const token = req.cookies.token;
      const loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { name, password, username, website } = req.body;
      if (!name || !password || !username || !website) {
        res.render("pass.ejs", {
          data: null,
          error: "Invalid input!",
        });
      } else {
        const user = await User.findOne({ username: loggedInUser });

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
            data: null,
            error: "Passwords not found!",
          });
        });
        if (response) {
          res.redirect("/pass");
        }
      }
    }
  });

router
  .route("/cards")
  .get(async (req, res) => {
    const { token } = req.cookies;
    if (!token) {
      res.redirect("/login");
    } else {
      var username = jwt.verify(token, SECRET_KEY).username;
      const user = await User.findOne({ username: username });
      if (user) {
        const cards = await axios
          .get(`${BACKEND_URL}/api/cards/user/${user.userID}`)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });
        if (cards.status === 200) {
          res.render("cards.ejs", {
            data: cards.data,
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
    if (req.body.method === "PUT") {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { name, card_number, card_type, card_cvv, card_exp, id } = req.body;
      const user = await User.findOne({ username: loggedInUser });

      if (!user) {
        res.redirect("/login");
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
        res.render("cards.ejs", {
          data: null,
          error: "Cards not found!",
        });
      });
      if (response) {
        res.redirect("/cards");
      }
    } else if (req.body.method === "DELETE") {
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
        res.redirect("/cards");
      });
      if (response) {
        res.redirect("/cards");
      }
    } else if (req.body.method === "DECRYPT") {
      const { id } = req.body;

      var options = {
        method: "GET",
        url: `${BACKEND_URL}/api/cards/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/cards");
      });
      if (response) {
        res.send(response.data);
      }
    } else {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { name, card_number, card_type, card_cvv, card_exp } = req.body;
      const user = await User.findOne({ username: loggedInUser });

      if (!user) {
        res.redirect("/login");
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
        res.render("cards.ejs", {
          data: null,
          error: "Cards not found!",
        });
      });
      if (response) {
        res.redirect("/cards");
      }
    }
  });

router
  .route("/notes")
  .get(async (req, res) => {
    const { token } = req.cookies;
    if (!token) {
      res.redirect("/login");
    } else {
      var username = jwt.verify(token, SECRET_KEY).username;
      const user = await User.findOne({ username: username });
      if (user) {
        const notes = await axios
          .get(`${BACKEND_URL}/api/notes/user/${user.userID}`)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });
        if (notes.status === 200) {
          res.render("notes.ejs", {
            data: notes.data,
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
    if (req.body.method === "PUT") {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { notename, content, id } = req.body;
      const user = await User.findOne({ username: loggedInUser });

      if (!user) {
        res.redirect("/login");
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
        res.render("notes.ejs", {
          data: null,
          error: "Notes not found!",
        });
      });
      if (response) {
        res.redirect("/notes");
      }
    } else if (req.body.method === "DELETE") {
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
        res.redirect("/notes");
      });
      if (response) {
        res.redirect("/notes");
      }
    } else if (req.body.method === "DECRYPT") {
      const { id } = req.body;

      var options = {
        method: "GET",
        url: `${BACKEND_URL}/api/notes/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/notes");
      });
      if (response) {
        res.send(response.data);
      }
    } else {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { notename, content } = req.body;
      const user = await User.findOne({ username: loggedInUser });

      if (!user) {
        res.redirect("/login");
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
        res.render("notes.ejs", {
          data: null,
          error: "Notes not found!",
        });
      });
      if (response) {
        res.redirect("/notes");
      }
    }
  });

router
  .route("/files")
  .get(async (req, res) => {
    const { token } = req.cookies;
    if (!token) {
      res.redirect("/login");
    } else {
      var username = jwt.verify(token, SECRET_KEY).username;
      const user = await User.findOne({ username: username });
      if (user) {
        const files = await axios
          .get(`${BACKEND_URL}/api/files/user/${user.userID}`)
          .catch(function (error) {
            console.log(error);
            res.redirect("/login");
          });
        if (files.status === 200) {
          res.render("files.ejs", {
            data: files.data,
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
    if (req.body.method === "DELETE") {
      const { id } = req.body;
      var options = {
        method: "DELETE",
        url: `${BACKEND_URL}/api/files/delete/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/files");
      });
      if (response) {
        res.redirect("/files");
      }
    } else if (req.body.method === "DOWNLOAD") {
      const { id, filename } = req.body;
      var options = {
        method: "GET",
        url: `${BACKEND_URL}/api/files/download/${id}`,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const response = await axios.request(options).catch(function (error) {
        console.log(error);
        res.redirect("/files");
      });

      if (response) {
        // make user download the file from response.data with filename
        file_data = atob(response.data);
        fs.writeFileSync(filename, file_data.toString("binary"), "binary");
        res.download(filename, () => {
          fs.unlinkSync(filename);
        });
      } else {
        res.redirect("/files");
      }
    } else {
      const token = req.cookies.token;
      var loggedInUser = jwt.verify(token, SECRET_KEY).username;
      const { name } = req.body;
      if (!req.files) {
        res.render("files.ejs", {
          data: null,
          error: "Files not found!",
        });
      } else {
        const file = req.files.file;

        const user = await User.findOne({ username: loggedInUser });

        if (!user) {
          res.redirect("/login");
        }
        const owner_id = user.userID;
        const formData = new FormData();
        const contentType = "text/plain";
        var fileName = file.name.split(" ").join("_");
        // make filename shorter if too big while intact with extension
        if (fileName.length > 50) {
          const fileExtension = fileName.split(".").pop();
          fileName = fileName.substring(0, 50 - fileExtension.length - 1);
          fileName = `${fileName}.${fileExtension}`;
        }
        // make filedata base64 encoded
        const fileBuffer = Buffer.from(file.data).toString("base64");

        const fileBlob = new Blob([fileBuffer], { type: contentType });

        formData.append("name", name);
        formData.append("file", fileBlob, fileName);
        formData.append("owner_id", owner_id);

        var options = {
          method: "POST",
          url: `${BACKEND_URL}/api/files/add/`,
          headers: {
            "Content-Type": `multipart/form-data; boundary=${formData._boundary}`,
          },
          data: formData,
        };
        const response = await axios.request(options).catch(function (error) {
          console.log(error);
          res.render("files.ejs", {
            data: null,
            error: "Files not found!",
          });
        });
        if (response) {
          res.redirect("/files");
        }
      }
    }
  });

module.exports = router;
