jQuery('#login-form').validate({
    rules:{
        email: {
            required: true,
        },
        password: {
            required: true
            // minlength: 8, // This checks for minimum length
            
          }
    },
    message:{
        email:{
            required:"please enter your email"
        },
    }
})


jQuery('#signup-form').validate({
    rules:{
        email: {
            required: true,
            email: true
        },
        name: {
            required: true
        },
        password: {
            required: true,
            minlength: 8, // This checks for minimum length
          },
        cfpassword:{
            required: true,
            passwordMatch: true
        }
    },  
    message:{
        email:{
            required:"please enter your email"
        },
        confirmPassword: {
            required: "Please enter the same password as above.",
            passwordMatch: "Passwords do not match."
        }
    }
})