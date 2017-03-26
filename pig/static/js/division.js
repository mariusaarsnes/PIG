// Dynamic form for division configuration
//
// The `name`s of form elements are the keys to the form dictionary that is 
// received and processed in scripts/create_division.py.
// They must be unique, so for parameter `N`, the `name`s will be:
//
// ParameterN
// TypeN
// MinN
// MaxN
// OptionN_0
// OptionN_1
// ...
//
// Where Options for that particular parameter are enumerated with `variantId`
// -- also note that "variant" and "option" are used interchangeably; we should
// probably stick to one.


var paramId = 0;
var variantId = 0;
function newParamId() { return (++ paramId); }
function newVariantId() { return (++ variantId); }

document.getElementById("add_button").addEventListener("click", function() {
    var parameterForm = document.createElement("div");
    parameterForm.style.setProperty("padding-bottom", "10px", "");
    parameterForm.style.setProperty("display", "block");
    var param = "Parameter" + newParamId();

    var nameDiv = document.createElement("div");
    nameDiv.className = "mdl-textfield mdl-js-textfield has-placeholder is-upgraded";
    nameDiv.setAttribute("data-upgraded", ",MaterialTextfield");
    nameDiv.style = "display: flex; padding: 0; margin-bottom: 10px;"

    var nameLabel = document.createElement("label");
    nameLabel.className = "mdl-textfield__label";
    nameLabel.setAttribute("for", param);
//    nameLabel.innerHTML = "Parameter:";

    var nameField = document.createElement("input");
    nameField.setAttribute("type", "password");
    nameField.className = "mdl-textfield__input";
    nameField.name = param;
    nameField.placeholder = "Parameter name";
    nameField.style = "width: 80%;"

    nameDiv.appendChild(nameLabel);
    nameDiv.appendChild(nameField);
    document.getElementById("division-form").insertBefore(parameterForm, document.getElementById("add_button"));

    // Display a form to add a parameter to a division.
    console.log(document.getElementById("division-form").childElementCount);

    //var label = document.createElement("label");
    //label.innerHTML = "Parameter:";

    var deleteBtn = document.createElement("input");
    deleteBtn.type = "image";
    deleteBtn.src = "./static/img/cross.png";
    deleteBtn.style = "width: 20%; max-width: 28px; max-height: 28px;"
    //<input class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" type="button" value="Add parameter" id="add_button">

    nameDiv.appendChild(deleteBtn);

    parameterForm.appendChild(nameDiv);
    //parameterForm.appendChild(label);
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
    select.style.setProperty("display", "block");
    select.style.setProperty("width", "100%");
    select.style.setProperty("margin-bottom", "10px");
    var numOption = document.createElement("option");
    numOption.text = "Numeric";
    numOption.value = "Number";
    var enumOption = document.createElement("option");
    enumOption.text = "Enumeration";
    enumOption.value = "Enum";

    select.options.add(numOption);
    select.options.add(enumOption);


    select.addEventListener("change", function() {
        console.log(select.value); // TODO
    });
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
    textField.name = "Option" + paramId + "_" + newVariantId();

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
