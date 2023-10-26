function showEditor(i) {
  var editor = document.getElementById("editor-" + i);
  editor.style.display = "block";
  document.getElementById("edit-button-" + i).style.display = "none";
  document.getElementById("data-" + i).style.display = "none";
}

function hideEditor(i) {
  var editor = document.getElementById("editor-" + i);
  editor.style.display = "none";
  document.getElementById("edit-button-" + i).style.display = "block";
  document.getElementById("data-" + i).style.display = "block";
}

function showPass(i, id) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ method: "DECRYPT", id: id }),
  };

  fetch("/pass", options)
    .then((response) => response.json())
    .then((response) => {
      document.getElementById("pass-" + i).innerHTML =
        "Password: " + response.password;
      document.getElementById("show-button-" + i).style.display = "none";
      document.getElementById("hide-button-" + i).style.display = "block";
    })
    .catch((err) => {
      console.log(err);
    });
}

function showCard(i, id) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ method: "DECRYPT", id: id }),
  };

  fetch("/cards", options)
    .then((response) => response.json())
    .then((response) => {
      document.getElementById("card-num-" + i).innerHTML =
        "Card Number: " + response.card_number;
      document.getElementById("card-exp-" + i).innerHTML =
        "Card Number: " + response.card_exp;
      document.getElementById("card-cvv-" + i).innerHTML =
        "Card Number: " + response.card_cvv;
      document.getElementById("show-button-" + i).style.display = "none";
      document.getElementById("hide-button-" + i).style.display = "block";
    })
    .catch((err) => {
      console.log(err);
    });
}

function showNote(i, id) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ method: "DECRYPT", id: id }),
  };

  fetch("/notes", options)
    .then((response) => response.json())
    .then((response) => {
      document.getElementById("note-" + i).innerHTML =
        "Content: " + response.content;
      document.getElementById("show-button-" + i).style.display = "none";
      document.getElementById("hide-button-" + i).style.display = "block";
    })
    .catch((err) => {
      console.log(err);
    });
}

function hidePass(i) {
  location.reload();
}
