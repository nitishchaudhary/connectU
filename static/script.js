//validating sign up form 

const validate_form=()=>{
    if($("#password").val().length < 8){
        let message = "Password must be 8 characters long"
        $('.password-error-messages').html(message);
        return false;
    }
    if($("#password").val() != $("#password_again").val()){
        let message = "Passwords do not match"
        $('.password-error-messages').html(message);
        return false;
    }
    
}
