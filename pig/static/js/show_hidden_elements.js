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

function addData(id, size) {
    var parent = document.getElementById("group" + id);
    var last = document.getElementById("button" + id);
    if (parent.children.length <= size) {
        console.log("Added element.");
        var newRow = document.createElement("tr");
        var newData = document.createElement("td");
        newData.id = "table-data" + id;
        newData.className = "mdl-data-table__cell--non-numeric full-width";
        parent.insertBefore(newRow, last);
        newRow.appendChild(newData);
        newData.appendChild(document.createTextNode("TODO"));
        if (parent.children.length > size) {
            console.log("Removed button.");
            var button = document.getElementById("button" + id);
            parent.removeChild(button);
        }
    }
}