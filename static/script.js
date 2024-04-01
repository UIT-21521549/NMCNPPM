function checkAccountExistence() {
    // Retrieve the value of the account input field
    var account = document.getElementById("account_2").value;
    
    // Example condition: if the account already exists, print a message
    if (account === "existing_account") {
        console.log("Account already exists!");
    }
}