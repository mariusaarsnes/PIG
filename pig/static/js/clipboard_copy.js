

function copyToClipboard(link) {

    var aux = document.createElement("input");
    aux.setAttribute("value", location.origin + "/" + link);
    document.body.appendChild(aux);
    aux.select();

    document.execCommand("copy");
    document.body.removeChild(aux);

}