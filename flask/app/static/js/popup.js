// Function to show the popup
document.getElementById('show-input').addEventListener('click', function(){
  console.log("aaaaaaaaaa")
  document.querySelector('.bg-modal').style.display = 'flex';
});
document.querySelector('.close').addEventListener('click', function(){
  console.log("bbbbbbbbb")
  document.querySelector('.bg-modal').style.display = 'none';
});
