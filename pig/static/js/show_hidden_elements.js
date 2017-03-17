function showHiddenElement(id) {
    var table = document.getElementById("group" + id);
    var caret = document.getElementById("table-caret" + id);
    if (table.style.display == "") {
        table.style.display = "none"
        caret.className = "fa fa-caret-down right-float font-size-twenty";
    } else {
        table.style.display = "";
        caret.className = "fa fa-caret-up right-float font-size-twenty";
    }
}