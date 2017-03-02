var paraId = 0;

document.getElementById("add_button").addEventListener("click", function() {
    var parameterForm = document.createElement("div");
    document.getElementById("division-form").insertBefore(parameterForm, document.getElementById("add_button"));

    // Display a form to add a parameter to a division.
    console.log(document.getElementById("division-form").childElementCount);

    var label = document.createElement("label");
    label.innerHTML = "Legg til parameter:";

    var nameField = document.createElement("input");
    nameField.setAttribute("type", "text");
    nameField.setAttribute("name", "Parameter" + paraId);
    nameField.setAttribute("id", "parameter");
    paraId += 1;
    nameField.setAttribute("placeholder", "Parameternavn");


    var cross = document.createElement("img");
    cross.setAttribute("src", "/static/img/cross.png");
    cross.setAttribute("id", "remove_button");

    parameterForm.appendChild(document.createElement("br"));
    parameterForm.appendChild(label);
    parameterForm.appendChild(document.createElement("br"));
    parameterForm.appendChild(nameField);
    parameterForm.appendChild(typeSelection());
    parameterForm.appendChild(numberForm());
    parameterForm.appendChild(cross);

    cross.addEventListener("click", function() {
        document.getElementById("division-form").removeChild(parameterForm);
    });
});

function typeSelection() {
    var select = document.createElement("select");
    var numOption = document.createElement("option");
    numOption.text = "Number";
    select.options.add(numOption);
    return select;
}

// If type of parameter is number - the form to be shown with number-specific configuration
function numberForm() {
    var min = document.createElement("input");
    min.setAttribute("placeholder", "min");
    var max = document.createElement("input");
    max.setAttribute("placeholder", "max");

    // Container so that we may change visibility of both fields
    var container = document.createElement("span");
    container.appendChild(min);
    container.appendChild(max);
    container.style.visibility = "visible";

    return container;
}

function enumForm() {
    
}
