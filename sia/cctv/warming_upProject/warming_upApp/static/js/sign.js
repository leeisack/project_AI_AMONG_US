function id_check(){
    var id = document.getElementById("id").value;
    console.log(id);
    $.ajax({
        url:  "/idcheck/",
        type: 'post',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({"id" : id}),
        success:function(response){
            if(response['error']){
                $("#id_msg").show();
                document.getElementById("id").value = "";
                document.getElementById("id").focus();
            }
            else{
                $("#id_msg").hide(); 
            }
        },
        error : function(xhr, error){
            console.log(error)
        }
    });
}

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