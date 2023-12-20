function validateForm() {
    var inputValue = document.getElementById("busqueda").value;
    if (inputValue.trim().length === 0) {
        alert("Por favor, ingresa al menos un carácter.");
        return false;
    }
    return true;
}