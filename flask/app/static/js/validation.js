// Chananchida & Komson
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
  // check sign up or log in
  const currentType = e.target.type.value
  let data = {}
  // console.log(currentType)
  let errorStatus = false;
  const regexEmail = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  
  if (password.value === '' || password.value == null){
    e.preventDefault();
    errorStatus = true;
    pswErr.innerHTML = "Please Enter your password"
  }else if (password.value.length < 8) {
    e.preventDefault();
    errorStatus = true;
    pswErr.innerHTML = "Password must be least at 8 characters"
  }else{
    //add password to data
    data.password = password.value;
  }
  
  if (!email.value.match(regexEmail)) {
    e.preventDefault();
    errorStatus = true;
    emailErr.innerHTML = "Please Enter valid email"
  }else{
    //add email to data
    data.email = email.value;
  }

  if(currentType=='signup')
  {
  if (username.value === '' || username.value == null){
    e.preventDefault();
    errorStatus = true;
    nameErr.innerHTML = "Please Enter your name"
    }else{
      //add name to data
      data.name = username.value;
    }
  if (!password.value === confirmpsw.value){
    e.preventDefault();
    errorStatus = true;
    cfErr.innerHTML = "Password doesn't match"
    }
  else if (confirmpsw.value === '' || confirmpsw.value == null){
    e.preventDefault();
    errorStatus = true;
    cfErr.innerHTML = "Please Enter your password"
    }else{
      //add cfPassword to data
      data.cfpassword = confirmpsw.value;
    }
  }
  if(errorStatus){
    // if have error will not go to back-end
    return false
  }

  else{
    
    sendToBackEnd(`/${currentType==='login'?'':'signup'}`,'POST',data)

  }
});
// async function 
async function sendToBackEnd(path, method, body={} ){
  // รอให้เสร็จก่อน แล้วค่อย (fetch  wait for fetch ) 
  // fetch = สร้าง request ไปหลังบ้าน
  //check get?? if yes return undefined
  //if post send headers to back-end
  const response = await fetch(path, method==='GET'? 
  undefined:{method: method, body:JSON.stringify(body)
    , headers: { "Content-Type": "application/json" }})
  
  const responseBody = await response.json();
  window.location.href = responseBody.path;
  // console.log(responseBody)
  return responseBody;
}
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

