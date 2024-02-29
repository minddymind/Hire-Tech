// Function to show the popup
document.getElementById('btn-post').addEventListener('click', function(){
  document.querySelector('.bg-modal').style.display = 'flex';
});
document.querySelector('.close').addEventListener('click', function(){
  document.querySelector('.bg-modal').style.display = 'none';
});
