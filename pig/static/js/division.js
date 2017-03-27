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
    parameterForm.style.setProperty("width", "100%");
    parameterForm.style.setProperty("border-top", "1px solid #555555");
    parameterForm.style.setProperty("padding-bottom", "10px", "");
    parameterForm.style.setProperty("display", "block");
    parameterForm.style.setProperty("padding-left", "10px");
    var param = "Parameter" + newParamId();
    var cloneDiv = document.getElementById("division-name");
    var nameDiv = cloneDiv.cloneNode(true);
    nameDiv.style.setProperty("width", "90%");
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
    enhanceField(nameDiv);
    document.getElementById("division-form").insertBefore(parameterForm, document.getElementById("add_button"));

    //var label = document.createElement("label");
    //label.innerHTML = "Parameter:";

    var deleteBtn = document.createElement("input");
    deleteBtn.type = "image";
    deleteBtn.src = "./static/img/cross.png";
    deleteBtn.style = "min-width: 20px; min-height: 20px; max-width: 20px; max-height: 20px;"
    //<input class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored" type="button" value="Add parameter" id="add_button">

    parameterForm.appendChild(nameDiv);
    parameterForm.appendChild(deleteBtn);
    parameterForm.appendChild(typeSelection());
    parameterForm.appendChild(numberForm());
    parameterForm.appendChild(enumForm());

    deleteBtn.addEventListener("click", function() {
        document.getElementById("division-form").removeChild(parameterForm);
    });
    componentHandler.upgradeElement(nameDiv);
});

function createTextField(fieldName, placeholderText) {
    var div = document.createElement("div");
    div.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
    var field = document.createElement("input");
    field.className = "mdl-textfield__input";
    field.setAttribute("type", "text");
    field.setAttribute("name", fieldName);
    var label = document.createElement("label");
    label.className = "mdl-textfield__label";
    label.setAttribute("type", "text");
    label.innerHTML = placeholderText;
    div.appendChild(label);
    div.appendChild(field);
    enhanceField(div);
    return div;
}

function enhanceField(field) {
    field.classList.add("is-upgraded");
    var textField = field.childNodes[1];
    field.addEventListener("focus", function() {
            field.classList.add("is-focused");
            if (textField.value == "")
                field.classList.remove("is-dirty");
            else
                field.classList.add("is-dirty");
    }, true);

    field.addEventListener("focusout", function() {
            field.classList.remove("is-focused");
            if (textField.value == "")
                field.classList.remove("is-dirty");
            else
                field.classList.add("is-dirty");
    }, true);
}

function typeSelection() {
    var selectDiv = document.createElement("div");
    selectDiv.className = "mdl-selectfield mdl-js-selectfield mdl-selectfield--floating-label";
    selectDiv.style.setProperty("padding", "0");
    var select = document.createElement("select");
    select.id = "type";
    select.name = "Type" + paramId;
    select.className = "mdl-selectfield__select";
    select.style.setProperty("display", "block");
    select.style.setProperty("width", "100%");

    var label = document.createElement("label");
    label.innerHTML = "Type";
    label.className = "mdl-selectfield__label";

    var numOption = document.createElement("option");
    numOption.text = "Numeric";
    numOption.value = "Number";
    var enumOption = document.createElement("option");
    enumOption.text = "Enumeration";
    enumOption.value = "Enum";
    selectDiv.appendChild(select);
    selectDiv.appendChild(label);
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
    componentHandler.upgradeElement(selectDiv);
    return selectDiv;
}

// If type of parameter is number - the form to be shown with number-specific configuration
function numberForm() {
    var minDiv = createTextField("Min" + paramId, "Min");
    minDiv.style.setProperty("width", "46.5%");
    var maxDiv = createTextField("Max" + paramId, "Max");
    maxDiv.style.setProperty("width", "46.5%");

    var descText = document.createElement("label");
    descText.innerHTML = "Enter the number range for this parameter:";
    descText.style.setProperty("display", "block");
    descText.style.setProperty("padding-top", "15px");
    descText.style.setProperty("padding-bottom", "5px");

    // Container so that we may change visibility of both fields
    var container = document.createElement("span");
    container.appendChild(descText);
    container.id = "number" + paramId;
    container.style.setProperty("width", "100%");
    container.appendChild(minDiv);
    container.appendChild(document.createTextNode("  -  "));
    container.appendChild(maxDiv);
    return container;
}

// TODO names?
function enumForm() {
    var addButton = document.createElement("button");
    addButton.id = "add_variant_button";
    addButton.type = "button";
    addButton.innerHTML = "+"

    var descText = document.createElement("label");
    descText.innerHTML = "Enter the number range for this parameter:";
    descText.style.setProperty("display", "block");
    descText.style.setProperty("padding-bottom", "5px");

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

    var textField = createTextField("Option" + paramId + "_" + newVariantId(), "Option");
    textField.style.setProperty("width", "40%");
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
