
function validateForm() {
    let phone = document.getElementById("phone").value;

    if (phone === "") {
        alert("Phone number is required!");
        return false;
    }

    if (phone.length < 10) {
        alert("Enter valid phone number!");
        return false;
    }

    return true;
}