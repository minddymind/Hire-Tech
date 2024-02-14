// function printError(Id, Msg) {
//   document.getElementById(Id).innerHTML = Msg;
// }

// function validateForm() {

//   var name = document.Form.name.value;
//   var email = document.Form.email.value;
//   var password = document.Form.password.value;
//   var cfpwd = document.Form.confirm.value;


//   var nameErr = emailErr = pswErr = confirmErr = true;

//   if(name == "") {
//       printError("nameErr", "Please enter your name");
//   } else {
//       printError("nameErr", "");
//       nameErr = false;
//   }
  
//   if(email == "") {
//       printError("emailErr", "Please enter your email address");
//   } else {
//       var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
//       if(regex.test(email) === false) {
//           printError("emailErr", "Please enter a valid email address");
//       } else{
//           printError("emailErr", "");
//           emailErr = false;
//       }
//   }

//   if(password == "") {
//     printError("pswErr", "Please enter your password");
//   } else if(password.length < 8){
//     printError("pswErr", "Password must be at least 8 character");
//   } else {
//     printError("pswErr", "");
//     pswErr = false;
//   }

//   if(cfpwd == "") {
//     printError("confirmErr", "Please enter your password");
//   }else if(password.test(cfpwd) === false) {
//     printError("confirmErr", "Password doesn\'t match");
//   }else {
//     printError("confirmErr", "");
//     confirmErr = false;
//   }

//   if((nameErr || emailErr || pswErr || confirmErr) == true) {
//      return false;
//   } 
// };

const form = document.getElementById('form');
const email = document.getElementById('email');
const username = document.getElementById('name');
const password = document.getElementById('password');
const confirmpsw = document.getElementById('confirm');

const emailErr = document.getElementById('emailErr');
const nameErr = document.getElementById('nameErr');
const pswErr = document.getElementById('pswErr');
const cfErr = document.getElementById('cfErr');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const regexEmail = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  
  if (password.value === '' || password.value == null){
    e.preventDefault();
    pswErr.innerHTML = "Please Enter your password"
  }else if (password.value.length < 8) {
    e.preventDefault();
    pswErr.innerHTML = "Password must be least at 8 characters"
  }

  if (!email.value.match(regexEmail)) {
    e.preventDefault();
    emailErr.innerHTML = "Please Enter valid email"
  }

  if (username.value === '' || username.value == null){
    e.preventDefault();
    nameErr.innerHTML = "Please Enter your name"
  }

  if (!password.value === confirmpsw.value){
    e.preventDefault();
    cfErr.innerHTML = "Password doesn't match"
  }else if (confirmpsw.value === '' || confirmpsw.value == null){
    e.preventDefault();
    cfErr.innerHTML = "Please Enter your password"
  }
});

const setError = (element, message) => {
  const inputControl = element.parentElemant;
  const errorDisplay = inputControl.querySelector('.error');

  errorDisplay.innerText = message;
  inputControl.classList.add('error');
  inputControl.classList.remove('succes');
}

const setSuccess = element => {
  const inputControl = element.parentElemant;
  const errorDisplay = inputControl.querySelector('.error');

  errorDisplay.innerText = '';
  inputControl.add('success');
  inputControl.classList.remove('error');
}

const isValidEmail = email => {
  const regexEmail = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  return regexEmail.test(String(email).toLowerCase());
}

const validateInputs = () => {
  const nameValue = username.value.trim();
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();
  const confirmValue = confirmpswd.value.trim();

  if(emailValue === '') {
    setError(email, 'Please enter your email');
  } else if (!isValidEmail(emailValue)) {
    setError(email, 'Provide a valid email address');
  } else {
    setSuccess(email);
  }

  if(nameValue === '') {
    setError(username, 'Please enter your name');
  } else {
    setSuccess(username)
  }

  if(passwordValue === '') {
    setError(password, 'Please enter your password');
  } else if (passwordValue.length < 8) {
    setError(password, 'Password must be at least 8 character')
  } else {
    setSuccess(password);
  }

  if(confirmValue === '') {
    setError(confirmpswd, 'Please enter your password');
  } else if (passwordValue !== confirmValue) {
    setError(confirmpswd, 'Password doesn\'t match');
  } else {
    setSuccess(confirmpswd);
  }
};

