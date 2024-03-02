// Function to show the popup
function popupFunction(){
  document.getElementById('btn-post').addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'flex';
  });
  document.querySelector('.close').addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'none';
  });
  document.getElementById('post-btn').addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'none';
  });

}

function editPost(location, district, amphoe, province, zipcode, job_name, 
  salary, job_time, message, id, owner_email, owner_id ){
  $('div > div > div > a#edit').click(function(){
    document.querySelector('.bg-modal').style.display = 'flex';
  })
  
  $('#post-form')[0].reset();
  $('#location').val(location);
  $('#district').val(district);
  $('#amphoe').val(amphoe);
  $('#province').val(province);
  $('#zipcode').val(zipcode);
  $('#job_name').val(job_name);
  $('#salary').val(salary);
  $('#job_time').val(job_time);
  $('#message').val(message);
  $('#entryid').val(id)
  $('#owner_email').val(owner_email);
  $('#owner_id').val(owner_id);

}