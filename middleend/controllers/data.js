async function getdata(type) {
  const { username } = req.body;
  const user = await User.findOne({ username: username });
  if (user) {
    const data = await axios
      .get(`${BACKEND_URL}/api/${type}/user/${user.userID}`)
      .catch(function (error) {
        console.log(error);
        res.status(404).send(`Cards not found!`);
      });
    if (data.status === 200) {
      return data.data;
    } else {
      return null;
    }
  } else {
    return null;
  }
}

module.exports = { getdata };
