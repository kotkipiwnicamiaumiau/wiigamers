function getSelectedText(elementId) {
    var elt = document.getElementById(elementId);

    if (elt.selectedIndex == -1)
        return null;

    return elt.options[elt.selectedIndex].text;
}

function displayMenu(){
    var sp = getSelectedText("sport");
    if(sp == "Pływanie" || sp == "Bieganie" || sp == "Kolarstwo"){
        document.getElementById("distsports").style = "display: block;";
        document.getElementById("gymsports").style = "display: none;";
    }
    if(sp == "Siłownia"){
        document.getElementById("gymsports").style = "display: block;";
        document.getElementById("distsports").style = "display: none;";
    }
}