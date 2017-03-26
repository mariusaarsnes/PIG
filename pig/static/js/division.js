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

    /*var nameDiv = document.createElement("div");
    nameDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label is-upgraded";

    var nameLabel = document.createElement("label");
    nameLabel.className = "mdl-textfield__label";
    nameLabel.setAttribute("for", param);
    nameLabel.innerHTML = "Parameter name";

    var nameField = document.createElement("input");
    nameField.setAttribute("type", "text");
    nameField.className = "mdl-mdl-textfield__input";
    nameField.name = param;
    nameField.placeholder = "Parameter name";
    nameField.style = "width: 90%;"

    nameDiv.appendChild(nameField);
    nameDiv.appendChild(nameLabel);*/
    var cloneDiv = document.getElementById("division-name");
    var nameDiv = cloneDiv.cloneNode(true);
    for (var i = 0; i < nameDiv.childNodes.length; i++) {
        var element = nameDiv.childNodes[i];
        console.log(i + " " + element.id);
        if (element.id == "division-name-field") {
            element.name = "" + param;
        } else if (element.id == "division-name-label") {
            element.setAttribute("for", param);
            element.innerHTML = "Parameter name";
        }
    }
    nameDiv.classList.add("is-upgraded");

    nameDiv.addEventListener("focus", function() {
            nameDiv.classList.add("is-focused");
    }, true);
    nameDiv.addEventListener("focusout", function() {
            nameDiv.classList.remove("is-focused");
    }, true);

    document.getElementById("division-form").insertBefore(parameterForm, document.getElementById("add_button"));

    //var label = document.createElement("label");
    //label.innerHTML = "Parameter:";

    var deleteBtn = document.createElement("input");
    deleteBtn.type = "image";
    deleteBtn.src = "./static/img/cross.png";
    deleteBtn.style = "min-width: 10%; min-height: 10%; max-width: 10%; max-height: 10%;"
    //<input class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" type="button" value="Add parameter" id="add_button">

    //nameDiv.appendChild(deleteBtn);

    parameterForm.appendChild(nameDiv);
    parameterForm.appendChild(typeSelection());
    parameterForm.appendChild(numberForm());
    parameterForm.appendChild(enumForm());

    deleteBtn.addEventListener("click", function() {
        document.getElementById("division-form").removeChild(parameterForm);
    });
    componentHandler.upgradeElement(nameDiv);
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
        var enumContainer = document.getElementById("enum" + paramId);
        var numberContainer = document.getElementById("number" + paramId);
        if (select.value == "Enum") {
            enumContainer.style.removeProperty("display");
            numberContainer.style.setProperty("display", "none");
        } else {
            enumContainer.style.setProperty("display", "none");
            numberContainer.style.removeProperty("display");
        }
    });
    return select;
}

// If type of parameter is number - the form to be shown with number-specific configuration
function numberForm() {
    var min = document.createElement("input");
    min.style.setProperty("width", "46.5%");
    min.name = "Min" + paramId;
    min.id = "min";
    min.placeholder = "min";
    var max = document.createElement("input");
    max.style.setProperty("width", "46.5%");
    max.name = "Max" + paramId;
    max.id = "max";
    max.placeholder = "max";

    var descText = document.createElement("label");
    descText.innerHTML = "Enter the number range for this parameter:";
    descText.style.setProperty("display", "block");
    descText.style.setProperty("padding-bottom", "5px");

    // Container so that we may change visibility of both fields
    var container = document.createElement("span");
    container.appendChild(descText);
    container.id = "number" + paramId;
    container.style.setProperty("width", "100%");
    container.appendChild(min);
    container.innerHTML += " - ";
    container.appendChild(max);

    return container;
}

// TODO names?
function enumForm() {
    var addButton = document.createElement("button");
    addButton.id = "add_variant_button";
    addButton.type = "button";
    addButton.innerHTML = "+"

    var container = document.createElement("span");
    container.id = "enum" + paramId;
    container.appendChild(addButton);
    container.style.setProperty("display", "none");
    addVariantFormTo(container, true);
    addButton.addEventListener("click", function() {
        // Add another variant form
        addVariantFormTo(container, false);
    });

    return container;
}

function addVariantFormTo(container, first) {
    var variantForm = document.createElement("div");

    var textField = document.createElement("input");
    textField.placeholder = "Option name";
    textField.name = "Option" + paramId + "_" + newVariantId();

    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.innerHTML = "-";

    variantForm.appendChild(textField);
    if (!first)
        variantForm.appendChild(deleteButton);


    var addButton = container.querySelector("#add_variant_button");
    container.insertBefore(variantForm, addButton);

    deleteButton.addEventListener("click", function() {
        container.removeChild(variantForm);
    });
}
