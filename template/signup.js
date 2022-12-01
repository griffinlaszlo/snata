function checkUser(){
    // checks to see if username is already in the database
    let user = document.getElementById("username").value;
    if (user == null){
        document.getElementById("user-result").innerText = "Invalid or unavailable Username"
    }
    else{
        document.getElementById("user-result").innerText = "Valid Username"
    }
}

function checkPass(){
    // checks to see if username is already in the database
    let password = document.getElementById("password").value;
    let confirm = document.getElementById("confirm").value;
    if (password == null){
        document.getElementById("user-result").innerText = "Invalid or unavailable password"
    }
    else if (password != confirm){
        document.getElementById("user-result-parent").innerText = "Passwords do not match"
    }
}
