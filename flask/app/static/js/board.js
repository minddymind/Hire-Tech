//for dropdown menu
function dropdownFunction(){
    $(".dropdown").click(function() {
      $(this).find(".dropdown-menu").toggleClass("show");
    });

    // Close the dropdown menu when clicking outside of it
    $(document).click(function(e) {
      if (!$(e.target).closest('.dropdown').length) {
        $(".dropdown-menu").removeClass("show");
      }
    });
    $(".dropdown-item").click(function() {
      if ($(this).text().trim() === "Hide") {
        $(this).closest(".post").hide();
        $('.undo-hide').show();
      }
      if ($(this).text().trim() === "Delete") {
        $(this).closest(".post").hide();
        $('.undo-delete').show();
      }
      if ($(this).text().trim() === "Hired") {
        $('#no-hired').hide();
        $('#hired').show();
      }
    });
    $(".undo-text").click(function() {
      $(".post").show();
      $(".undo-hide").hide();
      $(".undo-delete").hide();
    });
    $(".close-back").click(function() {
      $(".undo-hide").hide();
      $(".undo-delete").hide();
    });

    //jQuery thailand
    $.Thailand({
        $district: $('#district'), // input ของตำบล
        $amphoe: $('#amphoe'), // input ของอำเภอ
        $province: $('#province'), // input ของจังหวัด
        $zipcode: $('#zipcode'), // input ของรหัสไปรษณีย์
    });
}

function deletePost(post_id){
  var url = "board/delete"
  var formData = { 'id': post_id };
    $.post(url, formData, function (callbackData) {
      //refresh #feed-box to new data
      const parsedHTMLData = $.parseHTML(callbackData);
      //console.log(parsedHTMLData)
      const feedbox = $(parsedHTMLData).find('#feed-box')
      $('#feed-box').html(feedbox.html())
      calculateTime(); //from utility.js
      dropdownFunction(); //from board.js
      popupFunction();//from popup.js
      editPost();//from popup.js
  });
  function undelete(post_id){
  
  }
}

function hirePost(post_id){
  var url = "board/hired"
  var formData = { 'id': post_id };
    $.post(url, formData, function (callbackData) {
      //refresh #feed-box to new data
      const parsedHTMLData = $.parseHTML(callbackData);
      //console.log(parsedHTMLData)
      const feedbox = $(parsedHTMLData).find('#feed-box')
      $('#feed-box').html(feedbox.html())
      calculateTime(); //from utility.js
      dropdownFunction(); //from board.js
      popupFunction();//from popup.js
      editPost();//from popup.js
  });
}



$(document).ready(function() {
  // Check if there are any hidden posts stored in localStorage
  var hiddenPosts = localStorage.getItem('hiddenPosts');
  if (hiddenPosts) {
    hiddenPosts = JSON.parse(hiddenPosts);
    // Hide each of the stored hidden posts
    hiddenPosts.forEach(function(postId) {
      $('#' + postId).hide();
    });
  }

  // Event listener for hiding posts
  $(".dropdown-item").click(function() {
    var postId = $(this).closest('.post').attr('id');
    if ($(this).text().trim() === "Hide") {
      $('#' + postId).hide();
      // Add the hidden post's ID to the list of hidden posts in localStorage
      if (!hiddenPosts) hiddenPosts = [];
      hiddenPosts.push(postId);
      localStorage.setItem('hiddenPosts', JSON.stringify(hiddenPosts));
    }
  });
});