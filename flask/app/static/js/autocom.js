const searchWrapper = document.querySelector(".search-input");
const inputBox = document.querySelector("input");
const suggestBox = document.querySelector(".autocom-box");

// if user press any key and release
inputBox.onkeyup = (e) =>{
  let userData = e.target.value;
  let emptyArray = [];
  if(userData){
    emptyArray = suggest.filter((data) =>{
      return data.toLowerCase().startsWith(userData.toLowerCase());
    });
    emptyArray = emptyArray.map((data) =>{
      return data = '<li>'+ data +'</li>';
    });
    console.log(emptyArray);
    searchWrapper.classList.add("active"); //show autocom box
    showSuggestions(emptyArray);
    let allList = suggestBox.querySelectorAll("li");
    for (let i = 0; i < allList.length; i++){
      //adding onclick attr in all li tag
      allList[i].setAttribute("onclick", "select(this)");
    }
  }else{
    searchWrapper.classList.remove("active"); //hide autocom box
  }
}

function select(element){
  let selectUserData = element.textContent;
  inputBox.value = selectUserData; //passing the user selected list item data
  searchWrapper.classList.remove("active");
}

function showSuggestions(list){
  let listData;
  if(!list.length){
    userValue = inputBox.value;
    listData = '<li>'+userValue+'</li>';
  }else{
    listData = list.join('');
  }
  suggestBox.innerHTML = listData;
}

$(document).ready(function() {
  // Add event listener to the search input field
  $('#input-box').on('input', function() {
      var searchText = $(this).val().toLowerCase(); // Retrieve the input value

      // Iterate over each post
      $('.post').each(function() {
          var postContent = $(this).text().toLowerCase(); // Get the text content of the post

          // Show/hide posts based on whether they match the search criteria
          if (postContent.indexOf(searchText) !== -1) {
              $(this).show(); // Show the post if it matches the search criteria
          } else {
              $(this).hide(); // Hide the post if it doesn't match the search criteria
          }
      });
  });
});
