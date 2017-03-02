var paraId = 0;

document.getElementById("add_button").addEventListener("click", function() {
   
    console.log(document.getElementById("division-form").childElementCount);
    var label = document.createElement("label");
    label.innerHTML = "Parameter: ";
    var textField = document.createElement("input");
    textField.setAttribute("type", "text");
    textField.setAttribute("name", "Parameter" + paraId);
    textField.setAttribute("id", "parameter");
    paraId += 1;
    textField.setAttribute("placeholder", "Parameternavn");
    var cross = document.createElement("img");
   
    cross.setAttribute("id", "remove_button");
    document.getElementById("division-form").insertBefore(label, document.getElementById("add_button"));
    document.getElementById("division-form").insertBefore(textField, document.getElementById("add_button"));
    document.getElementById("division-form").insertBefore(cross, document.getElementById("add_button"));
    cross.addEventListener("click", function() {
       
        document.getElementById("division-form").removeChild(textField);
        document.getElementById("division-form").removeChild(label);
        document.getElementById("division-form").removeChild(cross);
        
        
    });
});