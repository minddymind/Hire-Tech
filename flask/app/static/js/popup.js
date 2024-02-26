// Function to show the popup
document.getElementById('show-input').addEventListener('click', function(){
  document.querySelector('.bg-modal').style.display = 'flex';
});
document.querySelector('.close').addEventListener('click', function(){
  document.querySelector('.bg-modal').style.display = 'none';
});
