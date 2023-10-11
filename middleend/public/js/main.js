function showEditor(i) {
    var editor = document.getElementById("editor-"+i);
    editor.style.display = "block";
    document.getElementById("edit-button-"+i).style.display = "none";
    document.getElementById("data-"+i).style.display = "none";
}

function hideEditor(i) {
    var editor = document.getElementById("editor-"+i);
    editor.style.display = "none";
    document.getElementById("edit-button-"+i).style.display = "block";
    document.getElementById("data-"+i).style.display = "block";
}