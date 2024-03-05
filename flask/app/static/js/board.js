//for dropdown menu
function dropdownFunction(){
    $(".dropdown").click(function() {
      $(".dropdown-menu").removeClass("show");
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
        // $(this).closest(".post").hide();
        $('.undo-hide').show();
        
      }
      if ($(this).text().trim() === "Delete") {
        $(this).closest(".post").hide();
        $('.undo-delete').show();
      }
      if ($(this).text().trim() === "Hired") {
        $('#no-hired').hide();
        
        $('.postoption').css({
          'border-top': 'none'
        })
      }
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
  // $('#entryid').val('')
  var url = "board/delete"
  var formData = { 'id': post_id };
  $.post(url, formData, function (callbackData) {
    refresh(url,formData);
  });
}

function unDelete(post_id){
  var url = "board/undelete"
  var formData = { 'id': post_id };
  $.post(url, formData, function (callbackData) {
    refresh(url,formData);
  });
}

function gotoprofile(owner_id){
  var url = "/oprofile"
  var formData = {'id':owner_id};
  $.post(url,formData, function(data){
  $('body').html(data)
  calculateTime(); //from utility.js
  dropdownFunction(); //from board.js
  popupFunction();//from popup.js
  editPost();//from popup.js
  })
  
}

// function hidePost(post_id){
//   // $('#entryid').val('')
//   var url = "board/hide"
//   var formData = { 'id': post_id };
//   $.post(url, formData, function (callbackData) {
//     //refresh #feed-box to new data
//     const parsedHTMLData = $.parseHTML(callbackData);
//     //console.log(parsedHTMLData)
//     // console.log("DELETE")
//     const feedbox = $(parsedHTMLData).find('#feed-box')
//     $('#feed-box').html(feedbox.html())
//     $('.undo-hide').click(function(){
//       $(".undo-hide").hide();
//       var url = "board/unhide"
//       var formData = { 'id': post_id };
//       $.post(url, formData, function (callbackData) {
//         //refresh #feed-box to new data
//         const parsedHTMLData = $.parseHTML(callbackData);
//         //console.log(parsedHTMLData)
//         // console.log("DELETE")
//         const feedbox = $(parsedHTMLData).find('#feed-box')
//         $('#feed-box').html(feedbox.html())
//         calculateTime();
//         dropdownFunction(); //from board.js
//         popupFunction();//from popup.js
//         editPost();//from popup.js
//       });
//     })
//   });
// }



function hirePost(post_id){
  var url = "board/hired"
  var formData = { 'id': post_id };
  $.post(url, formData, function (callbackData) {
    refresh(url,formData);
    $('#hired').show();
  });
}

