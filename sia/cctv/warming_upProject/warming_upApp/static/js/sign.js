function password_check() {
    var password = document.getElementById("pwd").value;
    var password_check = document.getElementById("pwd_chk").value;
    
    if(password != password_check) {
        $("#pwd_msg").show();
        document.getElementById("pwd_chk").value = "";
        document.getElementById("pwd_chk").focus();
    }
    else{
        $("#pwd_msg").hide();
    }
}