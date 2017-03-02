var paramId = 0;
function newId() { return (++ paramId); }

document.getElementById("add_button").addEventListener("click", function() {
    var parameterForm = document.createElement("div");
    parameterForm.style.borderStyle = "solid";
    document.getElementById("division-form").insertBefore(parameterForm, document.getElementById("add_button"));

    // Display a form to add a parameter to a division.
    console.log(document.getElementById("division-form").childElementCount);

    var label = document.createElement("label");
    label.innerHTML = "Parameter:";

    var nameField = document.createElement("input");
    nameField.type = "text";
    nameField.name = "Parameter" + newId();
    nameField.id = "parameter";
    nameField.placeholder = "Parameter name";


    var deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.innerHTML = "-";

    parameterForm.appendChild(label);
    parameterForm.appendChild(nameField);
    parameterForm.appendChild(deleteBtn);
    parameterForm.appendChild(document.createElement("br"));
    parameterForm.appendChild(typeSelection());
    parameterForm.appendChild(numberForm());
    parameterForm.appendChild(document.createElement("br"));
    parameterForm.appendChild(enumForm());

    deleteBtn.addEventListener("click", function() {
        document.getElementById("division-form").removeChild(parameterForm);
    });
});

function typeSelection() {
    var select = document.createElement("select");
    select.id = "type";
    select.name = "Type" + paramId;

    var numOption = document.createElement("option");
    numOption.text = "Numberic";
    numOption.value = "Number";
    var enumOption = document.createElement("option");
    enumOption.text = "Enumeration";
    enumOption.value = "Enum";

    select.options.add(numOption);
    select.options.add(enumOption);
    return select;
}

// If type of parameter is number - the form to be shown with number-specific configuration
function numberForm() {
    var min = document.createElement("input");
    min.name = "Min" + paramId;
    min.id = "min";
    min.placeholder = "min";
    var max = document.createElement("input");
    max.name = "Max" + paramId;
    max.id = "max";
    max.placeholder = "max";

    // Container so that we may change visibility of both fields
    var container = document.createElement("span");
    container.appendChild(min);
    container.innerHTML += " - ";
    container.appendChild(max);
    container.style.visibility = "visible";

    return container;
}

// TODO names?
function enumForm() {
    var addButton = document.createElement("button");
    addButton.id = "add_variant_button";
    addButton.type = "button";
    addButton.innerHTML = "+"

    var container = document.createElement("span");
    container.appendChild(addButton);

    addButton.addEventListener("click", function() {
        // Add another variant form
        addVariantFormTo(container);
    });

    return container;
}

function addVariantFormTo(container) {
    var variantForm = document.createElement("div");

    var textField = document.createElement("input");
    textField.placeholder = "Option name";
    textField.name = "Option" + paramId;

    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.innerHTML = "-";

    variantForm.appendChild(textField);
    variantForm.appendChild(deleteButton);


    var addButton = container.querySelector("#add_variant_button");
    container.insertBefore(variantForm, addButton);

    deleteButton.addEventListener("click", function() {
        container.removeChild(variantForm);
    });
}


// TODO legg inn div med fixed width før enum selection? Eller samme width som typeSelection?
